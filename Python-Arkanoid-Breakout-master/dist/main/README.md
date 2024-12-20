A fun and interactive block-breaking game implemented in Python using Pygame, SQLite3, and Tkinter. This project includes a user login system, high score tracking, and a visually appealing gameplay experience.

Features

User Registration and Login:

Register new users with unique usernames.

Secure login functionality with password validation.

Game Mechanics:

Control a paddle to bounce a ball and destroy blocks.

Dynamic gameplay with score tracking.

High Score System:

Tracks and displays user high scores.

Updates records in a database after each game.

Leaderboards:

View the top scores of all users.

Graphical Interface:

Tkinter-based UI for registration and login.

Pygame-based interface for the game.

Getting Started

Prerequisites

Make sure you have Python installed on your machine. You will also need the following Python libraries:

Pygame

Tkinter (comes pre-installed with Python)

SQLite3 (comes pre-installed with Python)

You can install Pygame using pip:

pip install pygame

Installation

Clone the repository:

git clone <repository-url>
cd <repository-folder>

Run the application by executing the main.py file:

python main.py

File Overview

main.py

Entry point of the application.

Allows users to either register or log in.

game.py

Implements the main game logic using Pygame.

Features include:

Block-breaking mechanics.

High score updates.

Leaderboard display.

log.py

Provides a login interface using Tkinter.

Verifies user credentials.

Redirects to the game upon successful login.

reg.py

Facilitates new user registration using Tkinter.

Validates unique usernames.

Saves user credentials to a SQLite database.

How to Play

Register or Log In:

Start the application (main.py).

Register a new account or log in with existing credentials.

Game Controls:

Use the left and right arrow keys to move the paddle.

Bounce the ball to break blocks and earn points.

Winning and Losing:

The game ends when you miss the ball or destroy all blocks.

Your high score is updated if you achieve a new personal best.

Database Structure

The project uses an SQLite3 database (users.db) with the following schema:

Users Table:

id (Primary Key)

username (Unique)

password

high_score

Future Enhancements

Add levels with increasing difficulty.

Introduce power-ups and special effects.

Implement a multiplayer mode.

Credits

This project was developed as a demonstration of Python programming skills, integrating multiple libraries for a cohesive application.