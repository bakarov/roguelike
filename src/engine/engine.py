import copy
import math
import pygame
import random

from configs.settings import MAXIMUM_DISTANCE_TO_ENEMY, MAXIMUM_DARKNESS, DARKNESS_TIMER, ENEMY_AI_TIMER
from configs.variables import GAME_OVER_STATE, NEXT_LEVEL_STATE
from configs.window import TILESIZE

from engine.enemy import Enemy
from engine.player import Player
from engine.darkness import Darkness

from surfaces.floor import Floor
from surfaces.wall import Wall
from surfaces.door import Door


class Engine(object):
    def __init__(self, camera, screen):
        # Common
        self.screen = screen
        self.camera = camera

        # Sprites
        self.sprites = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.walls = pygame.sprite.Group()
        self.floors = pygame.sprite.Group()
        self.doors = pygame.sprite.Group()

        # Objects
        self.player = None
        self.darkness = Darkness(self.screen)

        # Utils
        self.moving_directions = {
            'left': {'dx': -1, 'dy': 0, 'direction': 'left'},
            'right': {'dx': 1, 'dy': 0, 'direction': 'right'},
            'up': {'dx': 0, 'dy': -1, 'direction': 'up'},
            'down': {'dx': 0, 'dy': 1, 'direction': 'down'},
            'stay': {'dx': 0, 'dy': 0, 'direction': 'stay'}
        }
        self.timer = pygame.time.get_ticks()

    def create_dungeon_object(self, dungeon):
    
        offset_x, offset_y = 0, 0
        self.dungeon = copy.deepcopy(dungeon)
        dungeon_size = len(self.dungeon) - 1
        for a in range(dungeon_size):
            for b in range(dungeon_size):
                if dungeon[a][b].any():
                    for j in range(TILESIZE):
                        for i in range(TILESIZE):
                            spire_container = []
                            for case in dungeon[a][b][j][i]:
                                if case == 1 or case == 2:
                                    spire_container.append(
                                        Wall(self.sprites, self.walls, i + offset_x, j + offset_y))
                                elif case == 0:
                                    spire_container.append(
                                        Floor(self.sprites, self.floors, i + offset_x, j + offset_y))
                                elif case == 3:
                                    spire_container.append(
                                        Enemy(self.camera, self.enemies, i + offset_x, j + offset_y, self.screen, random.choice(list(self.moving_directions.values()))))
                                elif case == 4:
                                    spire_container.append(
                                                Door(self.sprites, self.doors, i + offset_x, j + offset_y))
                            self.dungeon[a][b][j][i] = spire_container
                offset_x += TILESIZE
            offset_y += TILESIZE
            offset_x = 0

    def place_player(self):
        dungeon_size = len(self.dungeon) - 1
        for j in range(TILESIZE):
            for i in range(TILESIZE):
                for case in self.dungeon[dungeon_size // 2][dungeon_size // 2][j][i]:
                    if isinstance(case, Floor):
                        self.player = Player(
                            self.sprites, self.camera, dungeon_size // 2 * TILESIZE + i, dungeon_size // 2 * TILESIZE + j, self.screen, self.moving_directions['stay'])
                        return

    def set_difficulty(self, difficulty_multiplier):
        self.darkness.increase_multiplier(difficulty_multiplier)

    def move_player(self, direction):
        self.player.direction = self.moving_directions[direction]
        self.player.change_animation('run')
        if not self.collide_with_walls(self.player.x, self.player.y, self.moving_directions[direction]['dx'], self.moving_directions[direction]['dy']):
            self.player.x += self.moving_directions[direction]['dx']
            self.player.y += self.moving_directions[direction]['dy']
            self.player.play_sound()

    def idle_player(self, direction):
        self.player.change_animation('idle')
        self.player.direction = self.moving_directions[direction]

    def collide_with_walls(self, x, y, dx, dy):
        for wall in self.walls:
            if wall.x == x + dx and wall.y == y + dy:
                return True

    def collide_with_doors(self, x, y, dx, dy):
        for door in self.doors:
            if door.x == x + dx and door.y == y + dy:
                return True

    def move_enemies_and_check_if_reach_player(self):
        for enemy in self.enemies:
            # update enemy ai
            # move enemy every second
            if pygame.time.get_ticks() - enemy.enemy_move_timer > ENEMY_AI_TIMER:
                enemy.enemy_move_timer = pygame.time.get_ticks()
                # move enemy
                if not self.collide_with_walls(enemy.x, enemy.y, enemy.direction['dx'], enemy.direction['dy']) and not self.collide_with_doors(enemy.x, enemy.y, enemy.direction['dx'], enemy.direction['dy']):
                    enemy.x += enemy.direction['dx']
                    enemy.y += enemy.direction['dy']
            
            # change moving direction once in a while
            if pygame.time.get_ticks() - enemy.enemy_direction_change_timer > DARKNESS_TIMER:
                enemy.enemy_direction_change_timer = pygame.time.get_ticks()
                enemy.direction = random.choice(
                    list(self.moving_directions.values()))
            
            if enemy.direction['direction'] == 'stay':
                enemy.change_animation('idle')
            else:
                enemy.change_animation('run')

            # check distance to enemy
            distance_to_player = math.sqrt((self.player.x - enemy.x)**2 + (self.player.y - enemy.y)**2)
            if distance_to_player <= MAXIMUM_DISTANCE_TO_ENEMY:
                return True

        return False

    def check_if_level_complete(self):
        for door in self.doors:
            if door.x == self.player.x and door.y == self.player.y:
                return True

    def check_if_reach_maximum_darkness(self):
        if self.darkness.darkness_value >= MAXIMUM_DARKNESS:
            return True

    def get_player(self):
        return self.player

    def update(self):
        self.sprites.update()
        self.enemies.update()

        if pygame.time.get_ticks() - self.timer > 500:
            self.timer = pygame.time.get_ticks()
            self.darkness.make_darker()
        
        if self.move_enemies_and_check_if_reach_player() or self.check_if_reach_maximum_darkness():
            return GAME_OVER_STATE

        if self.check_if_level_complete():
            return NEXT_LEVEL_STATE

    def draw(self):

        # Draw walls / floors / doors
        for sprite in self.sprites:
            if not isinstance(sprite, Player):
                self.screen.blit(sprite.image, self.camera.apply(sprite))

        # Draw objects
        self.player.draw()
        
        for enemy in self.enemies:
            enemy.draw()
        self.darkness.draw()
    