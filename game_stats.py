import json


class GameStats:
    """Track statistics for Alien Invasion"""
    def __init__(self, ai_settings):
        self.ai_settings = ai_settings
        self.ships_left = 0
        self.high_score = None
        self.score = None
        self.level = None
        self.reset_stats()
        self.initialize_high_score()
        self.game_active = False

    def reset_stats(self):
        """Initialize statistics that change during game play"""
        self.ships_left = self.ai_settings.ship_limit
        self.score = 0
        self.level = 1

    def initialize_high_score(self):
        """Read the saved high score from the json file on disk (if it exists)"""
        try:
            with open('score_data.json', 'r') as file:
                self.high_score = int(json.load(file))    # Cast to int to verify type
        except (FileNotFoundError, ValueError, EOFError, json.JSONDecodeError) as e:
            print(e)
            self.high_score = 0     # Some issue with the file, going to default

    def save_high_score(self):
        """Save the high score to a json file on disk"""
        with open('score_data.json', 'w') as file:
            json.dump(self.high_score, file)
