class Round:
    def __init__(
            self,
            round_name: str,
            start_date: str,
            end_date: str,
    ):
        self.round_name = round_name
        self.start_date = start_date
        self.end_date = end_date

        self.matches = []

    def pair_players(self, player_1, player_2):
        pass
