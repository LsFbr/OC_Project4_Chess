class Match:
    def __init__(self, player_1, player_2, player_1_score=0, player_2_score=0):
        self.player_1 = player_1
        self.player_2 = player_2
        self.player_1_score = player_1_score
        self.player_2_score = player_2_score

    def serialize(self):
        return (
            [self.player_1.serialize(), self.player_1_score],
            [self.player_2.serialize(), self.player_2_score]
        )

    def set_result(self, result):
        result = int(result)
        if result == 1:
            self.player_1_score += 1
            self.player_1.score += 1
        elif result == 2:
            self.player_2_score += 1
            self.player_2.score += 1
        elif result == 0:
            self.player_1_score += 0.5
            self.player_1.score += 0.5
            self.player_2_score += 0.5
            self.player_2.score += 0.5

    def __repr__(self):
        return (
            f"{self.player_1.national_chess_id} "
            f"{self.player_1.name} {self.player_1.surname} "
            f"({self.player_1_score}|{self.player_2_score}) "
            f"{self.player_2.national_chess_id} "
            f"{self.player_2.name} {self.player_2.surname}"
        )
