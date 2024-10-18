class View:
    def welcome(self):
        print("Welcome to the chess tournament manager!")

    def main_menu(self):
        print("[1]. Create a tournament")
        print("[2]. Add players")
        print("[3]. Start tournament")
        print("[0]. Exit")
        return input("Enter your choice : ")

    def prompt_for_add_player(self):
        print("Enter the player's informations")
        name = input("Name: ")
        surname = input("Surname: ")
        birthday = input("Birthday: ")
        national_chess_id = input("National chess ID: ")
        return name, surname, birthday, national_chess_id

    def prompt_for_add_another_player(self):
        print("Do you want to add another player?")
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

    def print(self, data):
        print(data)
