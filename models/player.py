class Player:
    def __init__(
            self,
            name: str,
            surname: str,
            birthday: str,
            rank: str
    ):
        self.name = name
        self.surname = surname
        self.birthday = birthday
        self.rank = rank

        self.score = 0
