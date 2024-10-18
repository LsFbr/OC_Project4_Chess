from models.player import Player
from models.tournament import Tournament
from views.view import View


class Controller:
    def __init__(self):
        self.view = View()

        self.players = []
        self.tournament = None

    def run(self):
        self.view.welcome()
        self.add_players()
        print(self.players)
        self.create_tournament()
        print(self.tournament)

    def add_players(self):
        while True:
            (name, surname, birthday, national_chess_id) = (
                self.view.prompt_for_player()
            )

            if not name:
                return
            player = Player(name, surname, birthday, national_chess_id)
            self.players.append(player)

    def create_tournament(self):
        (name, location, description, number_of_rounds) = (
            self.view.prompt_for_tournament()
        )

        self.tournament = Tournament(
            name, location, description, self.players, number_of_rounds
        )

    def start_tournament(self):
        self.tournament.create_round()
