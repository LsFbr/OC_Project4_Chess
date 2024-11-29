from .round import Round
from .match import Match

from datetime import datetime
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
            number_of_rounds=4,
            current_round_number=0,
            rounds=None,
            start_date=None,
            end_date=None
    ):
        self.name = name
        self.location = location
        self.description = description
        self.players = players
        self.number_of_rounds = number_of_rounds
        self.current_round_number = current_round_number
        self.rounds = rounds if rounds else []
        self.start_date = start_date
        self.end_date = end_date

    def serialize(self):
        return {
            "name": self.name,
            "location": self.location,
            "description": self.description,
            "players": [
                {
                    "name": player.name,
                    "surname": player.surname,
                    "birthday": player.birthday,
                    "national_chess_id": player.national_chess_id,
                    "score": player.score
                } for player in self.players
            ],
            "number_of_rounds": self.number_of_rounds,
            "current_round_number": self.current_round_number,
            "rounds": [round.serialize() for round in self.rounds],
            "start_date": (
                self.start_date.isoformat()
                if self.start_date
                else None
            ),
            "end_date": (
                self.end_date.isoformat()
                if self.end_date
                else None
            )
        }

    def create_round(self):
        self.current_round_number += 1
        round_name = f"Round {self.current_round_number}"
        round = Round(round_name)

        if self.current_round_number == 1:
            random.shuffle(self.players)
        else:
            self.players.sort(
                key=lambda x: (x.score, random.random()), reverse=True
            )

        # Track all pairs that have already played
        played_pairs = set()
        for previous_round in self.rounds:
            for match in previous_round.matches:
                pair = frozenset(
                    [
                        match.player_1.national_chess_id,
                        match.player_2.national_chess_id
                    ]
                )
                played_pairs.add(pair)

        unpaired_players = self.players[:]

        while len(unpaired_players) > 1:
            player_1 = unpaired_players.pop(0)
            best_match = None

            # Find the first player_2 who has not played with player_1 yet
            for player_2 in unpaired_players:
                current_pair = frozenset(
                    [player_1.national_chess_id, player_2.national_chess_id]
                )
                if current_pair not in played_pairs:
                    best_match = player_2
                    break

            # Pick the first remaining player
            if not best_match:
                best_match = unpaired_players[0]

            unpaired_players.remove(best_match)

            match = Match(player_1, best_match)
            round.matches.append(match)

        self.rounds.append(round)
        return round

    def start_current_round(self):
        self.rounds[-1].start_round()

    def __repr__(self):
        return (
            f"<<<Tournament : {self.name} --- "
            f"Round |{self.current_round_number}/{self.number_of_rounds}|>>>"
        )

    def set_start_date(self):
        self.start_date = datetime.now()

    def set_end_date(self):
        self.end_date = datetime.now()

    def save_tournament(self):
        tournaments_table = db.table("tournaments")
        tournaments_table.upsert(self.serialize(), Query().name == self.name)

    def get_ranked_players(self):
        return sorted(
            self.players, key=lambda player: (
                -player.score, random.random()
            )
        )
