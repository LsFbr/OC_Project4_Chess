from datetime import datetime


class Round:
    def __init__(self, name, players):
        self.name = name
        self.start_date = None
        self.end_date = None
        self.players: players
        self.matchs = []

    def start_round(self):
        self.start_date = datetime.now()

    def end_round(self):
        self.end_date = datetime.now()

    def create_matchs(self):
        pass

    def pair_players(self):
        pass
