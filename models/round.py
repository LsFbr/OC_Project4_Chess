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
            "start_date": str(self.start_date) if self.start_date else None,
            "end_date": str(self.end_date) if self.end_date else None,
            "matches": [match.serialize() for match in self.matches]
        }

    def start_round(self):
        self.set_start_date()

    def set_start_date(self):
        self.start_date = datetime.now()

    def set_end_date(self):
        self.end_date = datetime.now()

    def __repr__(self):
        return f"{self.round_name}"
