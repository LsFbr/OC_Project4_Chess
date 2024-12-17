from datetime import datetime


class Round:
    def __init__(
            self,
            round_name: str,
            matches=None,
            start_date=None,
            end_date=None
    ):
        """
        Initialize a Round instance.

        :param round_name: The name of the round.
        :param matches: A list of matches in the round.
        :param start_date: The start date of the round.
        :param end_date: The end date of the round.
        """
        self.round_name = round_name
        self.matches = matches if matches else []
        self.start_date = start_date
        self.end_date = end_date

    def serialize(self):
        """
        Serialize the round data to a dictionary.

        :return: A dictionary representation of the round.
        """
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
        """
        Set the start date of the round to the current date and time.
        """
        self.start_date = datetime.now()

    def end_round(self):
        """
        Set the end date of the round to the current date and time.
        """
        self.end_date = datetime.now()
