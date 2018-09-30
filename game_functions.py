import sys
import pygame
import random

from alien import Alien
from bullet import Bullet
from beam import Beam
from ufo import Ufo
from star import Star


def check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, beams, bullets):
    """Handle key presses and mouse events"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            stats.save_high_score()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, sb, play_button,
                              ship, aliens, beams, bullets, mouse_x, mouse_y)
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, stats.game_active, ship, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)


def check_play_button(ai_settings, screen, stats, sb, play_button,
                      ship, aliens, beams, bullets, mouse_x, mouse_y):
    """Start a new game when the play button is clicked"""
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        # Hide the mouse
        pygame.mouse.set_visible(False)
        # Reset settings
        ai_settings.initialize_dynamic_settings()
        # Reset game stats
        stats.reset_stats()
        stats.game_active = True
        # Reset scoreboard images
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()
        # Remove all aliens and bullets
        aliens.empty()
        bullets.empty()
        beams.empty()
        # Create new alien fleet and center the ship
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()


def check_keydown_events(event, ai_settings, screen, game_active, ship, bullets):
    """Handle key presses"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE and game_active:   # Prevent sounds from occurring when game not active
        fire_bullet(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_q:
        sys.exit()


def check_keyup_events(event, ship):
    """Handle key releases"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False


def fire_bullet(ai_settings, screen, ship, bullets):
    """Fire a bullet if the limit has not been reached already"""
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        ship.fire_weapon()
        bullets.add(new_bullet)


def fire_random_beam(ai_settings, screen, aliens, beams):
    """Fire a beam from a random alien in the fleet"""
    firing_alien = random.choice(aliens.sprites())
    if len(beams) < ai_settings.beams_allowed and \
            (ai_settings.beam_stamp is None or
             (abs(pygame.time.get_ticks() - ai_settings.beam_stamp) > ai_settings.beam_time)):
        new_beam = Beam(ai_settings, screen, firing_alien)
        firing_alien.fire_weapon()
        beams.add(new_beam)


def alien_collision_check(bullet, alien):
    if alien.dead:
        return False
    return pygame.sprite.collide_rect(bullet, alien)


def check_alien_bullet_collisions(ai_settings, screen, stats, sb, ship, aliens, beams, bullets, ufo):
    """Check that any aliens have been hit, handle empty fleet condition"""
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, False, collided=alien_collision_check)
    if collisions:
        for aliens in collisions.values():
            for a in aliens:
                stats.score += ai_settings.alien_points[str(a.alien_type)]
                a.begin_death()
            sb.prep_score()
        check_high_score(stats, sb)
    ufo_collide = pygame.sprite.groupcollide(bullets, ufo, True, False, collided=alien_collision_check)
    if ufo_collide:
        for ufo in ufo_collide.values():
            for u in ufo:
                stats.score += u.score
                u.begin_death()
            sb.prep_score()
        check_high_score(stats, sb)
    if len(aliens) == 0:
        # destroy all existing bullets and re-create fleet, increase speed
        beams.empty()
        bullets.empty()
        ai_settings.increase_speed()
        stats.level += 1
        sb.prep_level()
        create_fleet(ai_settings, screen, ship, aliens)


def check_ship_beam_collisions(ai_settings, screen, stats, sb, ship, aliens, beams, bullets, ufo):
    """Check that any alien beams have collided with the ship"""
    collide = pygame.sprite.spritecollideany(ship, beams)
    if collide:
        ship_hit(ai_settings, screen, stats, sb, ship, aliens, beams, bullets, ufo)


def check_bunker_collisions(beams, bullets, bunkers):
    """Check if any beams or bullets have collided with the bunkers"""
    pygame.sprite.groupcollide(bullets, bunkers, True, True)
    pygame.sprite.groupcollide(beams, bunkers, True, True)


def update_bullets_beams(ai_settings, screen, stats, sb, ship, aliens, beams, bullets, ufo):
    """Update the positions of all bullets, remove bullets that are no longer visible"""
    bullets.update()
    beams.update()
    # Remove bullets that are out of view
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    for beam in beams.copy():
        if beam.rect.bottom > ai_settings.screen_height:
            beams.remove(beam)
    check_alien_bullet_collisions(ai_settings, screen, stats, sb, ship, aliens, beams, bullets, ufo)
    check_ship_beam_collisions(ai_settings, screen, stats, sb, ship, aliens, beams, bullets, ufo)


def check_high_score(stats, sb):
    """Check to see if there's a new high score."""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()


def update_screen(ai_settings, screen, stats, sb, ship, aliens, beams, bullets, bunkers, play_button, stars, ufo_group):
    """Update images on the screen and flip to new screen"""
    if stats.game_active:
        ufo_event_check(ai_settings, screen, ufo_group)
    screen.fill(ai_settings.bg_color)
    stars.update()
    stars.draw(screen)
    # Redraw all bullets
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    # Redraw all beams
    for beam in beams.sprites():
        beam.blitme()
    if ufo_group:
        ufo_group.update()
        for ufo in ufo_group.sprites():
            ufo.blitme()
    aliens.draw(screen)
    check_bunker_collisions(beams, bullets, bunkers)
    sb.show_score()
    ship.blitme()
    bunkers.update()
    if not stats.game_active:
        play_button.draw_button()
    pygame.display.flip()


def get_number_aliens(ai_settings, alien_width):
    """Determine the number of aliens that can fit in a row"""
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2.5 * alien_width))
    return number_aliens_x


