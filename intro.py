from pygame.sysfont import SysFont
from pygame import Rect, display, draw, time


class Button:
    """Represents a click-able button style text, with altering text color"""
    def __init__(self, settings, screen, msg, y_factor=0.65):
        self.settings = settings
        self.screen = screen
        self.screen_rect = screen.get_rect()

        # Dimensions and properties of the button
        self.button_color = (0, 255, 0)
        self.text_color = (255, 255, 255)
        self.alt_color = (0, 255, 0)
        self.font = SysFont(None, 48)
        self.y_factor = y_factor

        # Prep button message
        self.msg = msg
        self.msg_image, self.msg_image_rect = None, None
        self.prep_msg(self.text_color)

    def check_button(self, mouse_x, mouse_y):
        """Check if the given button has been pressed"""
        if self.msg_image_rect.collidepoint(mouse_x, mouse_y):
            return True
        else:
            return False

    def alter_text_color(self, mouse_x, mouse_y):
        """Change text color if the mouse coordinates collide with the button"""
        if self.check_button(mouse_x, mouse_y):
            self.prep_msg(self.alt_color)
        else:
            self.prep_msg(self.text_color)

    def prep_msg(self, color):
        """Turn msg into a rendered image and center it on the button"""
        self.msg_image = self.font.render(self.msg, True, color, self.settings.bg_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.centerx = (self.settings.screen_width // 2)
        self.msg_image_rect.centery = int(self.settings.screen_height * self.y_factor)

    def draw_button(self):
        """blit message to the screen"""
        self.screen.blit(self.msg_image, self.msg_image_rect)


class Title:
    """Represents the title text to be displayed on screen"""
    def __init__(self, bg_color, screen, text, text_color=(255, 255, 255)):
        self.bg_color = bg_color
        self.screen = screen
        self.text = text
        self.text_color = text_color
        self.font = SysFont(None, 56)
        self.image = None
        self.image_rect = None

    def prep_image(self):
        """Render the subtitle text as an image"""
        self.image = self.font.render(self.text, True, self.text_color, self.bg_color)
        self.image_rect = self.image.get_rect()

    def blitme(self):
        """Draw the subtitle's image to the screen"""
        self.screen.blit(self.image, self.image_rect)


class Subtitle:
    """Represents the subtitle text displayed on screen"""
    def __init__(self, bg_color, screen, text):
        self.bg_color = bg_color
        self.screen = screen
        self.text = text
        self.text_color = (0, 255, 0)
        self.font = SysFont(None, 48)
        self.image = None
        self.image_rect = None

    def prep_image(self):
        """Render the subtitle text as an image"""
        self.image = self.font.render(self.text, True, self.text_color, self.bg_color)
        self.image_rect = self.image.get_rect()

    def blitme(self):
        """Draw the subtitle's image to the screen"""
        self.screen.blit(self.image, self.image_rect)


class Intro:
    """Contains information and methods relating to the start menu"""
    def __init__(self, settings, game_stats, screen):
        # settings, settings, stats
        self.settings = settings
        self.game_stats = game_stats
        self.screen = screen

        # text/image information
        self.title = Title(settings.bg_color, self.screen, 'SPACE')
        self.subtitle = Subtitle(settings.bg_color, self.screen, 'INVADERS')

    def prep_image(self):
        """Render the title as an image"""
        self.title.prep_image()
        self.title.image_rect.centerx = (self.settings.screen_width // 2)
        self.title.image_rect.centery = (self.settings.screen_height // 2) - self.title.image_rect.height
        self.subtitle.prep_image()
        self.subtitle.image_rect.centerx = (self.settings.screen_width // 2)
        self.subtitle.image_rect.centery = (self.settings.screen_height // 2) + (self.title.image_rect.height // 2)

    def show_menu(self):
        """Draw the title to the screen"""
        self.title.blitme()
        self.subtitle.blitme()


def level_intro(ai_settings, screen, stats):
    """Display a level intro screen for 1.5 seconds"""
    if stats.game_active:
        level_text = Title(ai_settings.bg_color, screen, 'Level: ' + str(stats.level))
        level_text.prep_image()
        level_text.image_rect.centerx = (ai_settings.screen_width // 2)
        level_text.image_rect.centery = (ai_settings.screen_height // 2) - level_text.image_rect.height
        start_time = time.get_ticks()
        while abs(start_time - time.get_ticks()) <= 1500:
            screen.fill(ai_settings.bg_color)
            level_text.blitme()
            display.flip()
