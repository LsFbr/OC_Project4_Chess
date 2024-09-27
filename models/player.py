class Player:
    def __init__(self, name, surname, date_of_birth, score=0):
        self.name = name
        self.surname = surname
        self.date_of_birth = date_of_birth
        self.score = score

    def __str__(self):
        return f"{self.name} is {self.age} years old"

    def __repr__(self):
        return self.__str__()
