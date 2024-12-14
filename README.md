# OC_Project4_Chess

## Introduction

This project is a chess tournament management software developed as part of the OpenClassrooms Python course. The primary goal of this project is to facilitate the organization and management of chess tournaments, allowing users to create tournaments, manage players, and track match results.

### Features

- **Tournament Management**: 
  - Create new tournaments with specific details such as name, location, and description.
  - Edit existing tournaments to update information or manage participants.
  - Start and manage multiple rounds within a tournament.

- **Player Management**: 
  - Add new players with personal details like name, surname, birthday, and national chess ID.
  - Edit player information to keep records up-to-date.
  - Display a list of all registered players, sorted alphabetically or by tournament participation.

- **Match Tracking**: 
  - Automatically generate matches for each round based on player rankings and previous matchups.
  - Record match results and update player scores accordingly.
  - View detailed match information, including player names and scores.

- **Reports**: 
  - Generate comprehensive reports on tournament details, including start and end dates, and current standings.
  - Display player rankings and scores within a tournament.
  - Provide a historical view of all rounds and matches played in a tournament.

These features are designed to streamline the process of organizing and managing chess tournaments, providing a user-friendly interface for both tournament organizers and participants.

### MVC Structure

The project is structured using the Model-View-Controller (MVC) design pattern:

- **Model**: Handles the data and business logic. It includes classes for players, matches, rounds, and tournaments, and manages data persistence using TinyDB.
- **View**: Manages the user interface and displays information to the user. It includes methods for displaying menus, player and tournament details, and match results.
- **Controller**: Acts as an intermediary between the model and the view. It processes user input, updates the model, and updates the view accordingly.

This structure ensures a clean separation of concerns, making the codebase easier to maintain and extend.

## Deployment

To deploy and run the chess tournament management software, follow these steps for your operating system:

### Prerequisites

- Ensure you have Python 3.8 or later installed on your system. You can download it from [python.org](https://www.python.org/downloads/).

### Deployment Steps

1. **Obtain the Project**:
   You have two options to obtain the project files:
   - **Clone the Repository**: 
     If you choose to clone the repository, ensure Git is installed on your system. You can download it from [git-scm.com](https://git-scm.com/). Then, open a terminal (or Command Prompt on Windows) and run the following command:
     ```bash
     git clone https://github.com/yourusername/OC_Project4_Chess.git
     cd OC_Project4_Chess
     ```
   - **Download as ZIP**:
     Go to the repository on GitHub, click on the "Code" button, and select "Download ZIP". Extract the downloaded ZIP file and navigate into the extracted directory.

2. **Create a Virtual Environment**:
   Create a virtual environment to manage dependencies:
   - On Linux and macOS:
     ```bash
     python3 -m venv venv
     ```
   - On Windows:
     ```bash
     python -m venv venv
     ```

3. **Activate the Virtual Environment**:
   - On Linux and macOS:
     ```bash
     source venv/bin/activate
     ```
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```

4. **Install Dependencies**:
   Install the required packages using pip:
   ```bash
   pip install -r requirements.txt
   ```

5. **Run the Program**:
   Execute the main script to start the application:
   - On Linux and macOS:
     ```bash
     python3 chess_manager.py
     ```
   - On Windows:
     ```bash
     python chess_manager.py
     ```

### Notes

- Ensure that your terminal or command prompt is open in the project directory before running the commands.
- If you encounter any issues with dependencies, ensure that your Python and pip versions are up-to-date.
- To deactivate the virtual environment, simply run `deactivate` in your terminal or command prompt.

## Usage

Once the program is running, you will be greeted with a welcome message and the main menu. The application is designed to be navigated using a simple text-based interface. Here’s a quick guide on how to use the program:

1. **Main Menu**:
   - **Players Menu**: Access options to display, add, or edit player information.
   - **Tournaments Menu**: Manage tournaments by creating new ones, editing existing ones, or starting a tournament.
   - **Reports Menu**: Generate and view reports on players and tournaments.
   - **Quit**: Exit the application.

2. **Navigating Menus**:
   - Enter the number corresponding to the menu option you wish to select.
   - Follow the prompts to input any required information, such as player details or tournament settings.

3. **Managing Players**:
   - Add new players by entering their personal details.
   - Edit existing player information to keep records accurate.

4. **Managing Tournaments**:
   - Create a new tournament by specifying its name, location, and description.
   - Start a tournament to automatically generate matches and track results.

5. **Viewing Reports**:
   - Access detailed reports on tournament standings, player rankings, and match results.

The program is designed to be intuitive and user-friendly, allowing you to efficiently manage chess tournaments and player information.

## Generating a Flake8 Report

To ensure your code adheres to PEP 8 standards and to generate a Flake8 report, follow these steps:

### Prerequisites

- Flake8 and Flake8-HTML are included in the `requirements.txt` file. If you have followed the deployment steps and installed the dependencies, these packages should already be installed in your virtual environment.

### Steps to Generate the Report

1. **Activate the Virtual Environment**:
   - On Linux and macOS:
     ```bash
     source venv/bin/activate
     ```
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```

2. **Run Flake8 with HTML Report Generation**:
   Use the following command to generate the Flake8 report in HTML format:
   ```bash
   flake8 --format=html --htmldir=flake8_rapport
   ```

3. **View the Report**:
   Open the `index.html` file located in the `flake8_rapport` directory with your web browser to view the report.

### Notes

- The `.flake8` configuration file is set to ignore certain directories like `.git`, `__pycache__`, and virtual environments to prevent unnecessary errors.
- Ensure your code is free of errors and warnings to maintain code quality and adhere to PEP 8 standards.