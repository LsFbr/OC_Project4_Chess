from models.player import Player
from models.tournament import Tournament
from views.view import View

from tinydb import TinyDB, Query

db = TinyDB("data/db.json")


class Controller:
    def __init__(self):
        self.view = View()

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
                self.db_show_all_players()
            elif choice == "2":
                self.db_add_players()
            elif choice == "3":
                self.db_edit_player()
            elif choice == "0":
                return

    def tournaments_menu(self):
        while True:
            choice = self.view.tournaments_menu()
            if choice == "1":
                self.db_show_all_tournaments()
            elif choice == "2":
                self.create_tournament()
            elif choice == "3":
                self.edit_tournament()
            elif choice == "4":
                self.start_tournament()
            elif choice == "0":
                return

    def tournament_edit_menu(self, tournament, tournament_id):
        while True:
            choice = self.view.tournament_edit_menu()
            if choice == "1":
                self.view.show_tournament_infos(tournament)
                self.view.show_all_tournament_players(tournament["players"])
            if choice == "2":
                self.edit_tournament_infos(tournament, tournament_id)
            if choice == "3":
                self.add_tournament_players(tournament, tournament_id)
            if choice == "4":
                self.remove_tournament_players(tournament, tournament_id)
            elif choice == "0":
                return

    def db_show_all_players(self):
        self.db_sort_players_alphabetically()

        players_table = db.table("players")
        players = players_table.all()

        if not players:
            self.view.print("No players available.")
            return

        self.view.show_all_players(players)

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

    def db_edit_player(self):

        self.db_show_all_players()

        self.view.print(
            "Enter the national chess ID of the player you want to edit :"
        )
        national_chess_id = self.view.prompt_for_chess_id()

        players_table = db.table("players")
        player = players_table.get(
            Query().national_chess_id == national_chess_id
        )

        if not player:
            self.view.print("\nPlayer not found.\n")
            return

        self.view.show_player(player)
        new_name, new_surname, new_birthday, new_national_chess_id = (
            self.view.prompt_for_edit_player()
        )

        player["name"] = new_name if new_name else player["name"]
        player["surname"] = new_surname if new_surname else player["surname"]
        player["birthday"] = (
            new_birthday if new_birthday
            else player["birthday"]
        )
        player["national_chess_id"] = (
            new_national_chess_id if new_national_chess_id
            else player["national_chess_id"]
        )

        players_table.update(
            player, Query().national_chess_id == national_chess_id
        )

        self.view.print("\nPlayer successfully updated.\n")

    def db_sort_players_alphabetically(self):
        """
        Sort players alphabetically by name and surname in the players table
        in the database, and update their keys to match their index.
        """
        players_table = db.table("players")

        players = players_table.all()
        if not players:
            return

        sorted_players = sorted(
            players, key=lambda x: (
                x["name"].lower(), x["surname"].lower()
            )
        )

        players_table.truncate()

        for player in sorted_players:
            players_table.insert(player)

    def db_show_all_tournaments(self):
        tournaments_table = db.table("tournaments")
        tournaments = tournaments_table.all()

        if not tournaments:
            self.view.print("No tournaments available.")
            return

        self.view.show_all_tournaments(tournaments)

    def create_tournament(self):

        # Create a new tournament
        (name, location, description, number_of_rounds) = (
            self.view.prompt_for_tournament()
        )

        if not number_of_rounds:
            number_of_rounds = 4
        else:
            number_of_rounds = int(number_of_rounds)

        self.tournament = Tournament(
            name, location, description, [], number_of_rounds
        )

        # Add players to the tournament
        players_table = db.table("players")
        players = players_table.all()

        self.view.show_all_players(players)

        national_chess_ids = self.view.prompt_for_add_tournament_players()
        national_chess_ids_list = [
            chess_id.strip() for chess_id in national_chess_ids.split(",")
        ]

        # Create a list of Player objects from the selected players
        selected_players = []
        for chess_id in national_chess_ids_list:
            player_data = players_table.get(
                Query().national_chess_id == chess_id
            )
            if player_data:
                player = Player(
                    name=player_data["name"],
                    surname=player_data["surname"],
                    birthday=player_data["birthday"],
                    national_chess_id=player_data["national_chess_id"]
                )
                selected_players.append(player)
            else:
                self.view.print(
                    f"\nPlayer with National Chess ID {chess_id} not found.\n"
                )

        self.tournament.players = selected_players

        # Save the tournament in the database
        tournaments_table = db.table("tournaments")
        tournaments_table.insert(self.tournament.serialize())

        self.view.print("\nTournament saved.\n")

    def add_tournament_players(self, tournament, tournament_id):
        self.view.show_all_tournament_players(tournament["players"])

        players_table = db.table("players")
        players = players_table.all()

        self.view.show_all_players(players)

        national_chess_ids = self.view.prompt_for_add_tournament_players()
        national_chess_ids_list = [
            chess_id.strip() for chess_id in national_chess_ids.split(",")
        ]

        existing_ids = {
            player["national_chess_id"] for player in tournament["players"]
        }

        # Create a list of Player objects from the selected players
        selected_players = []
        for chess_id in national_chess_ids_list:
            if chess_id in existing_ids:
                self.view.print(
                    f"\nPlayer with National Chess ID {chess_id} "
                    "is already in the tournament.\n"
                )
                continue

            player_data = players_table.get(
                Query().national_chess_id == chess_id
            )
            if player_data:
                player = {
                    "name": player_data["name"],
                    "surname": player_data["surname"],
                    "birthday": player_data["birthday"],
                    "national_chess_id": player_data["national_chess_id"]
                    }

                if player not in tournament["players"]:
                    selected_players.append(player)
            else:
                self.view.print(
                    f"\nPlayer with National Chess ID {chess_id} not found.\n"
                )

        tournament["players"].extend(selected_players)

        tournaments_table = db.table("tournaments")
        tournaments_table.update(
            tournament, doc_ids=[tournament_id]
        )

        self.view.print("\nTournament successfully updated.\n")

    def remove_tournament_players(self, tournament, tournament_id):
        self.view.show_all_tournament_players(tournament["players"])

        national_chess_ids = self.view.prompt_for_remove_tournament_players()
        national_chess_ids_list = [
            chess_id.strip() for chess_id in national_chess_ids.split(",")
        ]

        selected_players = []
        for chess_id in national_chess_ids_list:
            player = next(
                (
                    player for player in tournament["players"]
                    if player["national_chess_id"] == chess_id
                ),
                None
            )
            if player:
                selected_players.append(player)
            else:
                self.view.print(
                    f"\nPlayer with National Chess ID {chess_id} "
                    "is not in the tournament.\n"
                )

        for player in selected_players:
            tournament["players"].remove(player)

        tournaments_table = db.table("tournaments")
        tournaments_table.update(
            tournament, doc_ids=[tournament_id]
        )

        self.view.print("\nTournament successfully updated.\n")

    def edit_tournament(self):
        tournaments_table = db.table("tournaments")
        tournaments = tournaments_table.all()

        if not tournaments:
            self.view.print("No tournaments available.")
            return

        self.view.show_all_tournaments(tournaments)

        self.view.print(
            "Enter the ID of the tournament you want to edit :"
        )

        tournament_id = int(self.view.prompt_for_tournament_id())

        tournament = tournaments_table.get(doc_id=tournament_id)

        if not tournament:
            self.view.print("\nTournament not found.\n")
            return

        self.tournament_edit_menu(tournament, tournament_id)

    def edit_tournament_infos(self, tournament, tournament_id):
        self.view.show_tournament_infos(tournament)

        new_name, new_location, new_description, new_number_of_rounds = (
            self.view.prompt_for_edit_tournament_infos()
        )

        tournament["name"] = new_name if new_name else tournament["name"]
        tournament["location"] = (
            new_location if new_location else tournament["location"]
        )
        tournament["description"] = (
            new_description if new_description else tournament["description"]
        )
        tournament["number_of_rounds"] = (
            new_number_of_rounds if new_number_of_rounds
            else tournament["number_of_rounds"]
        )

        tournaments_table = db.table("tournaments")
        tournaments_table.update(
            tournament, doc_ids=[tournament_id]
        )

        self.view.print("\nTournament successfully updated.\n")

    def select_tournament(self):
        tournaments_table = db.table("tournaments")
        tournaments = tournaments_table.all()

        if not tournaments:
            self.view.print("No tournaments available.")
            return

        self.view.show_all_tournaments(tournaments)

        self.view.print(
            "Enter the ID of the tournament you want to select :"
        )

        tournament_id = int(self.view.prompt_for_tournament_id())

        tournament = tournaments_table.get(doc_id=tournament_id)

        if not tournament:
            self.view.print("\nTournament not found.\n")
            return

        return tournament, tournament_id

    def start_tournament(self):

        tournament, tournament_id = self.select_tournament()
        players = []
        for player in tournament["players"]:
            player = Player(
                player["name"],
                player["surname"],
                player["birthday"],
                player["national_chess_id"],
                player["score"]
            )
            players.append(player)

        self.tournament = Tournament(
            tournament["name"],
            tournament["location"],
            tournament["description"],
            players,
            tournament["number_of_rounds"]
        )

        self.view.print(self.tournament)

        round = next(
            (
                round for round in self.tournament.rounds
                if round.start_date and not round.end_date
            ),
            None
        )

        # self.tournament.create_round()
        # self.tournament.save_tournament()
