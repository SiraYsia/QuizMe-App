"""app.py"""

from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
import bcrypt
from generate_flashcards.send_request import generate_flashcards
from flask import session
import git
import os
from dotenv import load_dotenv
from sqlalchemy import func
import uuid
from flask import abort

load_dotenv()

shared_links = {}

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///quizme.db"


db = SQLAlchemy(app)

# User model representing the user table
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    # Establishing the relationship between User and FlashcardSet models
    flashcards = db.relationship("FlashcardSet", backref="user", lazy=True)

    def __repr__(self):
        return f"User(email='{self.email}')"


# FlashcardSet model representing the flashcard_set table. Flashard names.
class FlashcardSet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    flashcards = db.relationship(
        "Flashcard", backref="flashcard_set", lazy=True, cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"FlashcardSet(name='{self.name}')"


# Flashcard model representing the flashcard table. Each flashcard has a front and a back
class Flashcard(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    front = db.Column(db.String(100), nullable=False)
    back = db.Column(db.String(100), nullable=False)
    flashcard_set_id = db.Column(
        db.Integer,
        db.ForeignKey("flashcard_set.id", ondelete="CASCADE"),
        nullable=False,
    )

    def __repr__(self):
        return f"Flashcard(front='{self.front}', back='{self.back}')"


# Used to store flashcards created by users before they finalize and save them to a permanent falshard set since sessions are limited in storage
class TemporaryFlashcard(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    front = db.Column(db.String(100), nullable=False)
    back = db.Column(db.String(100), nullable=False)


with app.app_context():
    db.create_all()


@app.context_processor
def inject_user():
    user_id = session.get("user_id")
    if user_id:
        user = User.query.get(user_id)
        return dict(logged_in_user=user)
    return dict(logged_in_user=None)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():

    if "user_id" in session:
        user = User.query.get(session["user_id"])
        if user: 
            return redirect(url_for("your_flashcards"))

    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        # Retrieve the user from the database based on the provided email
        user = User.query.filter_by(email=email).first()
        if not email or not password:
            error_message = "Please provide both email and password."
            return render_template("login.html", error_message=error_message)

        if user:
            # Compare the hashed password stored in the database with the provided password
            if bcrypt.checkpw(password.encode("utf-8"), user.password):
                # Passwords match, user is authenticated
                # Store the authenticated user's ID in the session
                session["user_id"] = user.id

                return render_template("success.html", user=user)

        error_message = "Invalid email or password. Please try again."
        return render_template("login.html", error_message=error_message)

    return render_template("login.html")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if "user_id" in session:
        user = User.query.get(session["user_id"])
        if user:  # Check if the user exists in the database
            return redirect(url_for("your_flashcards"))

    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        if not email and not password:
            error_message = "Provide Email and Password"
            return render_template("signup.html", error_message=error_message)
        if not email or not password:
            error_message = "Provide Email and Password"
            return render_template("signup.html", error_message=error_message)

        user = User.query.filter_by(email=email).first()
        if user:
            # Email is not unique, show an error message
            error_message = "Email is already in use. Please choose a different email."
            return render_template("signup.html", error_message=error_message)

        hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
        user = User(email=email, password=hashed_password)
        db.session.add(user)
        db.session.commit()

        # redirect the user to login page
        return render_template("login.html")

    return render_template("signup.html")


@app.route("/logout")
def logout():
    session.pop("user_id", None)
    return redirect(url_for("index"))


@app.route("/StartCreating")
def get_started():
    user_id = session.get("user_id")
    user = User.query.get(user_id)
    flashcard_set_names = [flashcard_set.name for flashcard_set in user.flashcards]

    return render_template("getstarted.html", flashcard_set_names=flashcard_set_names)


@app.route("/CreateFlashcards", methods=["GET", "POST"])
def create_flashcards():

    if "user_id" not in session:
        return render_template(
            "login.html", error_message="Please log in to create flashcards."
        )

    user_id = session["user_id"]
    user = User.query.get(user_id)

    # Delete previous temp flashcards
    TemporaryFlashcard.query.filter_by(user_id=user_id).delete()
    db.session.commit()

    study_material = request.form.get("study_material")
    flashcard_count = request.form.get("flashcard_count")

    # Error handling for missing study material or flashcard count
    if not study_material or not flashcard_count:
        error_message = "Study material and flashcard count are required fields."
        return render_template("getstarted.html", error_message=error_message)

    try:
        flashcard_count = int(flashcard_count)
        if flashcard_count <= 0:
            raise ValueError()
    except ValueError:
        error_message = "Invalid flashcard count. Please provide a positive integer."
        return render_template(
            "getstarted.html", flashcards={}, error_message=error_message
        )

    append_option = request.form.get("append_option")
    flashcard_map = generate_flashcards(study_material, flashcard_count)

    if append_option == "no":

        flashcards = [
            {"Front": front, "Back": back} for front, back in flashcard_map.items()
        ]

        for flashcard in flashcards:
            temp_flashcard = TemporaryFlashcard(
                user_id=user_id, front=flashcard["Front"], back=flashcard["Back"]
            )
            db.session.add(temp_flashcard)
        db.session.commit()

        length = len(flashcards)

        if length == 0:
            error_message = "Flashcards were not generated. Please try again."
            return render_template("getstarted.html", error_message=error_message)

        return redirect(url_for("view_flashcards", LengthOfNewFlashcards=length))

    if append_option == "yes":

        flashcard_set_name = request.form.get("append_name")
        if not flashcard_set_name:
            error_message = (
                "Specify the name of the flashcard set you want to append to."
            )
            return render_template("getstarted.html", error_message=error_message)

        flashcard_set = FlashcardSet.query.filter_by(
            name=flashcard_set_name, user=user
        ).first()

        if not flashcard_set:
            error_message = f"Flashcard set '{flashcard_set_name}' does not exist. Please provide a valid set name."
            return render_template(
                "getstarted.html", flashcards=[], error_message=error_message
            )

        existing_flashcards = flashcard_set.flashcards
        formatted_flashcards = [
            {"Front": flashcard.front, "Back": flashcard.back}
            for flashcard in existing_flashcards
        ]
        new_flashcards = [
            {"Front": front, "Back": back} for front, back in flashcard_map.items()
        ]
        length = len(new_flashcards)

        if length == 0:
            error_message = "Flashcards were not generated. Please try again."
            return render_template("getstarted.html", error_message=error_message)

        else:
            appended_flashcards = formatted_flashcards + new_flashcards
            for flashcard in appended_flashcards:
                # print("what is front?", flashcard['Front'])
                temp_flashcard = TemporaryFlashcard(
                    user_id=user_id, front=flashcard["Front"], back=flashcard["Back"]
                )
                db.session.add(temp_flashcard)
                db.session.commit()
                length = len(new_flashcards)

        return redirect(url_for("view_flashcards", LengthOfNewFlashcards=length))

    return redirect(url_for("index"))


@app.route("/ViewFlashcards", methods=["GET"])
def view_flashcards():
    user_id = session.get("user_id")

    temporary_flashcards = TemporaryFlashcard.query.filter_by(user_id=user_id).all()
    flashcards_temp = [
        {"Front": flashcard.front, "Back": flashcard.back}
        for flashcard in temporary_flashcards
    ]

    length_of_new_flashcards = request.args.get(
        "LengthOfNewFlashcards", default=0, type=int
    )  
    return render_template(
        "flashcards.html",
        flashcards=flashcards_temp,
        LengthOfNewFlashcards=length_of_new_flashcards,
    )


@app.route("/YourFlashcards", methods=["GET", "POST"])
def your_flashcards():
    if "user_id" not in session:
        return render_template(
            "login.html", error_message="Please log in to access your flashcards."
        )

    user_id = session["user_id"]
    user = User.query.get(user_id)

    if request.method == "POST":
        flashcard_set_name = request.form.get("flashcard_set_name")
        questions = request.form.getlist("question[]")
        answers = request.form.getlist("answer[]")

        # Check if the flashcard set name already exists
        existing_flashcard_set = FlashcardSet.query.filter_by(
            name=flashcard_set_name, user=user
        ).first()
        if existing_flashcard_set:
            error_message = "Set name already exsists. Please choose a different name."
            flashcards_temp = [
                {"Front": question, "Back": answer}
                for question, answer in zip(questions, answers)
            ]

            # Retrieving existing flashcards from the questions and answers to display so they don't lose thier progress
            return render_template(
                "flashcards.html",
                flashcards=flashcards_temp,
                LengthOfNewFlashcards=len(flashcards_temp),
                error_message=error_message,
            )

        # Create a new flashcard set associated with the user
        flashcard_set = FlashcardSet(name=flashcard_set_name, user=user)
        db.session.add(flashcard_set)
        db.session.commit()

        # Create flashcards and associate them with the flashcard set
        for question, answer in zip(questions, answers):
            flashcard = Flashcard(
                front=question, back=answer, flashcard_set=flashcard_set
            )
            db.session.add(flashcard)
        db.session.commit()

        # Redirect to the your_flashcards page to prevent resubmission
        return redirect(url_for("your_flashcards"))

    flashcard_sets = user.flashcards[::-1]
    message = ""
    if not flashcard_sets:
        message = "Your saved flashcard sets will appear here."

    return render_template(
        "your-flashcards.html", flashcard_sets=flashcard_sets, message=message
    )



@app.route("/YourFlashcards/<flashcard_set_name>")
def single_flashcard(flashcard_set_name):
    if "user_id" not in session:
        return render_template(
            "login.html", error_message="Please log in to access your flashcards."
        )

    user_id = session["user_id"]
    user = User.query.get(user_id)

    flashcard_set = FlashcardSet.query.filter_by(
        name=flashcard_set_name, user=user
    ).first()


# shared_links = {
#     user_id_1: {
#         "share_link_1": flashcard_set_id_1,
#         "share_link_2": flashcard_set_id_2,
#     },
#     user_id_2: {
#         "share_link_3": flashcard_set_id_3,
#     },
# }
    if flashcard_set:
        flashcards = flashcard_set.flashcards
        share_link = None 

        # Check if the user already has a share link for this flashcard set
        if user_id in shared_links:
            for link, fs in shared_links[user_id].items(): 
                if fs == flashcard_set.id:  
                    share_link = link            
                    break     

        if not share_link:
            share_link = str(uuid.uuid4())
            if user_id not in shared_links:
                shared_links[user_id] = {}
            shared_links[user_id][share_link] = flashcard_set.id 

        return render_template(
            "single-flashcard.html",
            flashcards=flashcards,
            flashcard_set_name=flashcard_set_name,
            share_link=f"{request.host_url}shared/{share_link}"
        )
    else:
        return abort(404)

@app.route("/shared/<share_link>")
def shared_flashcard(share_link):

    flashcard_set = None
    for user_id, links in shared_links.items():
        if share_link in links:
            flashcard_set_id = links[share_link]
            flashcard_set = FlashcardSet.query.get(flashcard_set_id)
            break

    if flashcard_set:
        flashcards = flashcard_set.flashcards
        return render_template(
            "shared-flashcard.html",
            flashcards=flashcards,
            flashcard_set_name=flashcard_set.name
        )
    else:
        abort(404)


@app.route("/EditSet/<flashcard_set_name>", methods=["GET", "POST"])
def edit_flashcard_set(flashcard_set_name):
    if "user_id" not in session:
        return render_template(
            "login.html", error_message="Please log in to access your flashcards."
        )

    user_id = session["user_id"]
    user = User.query.get(user_id)

    flashcard_set = FlashcardSet.query.filter_by(
        name=flashcard_set_name, user=user
    ).first()

    if not flashcard_set:
        return render_template(
            "your-flashcards.html", error_message="Flashcard set not found"
        )

    if request.method == "POST":
        questions = request.form.getlist("question[]")
        answers = request.form.getlist("answer[]")

        # Remove all existing flashcards
        for flashcard in flashcard_set.flashcards:
            db.session.delete(flashcard)

        # Add new and updated flashcards
        for question, answer in zip(questions, answers):
            if question.strip() and answer.strip():  # Only add non-empty flashcards
                new_flashcard = Flashcard(
                    front=question, back=answer, flashcard_set=flashcard_set
                )
                db.session.add(new_flashcard)

        # If no flashcards remain, delete the entire flashcard set, (not really possible since empty flashcards aren't allowed to be saved)
        if not questions or all(not q.strip() for q in questions):
            db.session.delete(flashcard_set)
            db.session.commit()
            return redirect(url_for("your_flashcards"))

        db.session.commit()
        return redirect(url_for("your_flashcards"))

    return render_template("edit-flashcard-set.html", flashcard_set=flashcard_set)


@app.route("/Profile")
def success():
    if "user_id" not in session:
        return redirect(url_for("login"))
    user = User.query.get(session["user_id"])
    return render_template("success.html", user=user)


@app.route("/AboutUs")
def about_us():
    return render_template("aboutus.html")


@app.route("/DeleteSet/<flashcard_set_name>", methods=["DELETE"])
def delete_flashcard_set(flashcard_set_name):
    # Retrieve the authenticated user
    user_id = session.get("user_id")
    user = User.query.get(user_id)

    flashcard_set_name = flashcard_set_name.strip()

    flashcard_set = FlashcardSet.query.filter(
        func.replace(FlashcardSet.name, " ", "")
        == func.replace(flashcard_set_name, " ", ""),
        FlashcardSet.user == user,
    ).first()

    if flashcard_set:
        db.session.delete(flashcard_set)
        db.session.commit()
        return "", 204
    else:
        return "Flashcard set not found", 404


@app.route("/SearchFlashCardSet", methods=["POST"])
def search_flashcard_sets():
    if "user_id" not in session:
        return render_template(
            "login.html", error_message="Please log in to access your flashcards."
        )

    user_id = session["user_id"]
    user = User.query.get(user_id)
    search_keywords = request.form.get("search_keywords")

    # Retrieve flashcard sets that match the search criteria
    flashcard_sets = FlashcardSet.query.filter(
        FlashcardSet.name.ilike(f"%{search_keywords}%"), FlashcardSet.user == user
    ).all()

    if not flashcard_sets:
        if search_keywords:
            message = "No matching flashcard set was found."
        else:
            message = "Your saved flashcard sets will appear here. "
        return render_template(
            "your-flashcards.html", flashcard_sets=flashcard_sets, message=message
        )
    flashcard_sets = flashcard_sets[::-1]

    return render_template("your-flashcards.html", flashcard_sets=flashcard_sets)


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


@app.route("/update_server", methods=["POST"])
def webhook():
    if request.method == "POST":
        repo = git.Repo("/home/QuizMeApp/QuizMe-App")
        origin = repo.remotes.origin
        origin.pull()
        return "Updated PythonAnywhere successfully", 200
    else:
        return "Wrong event type", 400


if __name__ == "__main__":
    app.run(debug=True)
