class View:
    def welcome(self):
        print("Welcome to the chess tournament manager!")

    def prompt_for_player(self):
        name = input("Enter the player's name: ")
        if not name:
            return None, None, None, None
        surname = input("Enter the player's surname: ")
        birthday = input("Enter the player's birthday: ")
        national_chess_id = input("Enter the player's national chess ID: ")

        return name, surname, birthday, national_chess_id

    def prompt_for_tournament(self):
        name = input("Enter the tournament's name: ")
        location = input("Enter the tournament's location: ")
        description = input("Enter the tournament's description: ")
        number_of_rounds = input("Enter the number of rounds: ")

        return name, location, description, number_of_rounds

    def print(self, data):
        print(data)
