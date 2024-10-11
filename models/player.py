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

    def __str__(self):
        return [f"{self.name}, {self.surname}", f"{self.score}"]

    def __repr__(self):
        return self.__str__()
