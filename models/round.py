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
            "start_date": str(self.start_date) if self.start_date else None,
            "end_date": str(self.end_date) if self.end_date else None,
            "matches": [match.serialize() for match in self.matches]
        }

    def start_round(self):
        self.start_date = datetime.now()

    def end_round(self):
        self.end_date = datetime.now()

    def __repr__(self):
        return f"{self.round_name} : {self.matches}"
