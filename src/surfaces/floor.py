from configs.colors import LIGHTGREY

from surfaces.basic_surface import BasicSurface


class Floor(BasicSurface):
    def __init__(self, sprites, floors, x, y):
        super().__init__(sprites, floors, x, y)
        self.image.fill(LIGHTGREY)
