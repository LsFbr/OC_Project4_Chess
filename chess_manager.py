from controllers.main_controller import Controller


def main():
    controller = Controller()
    try:
        controller.run()
    except KeyboardInterrupt:
        print("\n\nProgram terminated by user. Goodbye!")
        exit(0)


if __name__ == "__main__":
    main()
