class Match:
    def __init__(
            self, player_1,
            player_2,
            player_1_match_score=0,
            player_2_match_score=0):
        """
        Initialize a Match instance.

        :param player_1: The first player in the match.
        :param player_2: The second player in the match.
        :param player_1_match_score: Score of the first player in the match.
        :param player_2_match_score: Score of the second player in the match.
        """
        self.player_1 = player_1
        self.player_2 = player_2
        self.player_1_match_score = player_1_match_score
        self.player_2_match_score = player_2_match_score

    def serialize(self):
        """
        Serialize the match data to a tuple.

        :return: A tuple representation of the match.
        """
        return (
            [{"player_1": self.player_1.serialize(), "player_1_match_score": self.player_1_match_score}],
            [{"player_2": self.player_2.serialize(), "player_2_match_score": self.player_2_match_score}]
        )

    def set_result(self, result):
        """
        Set the result of the match.

        :param result: The result of the match
            (1 for player 1 win, 2 for player 2 win, 0 for draw).
        """
        result = int(result)
        if result == 1:
            self.player_1_match_score += 1
            self.player_1.score += 1
        elif result == 2:
            self.player_2_match_score += 1
            self.player_2.score += 1
        elif result == 0:
            self.player_1_match_score += 0.5
            self.player_1.score += 0.5
            self.player_2_match_score += 0.5
            self.player_2.score += 0.5

    def __repr__(self):
        """
        Return a string representation of the match.

        :return: A string representation of the match.
        """
        return (
            f"{self.player_1.national_chess_id} "
            f"{self.player_1.name} {self.player_1.surname} "
            f"({self.player_1_match_score}|{self.player_2_match_score}) "
            f"{self.player_2.national_chess_id} "
            f"{self.player_2.name} {self.player_2.surname}"
        )
