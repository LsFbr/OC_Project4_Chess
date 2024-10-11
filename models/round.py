from datetime import datetime


class Round:
    def __init__(
            self,
            round_name: str,

    ):
        self.round_name = round_name

        self.start_date = None
        self.end_date = None
        self.matches = []

    def serialize(self):
        return {
            "round_name": self.round_name,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "matches": self.matches
        }

    def start_round(self):
        self.start_date = datetime.now()

    def end_round(self):
        self.end_date = datetime.now()
