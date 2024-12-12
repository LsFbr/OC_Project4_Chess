from .utils import format_date

from prettytable import PrettyTable


class View:
    def display_menu(self, title, options):
        """
        Display a menu and return the choice
        title: str
        options: dict
        """
        print(f"\n<<<{title}>>>")
        for key, value in options.items():
            print(f"Enter {key} to {value}")
        return input("Enter your choice : ")

    def welcome(self):
        """
        Display the welcome message.
        """
        print("\n<<<Welcome to the chess tournament manager>>>")

    def main_menu(self):
        """
        Display the main menu and return the user's choice.

        :return: The user's choice.
        """
        options = {
            "1": "access the Players Menu",
            "2": "access the Tournaments Menu",
            "3": "access the Reports Menu",
            "0": "quit"
        }
        return self.display_menu("Main Menu", options)

    def players_menu(self):
        """
        Display the players menu and return the user's choice.

        :return: The user's choice.
        """
        options = {
            "1": "display all players",
            "2": "add a player",
            "3": "edit a player",
            "0": "return to main menu"
        }
        return self.display_menu("Players Menu", options)

    def tournaments_menu(self):
        """
        Display the tournaments menu and return the user's choice.

        :return: The user's choice.
        """
        options = {
            "1": "display all tournaments",
            "2": "create a tournament",
            "3": "edit a tournament",
            "4": "start a tournament",
            "0": "return to main menu"
        }
        return self.display_menu("Tournaments Menu", options)

    def reports_menu(self):
        """
        Display the reports menu and return the user's choice.

        :return: The user's choice.
        """
        options = {
            "1": "display all players (alphabetically)",
            "2": "display all tournaments",
            "3": "display tournament details (name and dates)",
            "4": "display players of a tournament (alphabetically)",
            "5": "display all rounds and matches of a tournament",
            "0": "return to main menu"
        }
        return self.display_menu("Reports Menu", options)

    def tournament_edit_menu(self):
        """
        Display the tournament edit menu and return the user's choice.

        :return: The user's choice.
        """
        options = {
            "1": "display tournament information and players",
            "2": "edit tournament information",
            "3": "add players to the tournament",
            "4": "remove players from the tournament",
            "0": "return to tournament menu"
        }
        return self.display_menu("Tournament Edit Menu", options)

    def prompt_for_add_tournament_players(self):
        """
        Prompt the user to add players to the tournament.

        :return: A comma-separated string of player IDs.
        """
        print("\n<<<Add players to the tournament>>>")
        national_chess_ids = input(
            "Enter the players National Chess ID, comma separated: "
        )
        return national_chess_ids

    def prompt_for_remove_tournament_players(self):
        """
        Prompt the user to remove players from the tournament.

        :return: A comma-separated string of player IDs.
        """
        print("\n<<<Delete players from the tournament>>>")
        national_chess_ids = input(
            "Enter the players National Chess ID, comma separated: "
        )
        return national_chess_ids

    def show_tournament_infos(self, tournament):
        """
        Display the information of a tournament.

        :param tournament: The tournament instance to display.
        """
        table = PrettyTable()
        table.title = "<<<Tournament Informations>>>"
        table.field_names = [
            "Name", "Location", "Description", "Current Round", "Players"
        ]

        table.add_row([
            tournament.name,
            tournament.location,
            tournament.description,
            f"{tournament.current_round_number}/{tournament.number_of_rounds}",
            len(tournament.players)
        ])

        print(f"\n{table}")

    def show_tournament_details(self, tournament):
        """
        Display the details of a tournament.

        :param tournament: The tournament instance to display.
        """
        table = PrettyTable()
        table.title = "<<<Tournament Details>>>"
        table.field_names = ["Name", "Start Date", "End Date"]

        table.add_row([
            tournament.name,
            format_date(tournament.start_date)
            if tournament.start_date
            else "Not started yet",
            format_date(tournament.end_date)
            if tournament.end_date
            else "Not finished yet"
        ])

        print(f"\n{table}")

    def show_all_tournaments(self, tournaments):
        """
        Display all tournaments.

        :param tournaments: A list of tournament instances to display.
        """
        if not tournaments:
            print("\nNo tournaments available.")
            return

        table = PrettyTable()
        table.title = "<<<Tournaments List>>>"
        table.field_names = [
            "ID", "Name", "Location", "Description", "Current Round",
            "Players", "Start Date", "End Date"
        ]

        for tournament, doc_id in tournaments:
            table.add_row([
                doc_id,
                tournament.name,
                tournament.location,
                tournament.description,

                f"{tournament.current_round_number}/"
                f"{tournament.number_of_rounds}",

                len(tournament.players),

                format_date(tournament.start_date)
                if tournament.start_date
                else "Not started yet",

                format_date(tournament.end_date)
                if tournament.end_date
                else "Not finished yet"
            ])

        print(f"\n{table}")

    def prompt_for_edit_tournament_infos(self):
        """
        Prompt the user to edit tournament information.

        :return: A tuple containing the new tournament information.
        """
        print(
            "\nEnter new tournament's informations"
            " or press enter to keep the current one"
        )
        name = input("Name: ")
        location = input("Location: ")
        description = input("Description: ")
        number_of_rounds = input("Number of rounds: ")
        return name, location, description, number_of_rounds

    def prompt_for_add_player(self):
        """
        Prompt the user to add a new player.

        :return: A tuple containing the player's information.
        """
        print("\nEnter the player's informations")
        name = input("Name: ")
        surname = input("Surname: ")
        birthday = input("Birthday: ")
        national_chess_id = input("National chess ID: ")
        return name, surname, birthday, national_chess_id

    def prompt_for_add_another_player(self):
        """
        Prompt the user to add another player.

        :return: True if the user wants to add another player, False otherwise.
        """
        print("\nDo you want to add another player?")
        result = input("Enter 'y' to add another player or 'n' to continue: ")
        if result == 'y':
            return True
        return False

    def prompt_for_tournament(self):
        """
        Prompt the user to create a new tournament.

        :return: A tuple containing the tournament's information.
        """
        print("\n<<<Tournament creation>>>")
        name = input("Enter the tournament's name: ")
        location = input("Enter the tournament's location: ")
        description = input("Enter the tournament's description: ")
        number_of_rounds = input("Enter the number of rounds: ")

        return name, location, description, number_of_rounds

    def show_player(self, player):
        """
        Display the information of a player.

        :param player: The player instance to display.
        """
        table = PrettyTable()
        table.title = "<<<Player Information>>>"
        table.field_names = [
            "Name", "Surname", "Birthday", "National Chess ID"
        ]

        table.add_row([
            player.name,
            player.surname,
            player.birthday,
            player.national_chess_id
        ])

        print(f"\n{table}")

    def show_all_tournament_players(self, players):
        """
        Display all players in a tournament.

        :param players: A list of player instances to display.
        """
        if not players:
            print("\nNo players in the tournament.")
            return

        table = PrettyTable()
        table.title = "<<<Tournament's Players>>>"
        table.field_names = [
            "National Chess ID", "Name", "Surname", "Birthday", "Score"
        ]

        for player in players:
            table.add_row([
                player.national_chess_id,
                player.name,
                player.surname,
                player.birthday,
                player.score
            ])

        print(f"\n{table}")

    def show_tournament_results(self, tournament_instance, ranked_players):
        """
        Display the final ranking of a tournament.

        :param tournament_instance: The tournament instance.
        :param ranked_players: A list of ranked player instances.
        """
        table = PrettyTable()
        table.title = (f"<<<{tournament_instance.name} - Final Ranking>>>")
        table.field_names = [
            "Rank", "National Chess ID", "Name", "Surname", "Score"
        ]

        for rank, player in enumerate(ranked_players, start=1):
            table.add_row([
                rank,
                player.national_chess_id,
                player.name,
                player.surname,
                player.score
            ])

        print(f"\n{table}")
        print(
            f"    Start date: {format_date(
                str(tournament_instance.start_date)
            )}\n"
            f"    End date: {format_date(
                str(tournament_instance.end_date)
            )}"
        )

    def show_ranked_players(self, ranked_players):
        """
        Display the ranking of players in a tournament.

        :param ranked_players: A list of ranked player instances.
        """
        table = PrettyTable()
        table.title = "<<<Tournament Ranking>>>"
        table.field_names = [
            "Rank", "National Chess ID", "Name", "Surname", "Score"
        ]

        for rank, player in enumerate(ranked_players, start=1):
            table.add_row([
                rank,
                player.national_chess_id,
                player.name,
                player.surname,
                player.score
            ])

        print(f"\n{table}")

    def show_all_players(self, players):
        """
        Display all registered players.

        :param players: A list of player instances to display.
        """
        if not players:
            print("\nNo players available.")
            return

        table = PrettyTable()
        table.title = "<<<Registered Players>>>"
        table.field_names = [
            "National Chess ID", "Name", "Surname", "Birthday"
        ]

        for player in players:
            table.add_row([
                player.national_chess_id,
                player.name,
                player.surname,
                player.birthday
            ])

        print(f"\n{table}")

    def prompt_for_edit_player(self):
        """
        Prompt the user to edit a player's information.

        :return: A tuple containing the new player's information.
        (name, surname, birthday, national_chess_id)
        """
        print(
            "\nEnter new player's informations"
            " or press enter to keep the current one")
        name = input("Name: ")
        surname = input("Surname: ")
        birthday = input("Birthday: ")
        national_chess_id = input("National chess ID: ")
        return name, surname, birthday, national_chess_id

    def prompt_for_tournament_id(self):
        """
        Prompt the user to enter a tournament ID.

        :return: The tournament ID.
        """
        tournament_id = input(
            "Your choice :"
        )
        return tournament_id

    def prompt_for_chess_id(self):
        """
        Prompt the user to enter a chess ID.

        :return: The chess ID.
        """
        national_chess_id = input(
            "Your choice :"
        )
        return national_chess_id

    def show_round_matches(self, round_instance):
        """
        Display the matches of a round.

        :param round_instance: The round instance.
        """
        table = PrettyTable()
        table.title = f"<<<{round_instance.round_name}>>>"
        table.field_names = ["Player 1", "Score", "Player 2"]

        for match in round_instance.matches:
            table.add_row([
                f"{match.player_1.name} {match.player_1.surname}",
                f"{match.player_1_match_score}|{match.player_2_match_score}",
                f"{match.player_2.name} {match.player_2.surname}"
            ])
        print(f"\n{table}")

    def show_match(self, match_instance):
        """
        Display a match.

        :param match_instance: The match instance.
        """
        table = PrettyTable()
        table.field_names = ["Player 1", "Player 2"]
        table.add_row([
            f"{match_instance.player_1.name} "
            f"{match_instance.player_1.surname}",

            f"{match_instance.player_2.name} "
            f"{match_instance.player_2.surname}"
        ])
        print(f"\n{table}")

    def show_all_rounds(self, tournament, rounds):
        """
        Display all rounds of a tournament.

        :param tournament: The tournament instance.
        :param rounds: A list of round instances to display.
        """
        table = PrettyTable()
        table.title = (
            f"<<<{tournament.name} - Rounds List - "
            f"{tournament.current_round_number}/"
            f"{tournament.number_of_rounds}>>>"
        )
        table.field_names = ["Round", "Dates", "Matches"]

        for round_instance in rounds:
            matches_table = PrettyTable()
            matches_table.field_names = ["Player 1", "Score", "Player 2"]
            matches_table.align["Player 1"] = "r"
            matches_table.align["Score"] = "c"
            matches_table.align["Player 2"] = "l"
            for match in round_instance.matches:
                matches_table.add_row([
                    f"({match.player_1.national_chess_id}) "
                    f"{match.player_1.name} {match.player_1.surname}",

                    f"{match.player_1_match_score} | "
                    f"{match.player_2_match_score}",

                    f"{match.player_2.name} {match.player_2.surname} "
                    f"({match.player_2.national_chess_id})"
                ])

            matches_str = matches_table.get_string()

            table.add_row([
                round_instance.round_name,
                f"Started: {format_date(str(round_instance.start_date))}\n"
                f"Ended: {format_date(str(round_instance.end_date))}",
                matches_str,
            ])
            table.add_row([
                "---------",
                "------------------------------",
                "-------------------------------------------------------------"
                "--------"
            ])

        print(f"\n{table}")

    def show_round_results(self, round_instance):
        """
        Display the results of a round.

        :param round_instance: The round instance.
        """
        table = PrettyTable()
        table.title = (f"<<<{round_instance.round_name} results>>>")
        table.field_names = ["Player 1", "Score", "Player 2"]

        for match in round_instance.matches:
            table.add_row([
                f"{match.player_1.name} {match.player_1.surname}",
                f"{match.player_1_match_score}|{match.player_2_match_score}",
                f"{match.player_2.name} {match.player_2.surname}"
            ])
        print(f"\n{table}")
        print(
            f"    Start date: {format_date(str(round_instance.start_date))}\n"
            f"    End date: {format_date(str(round_instance.end_date))}"
        )

    def prompt_for_match_result(self):
        """
        Prompt the user to enter the result of a match.

        :return: The choice of the match result.
        """
        print(
            "Enter the result of the match\n"
            "Enter 1 if Player 1 wins\n"
            "Enter 2 if Player 2 wins\n"
            "Enter 0 for a draw"
        )
        choice = input("Your choice : ")
        return choice

    def prompt_for_create_round(self, round_number):
        """
        Prompt the user to create a new round.

        :param round_number: The number of the round to create.
        :return: The user's choice.
        """
        print(
            f"\nAre you ready to create matches for Round {round_number}?\n"
            "Enter 'y' to continue or 'n' to return to tournaments menu"
        )
        return input("Your choice : ").lower()

    def prompt_for_start_round(self, round_instance):
        """
        Prompt the user to start a round.

        :param round_instance: The round instance.
        :return: The user's choice.
        """
        print(
            f"Are you ready to start {round_instance.round_name}?\n"
            "Enter 'y' to continue or 'n' to return to tournaments menu"
        )
        return input("Your choice : ").lower()

    def print(self, data):
        """
        Print data to the console.

        :param data: The data to print.
        """
        print(f"\n{data}")
