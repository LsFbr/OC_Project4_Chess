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
        """
        Initialize the Controller with a View instance.
        """
        self.view = View()
        self.tournament = None

    def run(self):
        """
        Start the application by displaying the welcome message and main menu.
        """
        self.view.welcome()
        self.main_menu()

    def main_menu(self):
        """
        Display the main menu and handle user input.
        """
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
        """
        Display the players menu and handle user input.
        """
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
        """
        Display the tournaments menu and handle user input.
        """
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
        """
        Display the reports menu and handle user input.
        """
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
        """
        Display the tournament edit menu and handle user input.

        :param tournament: The tournament instance to edit.
        :param tournament_id: The ID of the tournament in the database.
        """
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
        """
        Display the details of a selected tournament instance.
        """
        tournament, tournament_id = self.select_tournament()
        if tournament:
            self.view.show_tournament_details(tournament)

    def report_tournament_players(self):
        """
        Display the players of a selected tournament instance.
        """
        tournament, tournament_id = self.select_tournament()
        if tournament:
            sorted_tournament = self.sort_tournament_players(tournament)
            self.view.show_all_tournament_players(sorted_tournament.players)

    def report_tournament_rounds_and_matches(self):
        """
        Display all rounds and matches of a selected tournament instance.
        """
        tournament, tournament_id = self.select_tournament()
        if tournament and tournament.rounds:
            self.view.show_all_rounds(tournament, tournament.rounds)

    def db_show_all_players(self):
        """
        Display all players sorted alphabetically.
        """
        self.db_sort_players_alphabetically()

        players_table = db.table("players")
        players_data = players_table.all()

        if not players_data:
            self.view.print("No players available.")
            return

        players = [Player(**player) for player in players_data]
        self.view.show_all_players(players)

    def db_add_players(self):
        """
        Add new players to the database in the "players" table.
        """
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
        """
        Edit an existing player's information in the database in the
        "players" table.
        """
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
            new_national_chess_id
            if new_national_chess_id
            else player.national_chess_id
        )

        # Update the player in the database using serialize()
        players_table.update(
            player.serialize(), Query().national_chess_id == national_chess_id
        )

        self.view.print("\nPlayer successfully updated.\n")

    def sort_tournament_players(self, tournament):
        """
        Sort players in a tournament by name (ascending).

        :param tournament: The tournament instance whose players are to be sorted.
        :return: The updated tournament.
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
        Sort players alphabetically by name and surname in the "players" table
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
        """
        Display all tournaments from the "tournaments" table in the database.
        """
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
        """
        Create a new tournament and save it to the database.
        """
        name, location, description, number_of_rounds = self.get_tournament_info()
        selected_players = self.select_tournament_players()

        self.tournament = Tournament(
            name, location, description, selected_players, number_of_rounds
        )

        self.tournament = self.sort_tournament_players(self.tournament)
        self.save_tournament_to_db()
        self.view.print("\nTournament saved.\n")

    def get_tournament_info(self):
        """
        Prompt the user for tournament information.

        :return: Tuple containing tournament name, location, description, and
                 number of rounds.
        """
        name, location, description, number_of_rounds = (
            self.view.prompt_for_tournament()
        )

        if not number_of_rounds:
            number_of_rounds = 4
        else:
            number_of_rounds = int(number_of_rounds)

        return name, location, description, number_of_rounds

    def select_tournament_players(self):
        """
        Select players for the tournament from the database.

        :return: List of selected Player instances.
        """
        players_table = db.table("players")
        players_data = players_table.all()

        players = [Player(**player) for player in players_data]
        self.view.show_all_players(players)

        national_chess_ids = self.view.prompt_for_add_tournament_players()
        national_chess_ids_list = [
            chess_id.strip() for chess_id in national_chess_ids.split(",")
        ]

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

        return selected_players

    def save_tournament_to_db(self):
        """
        Save the current tournament to the database.
        """
        tournaments_table = db.table("tournaments")
        tournaments_table.insert(self.tournament.serialize())
        self.tournament = None

    def add_tournament_players(self, tournament, tournament_id):
        """
        Add players from the "players" table in the database to an existing
        tournament.

        :param tournament: The tournament instance to which players are to be
        added.
        :param tournament_id: The ID of the tournament in the database.
        """
        self.view.show_all_tournament_players(tournament.players)

        players_table = db.table("players")
        players_data = players_table.all()

        self.view.show_all_players(
            [Player(**player) for player in players_data]
        )

        national_chess_ids = self.view.prompt_for_add_tournament_players()
        national_chess_ids_list = [
            chess_id.strip() for chess_id in national_chess_ids.split(",")
        ]

        existing_ids = {
            player.national_chess_id for player in tournament.players
        }

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

        tournament = self.sort_tournament_players(tournament)

        tournaments_table = db.table("tournaments")
        tournaments_table.update(
            tournament.serialize(), doc_ids=[tournament_id]
        )

        self.view.print("\nTournament successfully updated.")

    def remove_tournament_players(self, tournament, tournament_id):
        """
        Remove players from an existing tournament in the "tournaments" table
        in the database.

        :param tournament: The tournament instance from which players are to be
        removed.
        :param tournament_id: The ID of the tournament in the database.
        """
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
        """
        Edit an existing tournament's information.
        """
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
        """
        Edit the information of a tournament.

        :param tournament: The tournament instance to edit.
        :param tournament_id: The ID of the tournament in the database.
        """
        self.view.show_tournament_infos(tournament)

        new_name, new_location, new_description, new_number_of_rounds = (
            self.view.prompt_for_edit_tournament_infos()
        )

        tournament.name = new_name if new_name else tournament.name
        tournament.location = (
            new_location if new_location else tournament.location
        )
        tournament.description = (
            new_description if new_description else tournament.description
        )
        tournament.number_of_rounds = (
            int(new_number_of_rounds) if new_number_of_rounds
            else tournament.number_of_rounds
        )

        tournaments_table = db.table("tournaments")
        tournaments_table.update(
            tournament.serialize(), doc_ids=[tournament_id]
        )

        self.view.print("\nTournament successfully updated.\n")

    def select_tournament(self):
        """
        Select a tournament from the database.

        :return: The selected tournament instance and its ID.
        """
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

        self.view.print("Enter the ID of the tournament you want to select :")
        tournament_id = int(self.view.prompt_for_tournament_id())

        tournament_data = tournaments_table.get(doc_id=tournament_id)

        if not tournament_data:
            self.view.print("\nTournament not found.\n")
            return None, None

        players = self._convert_players(tournament_data["players"])
        rounds = self._convert_rounds(tournament_data["rounds"])

        tournament = Tournament(
            name=tournament_data["name"],
            location=tournament_data["location"],
            description=tournament_data["description"],
            players=players,
            number_of_rounds=tournament_data["number_of_rounds"],
            current_round_number=tournament_data["current_round_number"],
            rounds=rounds,
            start_date=(
                datetime.fromisoformat(tournament_data["start_date"])
                if tournament_data.get("start_date")
                else None
            ),
            end_date=(
                datetime.fromisoformat(tournament_data["end_date"])
                if tournament_data.get("end_date")
                else None
            ),
            doc_id=tournament_id
        )
        return tournament, tournament_id

    def _convert_players(self, players_data):
        """
        Convert player data to Player instances.

        :param players_data: List of player data dictionaries.
        :return: List of Player instances.
        """
        return [Player(**player_data) for player_data in players_data]

    def _convert_rounds(self, rounds_data):
        """
        Convert round data to Round instances.

        :param rounds_data: List of round data dictionaries.
        :return: List of Round instances.
        """
        rounds = []
        for round_data in rounds_data:
            matches = self._convert_matches(round_data["matches"])
            start_date = (
                datetime.fromisoformat(round_data["start_date"])
                if round_data.get("start_date")
                else None
            )
            end_date = (
                datetime.fromisoformat(round_data["end_date"])
                if round_data.get("end_date")
                else None
            )
            round_instance = Round(
                round_name=round_data["round_name"],
                matches=matches,
                start_date=start_date,
                end_date=end_date
            )
            rounds.append(round_instance)
        return rounds

    def _convert_matches(self, matches_data):
        """
        Convert match data to Match instances.

        :param matches_data: List of match data dictionaries.
        :return: List of Match instances.
        """
        matches = []
        for match_data in matches_data:
            player_1_data = match_data[0][0]["player_1"]
            player_1_match_score = match_data[0][0]["player_1_match_score"]
            player_2_data = match_data[1][0]["player_2"]
            player_2_match_score = match_data[1][0]["player_2_match_score"]

            player_1 = Player(**player_1_data)
            player_2 = Player(**player_2_data)

            match = Match(
                player_1,
                player_2,
                player_1_match_score,
                player_2_match_score
            )
            matches.append(match)
        return matches

    def start_tournament(self):
        """
        Start a selected tournament instance.
        """
        tournament, tournament_id = self.select_tournament()
        self.run_tournament(tournament)

    def run_tournament(self, tournament):
        """
        Run the tournament by managing rounds and matches.

        :param tournament: The tournament instance to run.
        """
        self.view.print(tournament)

        if not tournament.start_date:
            tournament.set_start_date()

        if tournament.end_date:
            self._handle_tournament_end(tournament)
            return

        while True:
            round_instance = self._create_new_round(tournament)
            if not round_instance:
                return

            self._start_round(tournament, round_instance)
            self._enter_match_results(round_instance)

            round_instance.end_round()
            self.view.show_round_results(round_instance)

            ranked_players = tournament.get_ranked_players()

            if tournament.current_round_number == tournament.number_of_rounds:
                self._finalize_tournament(tournament, ranked_players)
                return

            self.view.show_ranked_players(ranked_players)
            tournament.save_tournament()

    def _handle_tournament_end(self, tournament):
        """
        Handle the end of a tournament.

        :param tournament: The tournament instance.
        """
        self.view.print("Tournament already ended.")
        ranked_players = tournament.get_ranked_players()
        self.view.show_tournament_results(tournament, ranked_players)

    def _create_new_round(self, tournament):
        """
        Prompt the user to create a new round.

        :param tournament: The tournament instance.
        :return: The created round instance or None if cancelled.
        """
        round_number = int(tournament.current_round_number) + 1

        while True:
            choice = self.view.prompt_for_create_round(round_number)
            if choice == "y":
                return tournament.create_round()
            elif choice == "n":
                self.view.print(
                    "Round creation cancelled.\n"
                    "Back to Tournaments Menu..."
                )
                return None
            else:
                self.view.print("\nInvalid choice! Please try again.")

    def _start_round(self, tournament, round_instance):
        """
        Start the current round of the tournament.

        :param tournament: The tournament instance.
        :param round_instance: The round instance to start.
        """
        self.view.show_round_matches(round_instance)

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

        self.view.print(f"{round_instance.round_name} started !!!")

    def _enter_match_results(self, round_instance):
        """
        Prompt the user to enter the results of the matches.

        :param round_instance: The round instance.
        """
        for match in round_instance.matches:
            self.view.show_match(match)
            choice = self.view.prompt_for_match_result()
            match.set_result(choice)

    def _finalize_tournament(self, tournament, ranked_players):
        """
        Finalize the tournament and display results.

        :param tournament: The tournament instance.
        :param ranked_players: The list of ranked players.
        """
        tournament.set_end_date()
        self.view.print("Tournament ended !!!")
        self.view.show_tournament_results(tournament, ranked_players)
        tournament.save_tournament()
