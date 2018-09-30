import pygame

import game_functions as gf

from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from bunker import make_bunker
from settings import Settings
from ship import Ship

# TODO: Audio more like real space invaders, time frequency check for beams, startup screen


def run_game():
    pygame.init()
    ai_settings = Settings()    # Setup pygame, settings, and display
    screen = pygame.display.set_mode(
        (ai_settings.screen_width, ai_settings.screen_height)
    )
    pygame.display.set_caption('Alien Invasion')
    play_button = Button(ai_settings, screen, 'Play')
    clock = pygame.time.Clock()

    # Setup game stats and scoreboard
    stats = GameStats(ai_settings)
    sb = Scoreboard(ai_settings, screen, stats)
    # Setup ship, bullets, beams, aliens, background stars
    ship = Ship(ai_settings, screen)
    bullets = pygame.sprite.Group()
    beams = pygame.sprite.Group()
    aliens = pygame.sprite.Group()
    ufo = pygame.sprite.Group()
    stars = gf.create_stars(ai_settings, screen)
    gf.create_fleet(ai_settings, screen, ship, aliens)
    bunkers = pygame.sprite.Group(make_bunker(ai_settings, screen, 0),
                                  make_bunker(ai_settings, screen, 1),
                                  make_bunker(ai_settings, screen, 2),
                                  make_bunker(ai_settings, screen, 3))

    while True:
        clock.tick(70)  # 70 fps limit
        gf.check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, beams, bullets)
        if stats.game_active:
            ship.update()
            gf.update_bullets_beams(ai_settings, screen, stats, sb, ship, aliens, beams, bullets, ufo)
            gf.update_aliens(ai_settings, screen, stats, sb, ship, aliens, beams, bullets, ufo)
        gf.update_screen(ai_settings, screen, stats, sb, ship, aliens, beams, bullets, bunkers, play_button, stars, ufo)


if __name__ == '__main__':
    run_game()
