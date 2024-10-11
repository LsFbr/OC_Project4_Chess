class Player:
    def __init__(
            self,
            name: str,
            surname: str,
            birthday: str,
            national_chess_id: str,
    ):
        self.name = name
        self.surname = surname
        self.birthday = birthday
        self.national_chess_id = national_chess_id

        self.score = 0.0

    def serialize(self):
        return {
            "name": self.name,
            "surname": self.surname,
            "birthday": self.birthday,
            "national_chess_id": self.national_chess_id,
            "score": self.score
        }
