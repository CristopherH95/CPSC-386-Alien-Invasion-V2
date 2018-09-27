import pygame

import game_functions as gf

from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from settings import Settings
from ship import Ship


def run_game():
    pygame.init()
    ai_settings = Settings()    # Setup pygame, settings, and display
    screen = pygame.display.set_mode(
        (ai_settings.screen_width, ai_settings.screen_height)
    )
    pygame.display.set_caption('Alien Invasion')
    play_button = Button(ai_settings, screen, 'Play')

    # Setup game stats and scoreboard
    stats = GameStats(ai_settings)
    sb = Scoreboard(ai_settings, screen, stats)
    # Setup ship, bullets, beams, aliens, background stars
    ship = Ship(ai_settings, screen)
    bullets = pygame.sprite.Group()
    beams = pygame.sprite.Group()
    aliens = pygame.sprite.Group()
    stars = gf.create_stars(ai_settings, screen)
    gf.create_fleet(ai_settings, screen, ship, aliens)

    while True:
        gf.check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, beams, bullets)
        if stats.game_active:
            ship.update()
            gf.update_bullets_beams(ai_settings, screen, stats, sb, ship, aliens, beams, bullets)
            gf.update_aliens(ai_settings, screen, stats, sb, ship, aliens, beams, bullets)
        gf.update_screen(ai_settings, screen, stats, sb, ship, aliens, beams, bullets, play_button, stars)


if __name__ == '__main__':
    run_game()
