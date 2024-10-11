class Tournament:
    def __init__(
            self,
            name: str,
            location: str,
            start_date: str,
            end_date: str,
            players: list,
            description: str,
            current_round: int,
            rounds: list,
            number_of_rounds=4
    ):
        self.name = name
        self.location = location
        self.start_date = start_date
        self.end_date = end_date
        self.players = players
        self.description = description
        self.current_round = current_round
        self.rounds = rounds
        self.number_of_rounds = number_of_rounds

    def shuffle_players(self):
        pass

    def sort_players_by_score(self):
        pass
