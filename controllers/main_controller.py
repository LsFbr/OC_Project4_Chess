from typing import List
from models.player import Player


class Controler:
    def __init__(self, view):
        self.players: List[Player] = []

        self.view = view

    def get_players(self):
        pass

    def shuffle_players(self):
        pass

    def make_round(self):
        pass

    def start_tournament(self):
        self.shuffle_players()

    def run(self):
        self.get_players()
