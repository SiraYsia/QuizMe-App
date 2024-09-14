# QuizMe - Flashcard Generator

QuizMe is a full-stack web application that dynamically generates personalized flashcards from study materials, saving valuable time and effort for users in creating effective study aids. The project leverages google gemin Turbo for intelligent flashcard generation and offers various features to enhance the user experience. You can access it here http://quizmeapp.pythonanywhere.com/ 

## Table of Contents
- [Features](#features)
- [Getting Started](#getting-started)
- [Dependencies](#dependencies)
- [Installation](#installation)
- [Usage](#usage)


## Features

- **Personalized Flashcard Generation:** Dynamically generates personalized flashcards from study materials using the Google Gemini API.
- **Unlimited Flashcards:** Allows users to create and manage an unlimited number of flashcards.
- **Star and Bookmark Flashcards:** Enables users to star and bookmark flashcards for easy access and review.
- **User Authentication:** Provides secure login functionality using bcrypt-based user authentication.
- **Account-Based Storage:** Stores all generated flashcards in the user’s account, allowing users to access and manage their flashcards upon returning.
- **Robust Backend:** Implements Flask and SQLAlchemy for a robust backend, efficiently managing the SQLite database.
- **User-Friendly Frontend:** Offers a seamless user experience with a frontend built using HTML, CSS, and JavaScript.
- **Web Browser Access:** Allows users to access and interact with flashcards through a web browser.
- **Progress Tracking:** Tracks user progress to monitor study performance and identify areas for improvement.

You can access the application here: [QuizMe](http://quizmeapp.pythonanywhere.com/)


## Getting Started

To get started with QuizMe, follow the steps below:

1. Clone this repository to your local machine.
2. Ensure you have the required dependencies installed (see [Installation](#installation)).
3. Run the application using `python app.py` in your terminal.
4. Access the application at http://127.0.0.1:5000/ in your web browser.

Alternatively, you can visit the currently deployed site at http://quizmeapp.pythonanywhere.com/. Please note that the site is still a work in progress, and many more existing features are yet to come.

## Installation

1. Install Python on your system if you haven't already.
2. Clone this repository to your local machine using `git clone git@github.com:SiraYsia/QuizMe-App.git`.
3. Change into the project directory: `cd QuizMe`.
4. Install the required dependencies using `pip install -r requirements.txt`.
5. run app.py and follow the prompt 

## Usage

- Visit the QuizMe app homepage to create personalized flashcards.
- Log in or sign up to save and access your flashcard sets.
- Use the "Get Started" option to generate flashcards from study materials.
- Choose to append new flashcards to existing sets or create new sets.
- Access your flashcards from the "Your Flashcards" page.


