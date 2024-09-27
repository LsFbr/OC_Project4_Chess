class Match:
    def __init__(self, player1, player2):
        self.player1 = player1
        self.player2 = player2

    def make_match(self):
        match = (
            [self.player1, self.player1.score],
            [self.player2, self.player2.score]
            )
        return match
