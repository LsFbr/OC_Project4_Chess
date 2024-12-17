from tinydb import TinyDB, Query

db = TinyDB("data/db.json")


class Player:
    def __init__(
            self,
            name: str,
            surname: str,
            birthday: str,
            national_chess_id: str,
            score=0.0
    ):
        """
        Initialize a Player instance.

        :param name: The player's  name.
        :param surname: The player's first name.
        :param birthday: The player's date of birth.
        :param national_chess_id: The player's national chess ID.
        :param score: The player's score in the tournament.
        """
        self.name = name
        self.surname = surname
        self.birthday = birthday
        self.national_chess_id = national_chess_id
        self.score = score

    def serialize(self):
        """
        Serialize the player data to a dictionary.

        :return: A dictionary representation of the player.
        """
        return {
            "name": self.name,
            "surname": self.surname,
            "birthday": self.birthday,
            "national_chess_id": self.national_chess_id,
        }

    def db_save_player(self):
        """
        Save or update the player in the database in the "players" table.
        """
        players_table = db.table("players")
        players_table.upsert(
            self.serialize(),
            Query().national_chess_id == self.national_chess_id
        )
