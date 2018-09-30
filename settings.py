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

        # bunker settings
        self.bunker_block_size = 10
        self.bunker_color = (0, 255, 0)

        # beam settings
        self.beam_speed_factor = None
        self.beams_allowed = 1

        # sound settings
        self.audio_channels = 4
        self.ship_channel = mixer.Channel(0)
        self.alien_channel = mixer.Channel(1)
        self.death_channel = mixer.Channel(2)
        self.ufo_channel = mixer.Channel(3)

        # alien settings
        self.alien_speed_factor = None
        self.ufo_speed = None
        self.last_ufo = None
        self.ufo_min_interval = 30000
        self.fleet_drop_speed = 10
        self.fleet_direction = None
        self.alien_points = None
        self.ufo_point_values = [50, 100, 150]
        self.beam_stamp = None
        self.beam_time = 1000

        # How quickly the game speeds up
        self.speedup_scale = 1.1
        # initialize dynamics
        self.initialize_dynamic_settings()
        self.initialize_audio_settings()

    def initialize_dynamic_settings(self):
        """Initialize that change while the game is active"""
        self.ship_speed_factor = 6
        self.bullet_speed_factor = 10
        self.beam_speed_factor = 2
        self.alien_speed_factor = 2
        self.ufo_speed = self.alien_speed_factor * 2

        # scoring
        self.alien_points = {'1': 10, '2': 20, '3': 40}

        # fleet_direction : 1 represents right, -1 represents left
        self.fleet_direction = 1

    def initialize_audio_settings(self):
        """Initialize pygame audio settings"""
        mixer.init()
        mixer.set_num_channels(self.audio_channels)
        mixer.music.load('sound/space-invaders-bgm.wav')
        mixer.music.set_volume(0.75)

    def increase_speed(self):
        """Increase speed settings and point values"""
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale
