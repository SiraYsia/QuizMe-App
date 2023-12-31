# QuizMe - Flashcard Generator

QuizMe is a full-stack web application that dynamically generates personalized flashcards from study materials, saving valuable time and effort for users in creating effective study aids. The project leverages GPT-3.5 Turbo for intelligent flashcard generation and offers various features to enhance the user experience.

## Table of Contents
- [Features](#features)
- [Getting Started](#getting-started)
- [Dependencies](#dependencies)
- [Installation](#installation)
- [Usage](#usage)

## Features

- Dynamically generates personalized flashcards from study materials using GPT-3.5 Turbo.
- Implements Flask and SQLAlchemy for a robust backend, efficiently managing the SQLite database with bcrypt-based user authentication.
- Provides a user-friendly frontend with HTML, CSS, and JavaScript for an intuitive and seamless user experience.
- Enables users to access flashcards through a web browser 
- Tracks user progress to monitor study performance and identify areas for improvement.

## Getting Started

To get started with QuizMe, follow the steps below:

1. Clone this repository to your local machine.
2. Ensure you have the required dependencies installed (see [Dependencies](#dependencies)).
3. Run the application using `python run.py` in your terminal.
4. Access the application at http://127.0.0.1:5000/ in your web browser.

Alternatively, you can visit the currently deployed site at http://quizmeapp.pythonanywhere.com/. Please note that the site is still a work in progress, and many more existing features are yet to come.

**Please Note:** The flashcard generation process may take a few moments to format the output correctly. If you encounter empty flashcards after clicking on "Create Flashcards" and specifying the number of flashcards, simply try the process again. Rest assured, this is a normal part of the system's operation, and your flashcards will be generated successfully with a slight delay. We are continuously working to improve the flashcard generation process to make it even more seamless and efficient for our users. !





## Dependencies

- Flask
- Flask_SQLAlchemy
- bcrypt
- apy (for GPT-3.5 Turbo integration)

## Installation

1. Install Python on your system if you haven't already.
2. Clone this repository to your local machine using `git clone https://github.com/yourusername/QuizMe.git`.
3. Change into the project directory: `cd QuizMe`.
4. Install the required dependencies using `pip install -r requirements.txt`.
5. run run.py and follow the prompt 

## Usage

- Visit the QuizMe app homepage to create personalized flashcards.
- Log in or sign up to save and access your flashcard sets.
- Use the "Get Started" option to generate flashcards from study materials.
- Choose to append new flashcards to existing sets or create new sets.
- Access your flashcards from the "Your Flashcards" page.