def get_number_rows(ai_settings, ship_height, alien_height):
    """Determine the number of rows of aliens that can fit in a row"""
    available_space_y = (ai_settings.screen_height - (4 * alien_height) - ship_height)
    number_rows = int(available_space_y / (2.5 * alien_height))
    return number_rows


def ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets, beams, ufo):
    """Respond to ship being hit by an alien"""
    if ufo:     # ufos play sound, so kill them first so the death sound is clear
        for u in ufo.sprites():
            u.kill()
    ship.death()
    ship.update()
    while ship.dead:
        screen.fill(ai_settings.bg_color)
        ship.blitme()
        pygame.display.flip()
        ship.update()
    if stats.ships_left > 0:
        # Decrement lives
        stats.ships_left -= 1
        # Remove all aliens and bullets on screen
        aliens.empty()
        bullets.empty()
        beams.empty()
        # Re-create fleet and center ship
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()
        # Update scoreboard
        sb.prep_ships()
    else:
        stats.game_active = False
        stats.save_high_score()
        pygame.mouse.set_visible(True)


def check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, beams, bullets, ufo):
    """Check if any aliens have reached the bottom of the screen"""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # Treated the same as if the ship has been hit
            ship_hit(ai_settings, screen, stats, sb, ship, aliens, beams, bullets, ufo)
            break


def update_aliens(ai_settings, screen, stats, sb, ship, aliens, beams, bullets, ufo):
    """Check if any aliens in the fleet have reached an edge,
    then update the positions of all aliens"""
    check_fleet_edges(ai_settings, aliens)
    aliens.update()
    # check for alien-ship collisions
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, screen, stats, sb, ship, aliens, beams, bullets, ufo)
    # Check that any aliens have hit the bottom of the screen
    check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, beams, bullets, ufo)
    if aliens.sprites():
        fire_random_beam(ai_settings, screen, aliens, beams)


def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    """Create an alien and place it in a row"""
    if row_number < 2:
        alien_type = 1
    elif row_number < 4:
        alien_type = 2
    else:
        alien_type = 3
    alien = Alien(ai_settings, screen, alien_type)
    alien_width = alien.rect.width
    alien.x = alien_width + 1.25 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 1.25 * alien.rect.height * row_number
    alien.rect.y += int(ai_settings.screen_height / 8)
    aliens.add(alien)


def create_fleet(ai_settings, screen, ship, aliens):
    """Creates a full fleet of aliens"""
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)

    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number, row_number)


def change_fleet_direction(ai_settings, aliens):
    """Drop the entire fleet down, and change the fleets direction"""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1


def check_fleet_edges(ai_settings, aliens):
    """Respond in the event any aliens have reached an edge of the screen"""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break


def create_random_ufo(ai_settings, screen):
    """With a chance of 10% create a Ufo and return it with the time it was created"""
    ufo = None
    time_stamp = None
    if random.randrange(0, 100) <= 10:  # 10% chance of ufo
        ufo = Ufo(ai_settings, screen)
        time_stamp = pygame.time.get_ticks()
    return time_stamp, ufo


def ufo_event_check(ai_settings, screen, ufo_group):
    """Check if now is a good time to create a ufo and if so create one and add it to the ufo group"""
    if not ai_settings.last_ufo and not ufo_group:
        ai_settings.last_ufo, n_ufo = create_random_ufo(ai_settings, screen)
        if n_ufo:
            ufo_group.add(n_ufo)
    elif abs(pygame.time.get_ticks() - ai_settings.last_ufo) > ai_settings.ufo_min_interval and not ufo_group:
        ai_settings.last_ufo, n_ufo = create_random_ufo(ai_settings, screen)
        if n_ufo:
            ufo_group.add(n_ufo)


def create_stars(ai_settings, screen):
    """Create a sprite group of stars that are placed randomly in the background"""
    stars = pygame.sprite.Group()
    for i in range(ai_settings.stars_limit):
        new_star = Star(ai_settings, screen)
        stars.add(new_star)
    return stars
