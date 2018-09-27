from pygame import sprite
from pygame import Surface


class BunkerBlock(sprite.Sprite):
    """Represents a portion of bunker block"""
    def __init__(self, ai_settings, screen, row, col):
        super().__init__()
        self.screen = screen
        self.height = ai_settings.bunker_block_size
        self.width = ai_settings.bunker_block_size
        self.color = ai_settings.bunker_color
        self.image = Surface((self.width, self.height))
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.row = row
        self.col = col

    def update(self):
        self.screen.blit(self.image, self.rect)


def make_bunker(ai_settings, screen, position):
    """Create a bunker at the given position on the screen from a series of blocks"""
    bunker = sprite.Group()
    for i in range(4):
        for j in range(9):
            # Don't draw full rows of blocks on last two rows, to style the bunker
            if not ((i > 2 and (1 < j < 7)) or (i > 1 and (2 < j < 6))):
                block = BunkerBlock(ai_settings, screen, i, j)
                block.rect.x = int(ai_settings.screen_width * 0.15) + (250 * position) + (j * block.width)
                block.rect.y = int(ai_settings.screen_height * 0.8) + (i * block.height)
                bunker.add(block)
    return bunker
