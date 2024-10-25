from models.player import Player
from models.tournament import Tournament
from views.view import View

from prettytable import PrettyTable
from tinydb import TinyDB

db = TinyDB("data/db.json")


class Controller:
    def __init__(self):
        self.view = View()

        self.players = []
        self.tournament = None

    def run(self):
        self.view.welcome()
        self.main_menu()

    def main_menu(self):
        while True:
            choice = self.view.main_menu()
            if choice == "1":
                self.players_menu()
            elif choice == "2":
                self.tournaments_menu()
            elif choice == "0":
                self.view.print("\nGoodbye!\n")
                return

    def players_menu(self):
        while True:
            choice = self.view.players_menu()
            if choice == "1":
                self.show_all_players()
            elif choice == "2":
                self.db_add_players()
            elif choice == "3":
                self.edit_player()
            elif choice == "0":
                return

    def show_all_players(self):
        self.db_sort_players_alphabetically()

        players_table = db.table("players")
        players = players_table.all()

        table = PrettyTable()
        table.title = "<<<REGISTERED PLAYERS>>>"
        table.field_names = [
            "National Chess ID", "Name", "Surname", "Birthday"
        ]

        for player in players:
            table.add_row([
                player["national_chess_id"],
                player["name"],
                player["surname"],
                player["birthday"]
            ])

        self.view.print(table)

    def db_add_players(self):
        while True:
            (name, surname, birthday, national_chess_id) = (
                self.view.prompt_for_add_player()
            )
            if (
                not name
                or not surname
                or not birthday
                or not national_chess_id
            ):
                return

            player = Player(name, surname, birthday, national_chess_id)
            player.db_save_player()

            self.db_sort_players_alphabetically()

            if not self.view.prompt_for_add_another_player():
                return

    def db_sort_players_alphabetically(self):
        """
        Sort players alphabetically by name and surname in the players table
        in the database, and update their keys to match their index.
        """

        players_table = db.table("players")
        players = players_table.all()

        sorted_players = sorted(
            players, key=lambda x: (x["name"].lower(), x["surname"].lower())
        )

        sorted_players_dict = {}
        for index, player in enumerate(sorted_players, start=1):
            sorted_players_dict[str(index)] = player

        players_table.truncate()

        players_table.insert({"players": sorted_players_dict})

    def create_tournament(self):
        (name, location, description, number_of_rounds) = (
            self.view.prompt_for_tournament()
        )

        if not number_of_rounds:
            self.tournament = Tournament(
                name, location, description, self.players
                )
        else:
            number_of_rounds = int(number_of_rounds)
            self.tournament = Tournament(
                name, location, description, self.players, number_of_rounds
                )

        self.tournament.save_tournament()

    def start_tournament(self):
        self.tournament.create_round()
        self.tournament.save_tournament()
