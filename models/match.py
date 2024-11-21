class Match:
    def __init__(self, player_1, player_2):
        self.player_1 = player_1
        self.player_2 = player_2

        self.winner = None

    def serialize(self):
        return (
            [self.player_1.serialize(), self.player_1.score],
            [self.player_2.serialize(), self.player_2.score]
        )

    def set_result(self, result):
        if result == 1:
            self.player_1.score += 1
            self.winner = self.player_1
        elif result == 2:
            self.player_2.score += 1
            self.winner = self.player_2
        else:
            self.player_1.score += 0.5
            self.player_2.score += 0.5
            self.winner = "Draw"

    def __repr__(self):
        return f"{self.player_1} vs {self.player_2}"
