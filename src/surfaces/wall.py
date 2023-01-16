from configs.colors import DARKGREY

from surfaces.basic_surface import BasicSurface


class Wall(BasicSurface):
    def __init__(self, sprites, floors, x, y):
        super().__init__(sprites, floors, x, y)
        self.image.fill(DARKGREY)
