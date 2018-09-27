from pygame import mixer


class Settings:
    """Stores settings for Alien Invasion"""
    def __init__(self):
        # screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.stars_limit = 8
        print('Automatic screen resolution: ' + str(self.screen_width) + ' ' + str(self.screen_height))
        self.bg_color = (0, 0, 0)

        # ship settings
        self.ship_speed_factor = None
        self.ship_limit = 3

        # bullet settings
        self.bullet_speed_factor = None
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (255, 255, 255)
        self.bullets_allowed = 3

        # beam settings
        self.beam_speed_factor = None
        self.beams_allowed = 1

        # sound settings
        self.alien_death_sound = mixer.Sound('sound/alien_death.wav')
        self.alien_fire_sound = mixer.Sound('sound/alien_shoot.wav')
        self.ship_fire_sound = mixer.Sound('sound/ship_shoot.wav')
        self.ship_death_sound = mixer.Sound('sound/ship_death.wav')
        self.alien_death_sound.set_volume(0.3)
        self.alien_fire_sound.set_volume(0.3)
        self.ship_fire_sound.set_volume(0.3)
        self.ship_death_sound.set_volume(0.5)
        self.audio_channels = 3
        self.ship_channel = mixer.Channel(0)
        self.alien_channel = mixer.Channel(1)
        self.death_channel = mixer.Channel(2)

        # alien settings
        self.alien_speed_factor = None
        self.fleet_drop_speed = 10
        self.fleet_direction = None
        self.alien_points = None
        self.score_scale = 1.5

        # How quickly the game speeds up
        self.speedup_scale = 1.1
        self.initialize_dynamic_settings()
        self.initialize_audio_settings()

    def initialize_dynamic_settings(self):
        """Initialize that change while the game is active"""
        self.ship_speed_factor = 1.5
        self.bullet_speed_factor = 3
        self.beam_speed_factor = 0.25
        self.alien_speed_factor = 1

        # scoring
        self.alien_points = 50

        # fleet_direction : 1 represents right, -1 represents left
        self.fleet_direction = 1

    def initialize_audio_settings(self):
        """Initialize pygame audio settings"""
        mixer.init()
        mixer.set_num_channels(self.audio_channels)

    def increase_speed(self):
        """Increase speed settings and point values"""
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale)
