from prettytable import PrettyTable


class View:
    def welcome(self):
        print("\n<<<Welcome to the chess tournament manager>>>")

    def main_menu(self):
        print("\n<<<Main Menu>>>")
        print("Enter 1 for Players Menu")
        print("Enter 2 for Tournaments Menu")
        print("Enter 0 to quit")
        return input("Enter your choice : ")

    def players_menu(self):
        print("\n<<<Players Menu>>>")
        print("Enter 1 to show all players")
        print("Enter 2 to add a player")
        print("Enter 3 to edit a player")
        print("Enter 0 to return to the main menu")
        return input("Enter your choice : ")

    def tournaments_menu(self):
        print("\n<<<Tournaments Menu>>>")
        print("Enter 1 to show all tournaments")
        print("Enter 2 to create a tournament")
        print("Enter 3 to edit a tournament")
        print("Enter 4 to start a tournament")
        print("Enter 0 to return to the main menu")
        return input("Enter your choice : ")

    def tournament_edit_menu(self):
        print("\n<<<Tournament Edit Menu>>>")
        print("Enter 1 to show tournament informations and players")
        print("Enter 2 to edit tournament informations")
        print("Enter 3 to add players to the tournament")
        print("Enter 4 to remove players from the tournament")
        print("Enter 0 to return to the tournament menu")
        return input("Enter your choice : ")

    def prompt_for_add_tournament_players(self):
        print("\n<<<Add players to the tournament>>>")
        national_chess_ids = input(
            "Enter the players National Chess ID, comma separated: "
        )
        return national_chess_ids

    def prompt_for_remove_tournament_players(self):
        print("\n<<<Delete players from the tournament>>>")
        national_chess_ids = input(
            "Enter the players National Chess ID, comma separated: "
        )
        return national_chess_ids

    def show_tournament_infos(self, tournament):
        table = PrettyTable()
        table.title = "<<<Tournament Informations>>>"
        table.field_names = [
            "Name", "Location", "Description", "Current Round", "Players"
        ]

        table.add_row([
            tournament["name"],
            tournament["location"],
            tournament["description"],
            (
                f"{tournament['current_round_number']}/"
                f"{tournament['number_of_rounds']}"
            ),
            len(tournament["players"])
        ])

        print(table)

    def show_all_tournaments(self, tournaments):
        if not tournaments:
            print("\nNo tournaments available.")
            return

        table = PrettyTable()
        table.title = "<<<Tournaments List>>>"
        table.field_names = [
            "ID", "Name", "Location", "Description", "Current Round", "Players"
        ]

        for tournament in tournaments:
            table.add_row([
                tournament.doc_id,
                tournament["name"],
                tournament["location"],
                tournament["description"],
                (
                    f"{tournament['current_round_number']}/"
                    f"{tournament['number_of_rounds']}"
                ),
                len(tournament["players"])
            ])

        print(table)

    def prompt_for_edit_tournament_infos(self):
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
        print("\nEnter the player's informations")
        name = input("Name: ")
        surname = input("Surname: ")
        birthday = input("Birthday: ")
        national_chess_id = input("National chess ID: ")
        return name, surname, birthday, national_chess_id

    def prompt_for_add_another_player(self):
        print("\nDo you want to add another player?")
        result = input("Enter 'y' to add another player or 'n' to continue: ")
        if result == 'y':
            return True
        return False

    def prompt_for_tournament(self):
        print("\n<<<Tournament creation>>>")
        name = input("Enter the tournament's name: ")
        location = input("Enter the tournament's location: ")
        description = input("Enter the tournament's description: ")
        number_of_rounds = input("Enter the number of rounds: ")

        return name, location, description, number_of_rounds

    def show_player(self, player):
        print("\n<<<Player Informations>>>")
        print(f"Name: {player['name']}")
        print(f"Surname: {player['surname']}")
        print(f"Birthday: {player['birthday']}")
        print(f"National Chess ID: {player['national_chess_id']}")

    def show_all_tournament_players(self, players):
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
                player["national_chess_id"],
                player["name"],
                player["surname"],
                player["birthday"],
                player["score"]
            ])

        print(table)

    def show_all_players(self, players):
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
                player["national_chess_id"],
                player["name"],
                player["surname"],
                player["birthday"]
            ])

        print(table)

    def prompt_for_edit_player(self):
        print(
            "\nEnter new player's informations"
            " or press enter to keep the current one")
        name = input("Name: ")
        surname = input("Surname: ")
        birthday = input("Birthday: ")
        national_chess_id = input("National chess ID: ")
        return name, surname, birthday, national_chess_id

    def prompt_for_tournament_id(self):
        tournament_id = input(
            "Your choice :"
        )
        return tournament_id

    def prompt_for_chess_id(self):
        national_chess_id = input(
            "Your choice :"
        )
        return national_chess_id

    def show_round_matches(self, round):
        print(f"{round}")
        for match in round.matches:
            print(f"{match}")

    def print(self, data):
        print(f"\n{data}")
