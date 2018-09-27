import pygame
from time import sleep


class Ship(pygame.sprite.Sprite):
    def __init__(self, ai_settings, screen):
        """Initialize ship and set starting position"""
        super().__init__()
        self.screen = screen
        self.ai_settings = ai_settings
        # Load ship image and set rect attributes
        self.image = pygame.image.load('images/ship.png')
        self.image_death = pygame.image.load('images/ship_death.png')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom
        # Moving status flags
        self.moving_right = False
        self.moving_left = False
        # Store center as decimal
        self.center = float(self.rect.centerx)

    def update(self):
        """Update ship's position based on moving state"""
        # Move right/left based on moving status flags, unless the ship is at the edge of the screen
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center += self.ai_settings.ship_speed_factor
        if self.moving_left and self.rect.left > 0:
            self.center -= self.ai_settings.ship_speed_factor

        self.rect.centerx = self.center

    def center_ship(self):
        """Center the ship on the screen"""
        self.center = self.screen_rect.centerx

    def death(self):
        """Switch ship to death image briefly and pause"""
        original_img = self.image
        self.image = self.image_death
        self.blitme()
        pygame.display.flip()
        sleep(0.5)
        self.image = original_img

    def blitme(self):
        self.screen.blit(self.image, self.rect)
