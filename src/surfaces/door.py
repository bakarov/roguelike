from configs.colors import RED

from surfaces.basic_surface import BasicSurface


class Door(BasicSurface):
    def __init__(self, sprites, doors, x, y):
        super().__init__(sprites, doors, x, y)
        self.image.fill(RED)

    def open(self):
        self.door_open.play()
