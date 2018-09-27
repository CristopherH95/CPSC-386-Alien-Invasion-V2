from pygame.sysfont import SysFont
from pygame import Rect


class Button:
    def __init__(self, ai_settings, screen, msg):
        self.ai_settings = ai_settings
        self.screen = screen
        self.screen_rect = screen.get_rect()

        # Dimensions and properties of the button
        self.width, self.height = 200, 50
        self.button_color = (0, 255, 0)
        self.text_color = (255, 255, 255)
        self.font = SysFont(None, 48)
        # Build button rect and center it
        self.rect = Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center
        # Prep button message only once
        self.msg_image, self.msg_image_rect = None, None
        self.prep_msg(msg)

    def prep_msg(self, msg):
        """Turn msg into a rendered image and center it on the button"""
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        """Draw button and then draw message"""
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)
