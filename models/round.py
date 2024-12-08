from datetime import datetime


class Round:
    def __init__(
            self,
            round_name: str,
            matches=None,
            start_date=None,
            end_date=None
    ):

        self.round_name = round_name
        self.matches = matches if matches else []
        self.start_date = start_date
        self.end_date = end_date

    def serialize(self):
        return {
            "round_name": self.round_name,
            "matches": [
                match.serialize() for match in self.matches
            ],
            "start_date": (
                self.start_date.isoformat() if self.start_date else None
            ),
            "end_date": (
                self.end_date.isoformat() if self.end_date else None
            )
        }

    def start_round(self):
        self.start_date = datetime.now()

    def end_round(self):
        self.end_date = datetime.now()

    def __repr__(self):
        return f"{self.round_name}"
