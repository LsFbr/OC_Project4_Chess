from models.player import Player
from models.match import Match
from models.round import Round
from models.tournament import Tournament
from views.view import View

from datetime import datetime

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
            elif choice == "3":
                self.reports_menu()
            elif choice == "0":
                self.view.print("\nGoodbye!\n")
                return
            else:
                self.view.print("\nInvalid choice! Please try again.")
                continue

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
            else:
                self.view.print("\nInvalid choice! Please try again.")
                continue

    def tournaments_menu(self):
        while True:
            choice = self.view.tournaments_menu()
            if choice == "1":
                self.db_show_all_tournaments()
            elif choice == "2":
                self.create_tournament()
            elif choice == "3":
                tournament, tournament_id = self.select_tournament()
                if tournament:
                    self.tournament_edit_menu(tournament, tournament_id)
            elif choice == "4":
                self.start_tournament()
            elif choice == "0":
                return
            else:
                self.view.print("\nInvalid choice! Please try again.")
                continue

    def reports_menu(self):
        while True:
            choice = self.view.reports_menu()
            if choice == "1":
                self.db_show_all_players()
            elif choice == "2":
                self.db_show_all_tournaments()
            elif choice == "3":
                self.report_tournament_details()
            elif choice == "4":
                self.report_tournament_players()
            elif choice == "5":
                self.report_tournament_rounds_and_matches()
            elif choice == "0":
                return
            else:
                self.view.print("\nInvalid choice! Please try again.")
                continue

    def tournament_edit_menu(self, tournament, tournament_id):
        while True:
            choice = self.view.tournament_edit_menu()
            if choice == "1":
                self.view.show_tournament_infos(tournament)
                self.view.show_all_tournament_players(tournament.players)
            elif choice == "2":
                self.edit_tournament_infos(tournament, tournament_id)
            elif choice == "3":
                self.add_tournament_players(tournament, tournament_id)
            elif choice == "4":
                self.remove_tournament_players(tournament, tournament_id)
            elif choice == "0":
                return
            else:
                self.view.print("\nInvalid choice! Please try again.")
                continue

    def report_tournament_details(self):
        tournament, _ = self.select_tournament()
        if tournament:
            self.view.show_tournament_details(tournament)

    def report_tournament_players(self):
        tournament, _ = self.select_tournament()
        if tournament:
            sorted_tournament = self.db_sort_tournament_players(tournament)
            self.view.show_all_tournament_players(sorted_tournament.players)

    def report_tournament_rounds_and_matches(self):
        tournament, tournament_id = self.select_tournament()
        if tournament and tournament.rounds:
            self.view.show_all_rounds(tournament, tournament.rounds)

    def db_show_all_players(self):
        self.db_sort_players_alphabetically()

        players_table = db.table("players")
        players_data = players_table.all()

        if not players_data:
            self.view.print("No players available.")
            return

        players = [Player(**player) for player in players_data]
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
        player_data = players_table.get(
            Query().national_chess_id == national_chess_id
        )

        if not player_data:
            self.view.print("\nPlayer not found.\n")
            return

        # Convert the player data to a Player instance
        player = Player(**player_data)

        self.view.show_player(player)
        new_name, new_surname, new_birthday, new_national_chess_id = (
            self.view.prompt_for_edit_player()
        )

        player.name = new_name if new_name else player.name
        player.surname = new_surname if new_surname else player.surname
        player.birthday = new_birthday if new_birthday else player.birthday
        player.national_chess_id = (
            new_national_chess_id if new_national_chess_id else player.national_chess_id
        )

        # Update the player in the database using serialize()
        players_table.update(
            player.serialize(), Query().national_chess_id == national_chess_id
        )

        self.view.print("\nPlayer successfully updated.\n")

    def db_sort_tournament_players(self, tournament):
        """
        Sort players in a tournament by name (ascending).
        return: the updated tournament
        """
        if not tournament.players:
            self.view.print("\nNo players available in this tournament.\n")
            return tournament

        sorted_players = sorted(
            tournament.players,
            key=lambda player: (
                player.name.lower(), player.surname.lower()
            )
        )

        tournament.players = sorted_players

        return tournament

    def db_sort_players_alphabetically(self):
        """
        Sort players alphabetically by name and surname in the players table
        in the database.
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
        tournaments_data = tournaments_table.all()

        if not tournaments_data:
            self.view.print("No tournaments available.")
            return

        tournaments = [
            (Tournament(**tournament), tournament.doc_id)
            for tournament in tournaments_data
        ]
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

        # Add players to the tournament
        players_table = db.table("players")
        players_data = players_table.all()

        # Convert player data to Player instances
        players = [Player(**player) for player in players_data]

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

        self.tournament = Tournament(
            name, location, description, selected_players, number_of_rounds
        )

        self.tournament = self.db_sort_tournament_players(self.tournament)
        # Save the tournament in the database
        tournaments_table = db.table("tournaments")
        tournaments_table.insert(self.tournament.serialize())
        self.tournament = None

        self.view.print("\nTournament saved.\n")

    def add_tournament_players(self, tournament, tournament_id):
        self.view.show_all_tournament_players(tournament.players)

        players_table = db.table("players")
        players_data = players_table.all()

        self.view.show_all_players([Player(**player) for player in players_data])

        national_chess_ids = self.view.prompt_for_add_tournament_players()
        national_chess_ids_list = [
            chess_id.strip() for chess_id in national_chess_ids.split(",")
        ]

        existing_ids = {player.national_chess_id for player in tournament.players}

        # Create a list of Player objects from the selected players
        selected_players = []
        for chess_id in national_chess_ids_list:
            if chess_id in existing_ids:
                self.view.print(
                    f"Player with National Chess ID {chess_id} "
                    "is already in the tournament."
                )
                continue

            player_data = players_table.get(
                Query().national_chess_id == chess_id
            )
            if player_data:
                player = Player(**player_data)

                if player not in tournament.players:
                    selected_players.append(player)
                    self.view.print(
                        f"Added {chess_id} "
                        f"{player.name} {player.surname}."
                    )
            else:
                self.view.print(
                    f"Player with National Chess ID {chess_id} not found."
                )

        tournament.players.extend(selected_players)

        tournament = self.db_sort_tournament_players(tournament)

        tournaments_table = db.table("tournaments")
        tournaments_table.update(
            tournament.serialize(), doc_ids=[tournament_id]
        )

        self.view.print("\nTournament successfully updated.")

    def remove_tournament_players(self, tournament, tournament_id):
        self.view.show_all_tournament_players(tournament.players)

        national_chess_ids = self.view.prompt_for_remove_tournament_players()
        national_chess_ids_list = [
            chess_id.strip() for chess_id in national_chess_ids.split(",")
        ]

        selected_players = []
        for chess_id in national_chess_ids_list:
            player = next(
                (
                    player for player in tournament.players
                    if player.national_chess_id == chess_id
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
            tournament.players.remove(player)
            self.view.print(
                f"Removed {player.national_chess_id} "
                f"{player.name} {player.surname}."
            )

        tournaments_table = db.table("tournaments")
        tournaments_table.update(
            tournament.serialize(), doc_ids=[tournament_id]
        )

        self.view.print("Tournament successfully updated.")

    def edit_tournament(self):
        tournaments_table = db.table("tournaments")
        tournaments_data = tournaments_table.all()

        if not tournaments_data:
            self.view.print("No tournaments available.")
            return

        tournaments = [
            (Tournament(**tournament), tournament.doc_id)
            for tournament in tournaments_data
        ]
        self.view.show_all_tournaments(tournaments)

        self.view.print(
            "Enter the ID of the tournament you want to edit :"
        )

        tournament_id = int(self.view.prompt_for_tournament_id())

        tournament_data = tournaments_table.get(doc_id=tournament_id)

        if not tournament_data:
            self.view.print("\nTournament not found.\n")
            return

        tournament = Tournament(**tournament_data)
        self.view.show_tournament_infos(tournament)
        self.tournament_edit_menu(tournament, tournament_id)

    def edit_tournament_infos(self, tournament, tournament_id):
        self.view.show_tournament_infos(tournament)

        new_name, new_location, new_description, new_number_of_rounds = (
            self.view.prompt_for_edit_tournament_infos()
        )

        tournament.name = new_name if new_name else tournament.name
        tournament.location = new_location if new_location else tournament.location
        tournament.description = new_description if new_description else tournament.description
        tournament.number_of_rounds = (
            int(new_number_of_rounds) if new_number_of_rounds else tournament.number_of_rounds
        )

        tournaments_table = db.table("tournaments")
        tournaments_table.update(
            tournament.serialize(), doc_ids=[tournament_id]
        )

        self.view.print("\nTournament successfully updated.\n")

    def select_tournament(self):
        tournaments_table = db.table("tournaments")
        tournaments_data = tournaments_table.all()

        if not tournaments_data:
            self.view.print("No tournaments available.")
            return None, None

        tournaments = [
            (Tournament(**tournament), tournament.doc_id)
            for tournament in tournaments_data
        ]
        self.view.show_all_tournaments(tournaments)

        self.view.print(
            "Enter the ID of the tournament you want to select :"
        )

        tournament_id = int(self.view.prompt_for_tournament_id())

        tournament_data = tournaments_table.get(doc_id=tournament_id)

        if not tournament_data:
            self.view.print("\nTournament not found.\n")
            return None, None

        # Convert players to Player instances
        players = [Player(**player_data) for player_data in tournament_data["players"]]

        # Convert rounds to Round instances, and matches to Match instances
        rounds = []
        for round_data in tournament_data["rounds"]:
            matches = []
            for match_data in round_data["matches"]:
                player_1_data, player_1_match_score = match_data[0]
                player_2_data, player_2_match_score = match_data[1]

                player_1 = Player(**player_1_data)
                player_2 = Player(**player_2_data)

                match = Match(player_1, player_2, player_1_match_score, player_2_match_score)
                matches.append(match)

            # Convert start_date and end_date to datetime objects
            start_date = datetime.fromisoformat(round_data["start_date"]) if round_data.get("start_date") else None
            end_date = datetime.fromisoformat(round_data["end_date"]) if round_data.get("end_date") else None

            round_instance = Round(
                round_name=round_data["round_name"],
                matches=matches,
                start_date=start_date,
                end_date=end_date
            )
            rounds.append(round_instance)

        tournament = Tournament(
            name=tournament_data["name"],
            location=tournament_data["location"],
            description=tournament_data["description"],
            players=players,
            number_of_rounds=tournament_data["number_of_rounds"],
            current_round_number=tournament_data["current_round_number"],
            rounds=rounds,
            start_date=datetime.fromisoformat(tournament_data["start_date"]) if tournament_data.get("start_date") else None,
            end_date=datetime.fromisoformat(tournament_data["end_date"]) if tournament_data.get("end_date") else None,
            doc_id=tournament_id
        )
        return tournament, tournament_id

    def start_tournament(self):
        # Select a tournament
        tournament, tournament_id = self.select_tournament()
        self.run_tournament(tournament)

    def run_tournament(self, tournament):
        self.view.print(tournament)

        if not tournament.start_date:
            tournament.set_start_date()

        if tournament.end_date:
            self.view.print("Tournament already ended.")
            ranked_players = tournament.get_ranked_players()
            self.view.show_tournament_results(tournament, ranked_players)
            return

        while True:
            # Prompt the user to create a new round
            round_number = int(tournament.current_round_number) + 1

            while True:
                choice = self.view.prompt_for_create_round(round_number)
                if choice == "y":
                    round_instance = tournament.create_round()
                    break
                elif choice == "n":
                    self.view.print(
                        "Round creation cancelled.\n"
                        "Back to Tournaments Menu..."
                    )
                    return
                else:
                    self.view.print("\nInvalid choice! Please try again.")
                    continue

            self.view.show_round_matches(round_instance)

            # Prompt the user to start the round
            while True:
                choice = self.view.prompt_for_start_round(round_instance)
                if choice == "y":
                    tournament.start_current_round()
                    break
                elif choice == "n":
                    self.view.print(
                        "Round start cancelled.\n"
                        "Back to Tournaments Menu..."
                    )
                    return
                else:
                    self.view.print("\nInvalid choice! Please try again.")
                    continue

            self.view.print(f"{round_instance.round_name} started !!!")

            # Prompt the user to enter the results of the matches
            for match in round_instance.matches:
                self.view.show_match(match)
                choice = self.view.prompt_for_match_result()
                # Ajouter vérif
                match.set_result(choice)

            round_instance.end_round()

            self.view.show_round_results(round_instance)

            ranked_players = tournament.get_ranked_players()

            if (tournament.current_round_number ==
                    tournament.number_of_rounds):

                tournament.set_end_date()
                self.view.print("Tournament ended !!!")
                self.view.show_tournament_results(
                    tournament, ranked_players
                )
                tournament.save_tournament()
                return

            self.view.show_ranked_players(ranked_players)
            tournament.save_tournament()
