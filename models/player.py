from tinydb import TinyDB, Query

db = TinyDB("data/db.json")


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
            "score": self.score,
        }

    def __repr__(self):
        return (
            f"{self.name} {self.surname}\n"
            f"Birthday : {self.birthday}\n"
            f"Chess ID : {self.national_chess_id}"
            f"Score in tournament : {self.score}"
        )

    def db_save_player(self):
        players_table = db.table("players")
        players_table.upsert(
            self.serialize(),
            Query().national_chess_id == self.national_chess_id
        )
