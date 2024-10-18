from models.player import Player
from models.tournament import Tournament
from views.view import View
from tinydb import TinyDB

database = TinyDB("data/database.json")


class Controller:
    def __init__(self):
        self.view = View()

        self.players = []
        self.tournament = None

    def run(self):
        self.view.welcome()
        while True:
            main_menu_result = self.view.main_menu()
            if main_menu_result == "1":
                self.create_tournament()
            elif main_menu_result == "2":
                self.add_players()
            elif main_menu_result == "3":
                self.start_tournament()
            elif main_menu_result == "0":
                return

    def add_players(self):
        while True:
            (name, surname, birthday, national_chess_id) = (
                self.view.prompt_for_add_player()
            )
            if not name or not surname or not birthday or not national_chess_id:
                return
            player = Player(name, surname, birthday, national_chess_id)
            self.players.append(player)
            player.save_player()
            if not self.view.prompt_for_add_another_player():

                return

    def create_tournament(self):
        (name, location, description, number_of_rounds) = (
            self.view.prompt_for_tournament()
        )

        self.tournament = Tournament(
            name, location, description, self.players, number_of_rounds
        )

        self.tournament.save_tournament()

    def start_tournament(self):
        self.tournament.create_round()
