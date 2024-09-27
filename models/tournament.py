from models.round import Round


class Tournament:
    def __init__(self,
                 name,
                 location,
                 start_date,
                 end_date,
                 players,
                 description,
                 number_of_rounds=4,):
        self.name = name
        self.location = location
        self.start_date = start_date
        self.end_date = end_date
        self.players = players
        self.description = description
        self.number_of_rounds = number_of_rounds
        self.rounds = []

    def create_rounds(self):
        for i in range(self.number_of_rounds):
            round = Round(f"Round{i+1}", self.players)
            round.create_matchs()
            self.rounds.append(round)
