from configs.window import WIDTH


class Text(object):
    def __init__(self, screen, x, y, text, font, color, center=True):
        super(Text, self).__init__()
        self.screen = screen
        self.x = x
        self.y = y
        self.text = font.render(text, 1, color)
        if center:
            self.x = WIDTH / 2 - self.text.get_width() / 2

    def render(self):
        self.show = self.screen.blit(self.text, (self.x, self.y))
        return self
