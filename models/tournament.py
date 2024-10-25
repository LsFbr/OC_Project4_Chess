from .round import Round
from .match import Match

import random
from tinydb import TinyDB, Query

db = TinyDB("data/db.json")


class Tournament:
    def __init__(
            self,
            name,
            location,
            description,
            players,
            number_of_rounds=4
    ):
        self.name = name
        self.location = location
        self.description = description
        self.players = players
        self.number_of_rounds = number_of_rounds

        self.start_date = None
        self.end_date = None
        self.current_round_number = 0
        self.rounds = []
        self.previous_matches = []

    def serialize(self):
        return {
            "name": self.name,
            "location": self.location,
            "description": self.description,
            "players": [player.serialize() for player in self.players],
            "number_of_rounds": self.number_of_rounds,
            "current_round_number": self.current_round_number,
            "rounds": [round.serialize() for round in self.rounds],
            "previous_matches": [
                match.serialize() for match in self.previous_matches
            ]
        }

    def create_round(self):
        self.current_round_number += 1
        round_name = f"Round {self.current_round_number}"
        round = Round(round_name)

        if self.current_round_number == 1:
            random.shuffle(self.players)
        else:
            self.players.sort(key=lambda x: x.score, reverse=True)

        for i in range(0, len(self.players) - 1, 2):
            player_1 = self.players[i]
            player_2 = self.players[i + 1]

            match = Match(player_1, player_2)

            round.matches.append(match)
            self.previous_matches.append(match)

        self.rounds.append(round)
        return round

    def __repr__(self):
        return f"{self.name}"

    def save_tournament(self):
        tournaments_table = db.table("tournaments")
        tournaments_table.upsert(self.serialize(), Query().name == self.name)
