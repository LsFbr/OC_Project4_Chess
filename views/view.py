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
        name = input("Enter the tournament's name: ")
        location = input("Enter the tournament's location: ")
        description = input("Enter the tournament's description: ")
        number_of_rounds = input("Enter the number of rounds: ")

        return name, location, description, number_of_rounds

    def show_all_players(self, players):
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

        print(table)

    def show_round_matches(self, round):
        print(f"{round}")
        for match in round.matches:
            print(f"{match}")

    def print(self, data):
        print(f"\n{data}")
