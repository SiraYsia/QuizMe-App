from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import bcrypt
from apy import generate_flashcards
from flask import session 

app = Flask(__name__)
app.config['SECRET_KEY'] = 'cSuT6KxPuOayBkNnvTWXO0e0J'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///quizme.db'

db = SQLAlchemy(app)

# Define the User model representing the user table
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
        # Define the columns of the user table

    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
        # Establish the relationship between User and FlashcardSet models

    flashcards = db.relationship('FlashcardSet', backref='user', lazy=True)

    def __repr__(self):
        return f"User(email='{self.email}')"

# Define the FlashcardSet model representing the flashcard_set table. A set of flashcards 
class FlashcardSet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    flashcards = db.relationship('Flashcard', backref='flashcard_set', lazy=True)

    def __repr__(self):
        return f"FlashcardSet(name='{self.name}')"
    
# Define the Flashcard model representing the flashcard table. Each flashcard has a front and a back
class Flashcard(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    front = db.Column(db.String(100), nullable=False)
    back = db.Column(db.String(100), nullable=False)
    flashcard_set_id = db.Column(db.Integer, db.ForeignKey('flashcard_set.id'), nullable=False)

    def __repr__(self):
        return f"Flashcard(front='{self.front}', back='{self.back}')"

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # Retrieve the user from the database based on the provided email
        user = User.query.filter_by(email=email).first()

        if user:
            # Compare the hashed password stored in the database with the provided password
            if bcrypt.checkpw(password.encode('utf-8'), user.password):
                # Passwords match, user is authenticated
                # Store the authenticated user's ID in the session
                session['user_id'] = user.id

                # Redirect the user to the success route
                return render_template('success.html', user=user)

        # Invalid email or password, show an error message
        error_message = "Invalid email or password. Please try again."
        return render_template('login.html', error_message=error_message)

    # GET request, render the login form
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
@app.route('/signup')
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # Hash the password using bcrypt
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        # Store the email and hashed password in the database as well as empty flashcards
        user = User(email=email, password=hashed_password, flashcards = [] )
        db.session.add(user)
        db.session.commit()

        # redirect the user to login page
        return render_template('login.html', email=email)

    # GET request, render the sign-up form
    return render_template('signup.html')

@app.route('/getstarted') 
def get_started():
    return render_template('getstarted.html')

@app.route('/createflashcards', methods=['GET', 'POST'])
def create_flashcards():
    study_material = request.form.get('study_material')
    flashcard_count = int(request.form.get('flashcard_count'))
    flashcards = generate_flashcards(study_material, flashcard_count)
    print(flashcards)
    print(flashcard_count)
    return render_template('flashcards.html', flashcards=flashcards)

@app.route('/your-flashcards', methods=['POST'])
def your_flashcards():
    if 'user_id' not in session:
        # User is not authenticated, redirect them to the login page or show an error message
        return render_template('login.html', error_message="Please log in to access your flashcards.")

    # Retrieve the authenticated user
    user_id = session['user_id']
    user = User.query.get(user_id)

    flashcard_set_name = request.form.get('flashcard_set_name')
    questions = request.form.getlist('question[]')
    answers = request.form.getlist('answer[]')

    # Create a new flashcard set associated with the user
    flashcard_set = FlashcardSet(name=flashcard_set_name, user=user)
    db.session.add(flashcard_set)
    db.session.commit()

    # Create flashcards and associate them with the flashcard set
    for question, answer in zip(questions, answers):
        flashcard = Flashcard(front=question, back=answer, flashcard_set=flashcard_set)
        db.session.add(flashcard)
    db.session.commit()

    # Retrieve all flashcard sets associated with the user
    flashcard_sets = user.flashcards

    # Render the your-flashcards.html template with the flashcard sets
    return render_template('your-flashcards.html', flashcard_sets=flashcard_sets)

@app.route('/single-flashcard/<flashcard_set_name>')
def single_flashcard(flashcard_set_name):
    if 'user_id' not in session:
        # User is not authenticated, redirect them to the login page or show an error message
        return render_template('login.html', error_message="Please log in to access your flashcards.")
    
    user_id = session['user_id']
    user = User.query.get(user_id)
    
    flashcard_set = FlashcardSet.query.filter_by(name=flashcard_set_name, user=user).first()
    
    if flashcard_set:
        # Retrieve the flashcards associated with the flashcard set
        flashcards = flashcard_set.flashcards
        
        # Render the single-flashcard.html template with the flashcards
        return render_template('single-flashcard.html', flashcards=flashcards, flashcard_set_name=flashcard_set_name)
    else:
        # Handle the case when the flashcard set is not found
        return "Flashcard set not found"

@app.route('/new_flash')
def new_flash():
    return render_template('new-name.html')


@app.route('/append')
def append():
    return render_template('append.html')

@app.route('/success')
def success():
    return render_template('success.html')

app.route('/single-flashcard')
def single_flashcard():
    return render_template('single-flashcard.html')

# @app.route('/single-flashcard/<flashcard_set_name>')
# def single_flashcard(flashcard_set_name):
#     if 'user_id' not in session:
#         # User is not authenticated, redirect them to the login page or show an error message
#         return render_template('login.html', error_message="Please log in to access your flashcards.")
#     user_id = session['user_id']
#     user = User.query.get(user_id)
#     flashcard_set = FlashcardSet.query.filter_by(name=flashcard_set_name, user=user).first()

#     if flashcard_set:
#         # Retrieve the flashcards associated with the flashcard set
#         flashcards = flashcard_set.flashcards

#         # Render the single_flashcard.html template with the flashcards
#         return render_template('single-flashcard.html', flashcards=flashcards, flashcard_set_name=flashcard_set_name)
#     else:
#         # Handle the case when the flashcard set is not found
#         return "Flashcard set not found"


    # # Retrieve the flashcard set based on the provided name
    # flashcard_set = FlashcardSet.query.filter_by(name=flashcard_set_name).first()

    # if flashcard_set:
    #     # Retrieve the flashcards associated with the flashcard set
    #     flashcards = flashcard_set.flashcards
    #     return render_template('single_flashcard.html', flashcards=flashcards)
    # else:
    #     # Handle the case when the flashcard set is not found


@app.route('/aboutus')
def about_us():
    return render_template('aboutus.html')



# @app.route('/single-flashcard/<int:flashcard_set_id>')
# def single_flashcard(flashcard_set_id):
#     # Retrieve the flashcard set based on the flashcard_set_id
#     flashcard_set = FlashcardSet.query.get(flashcard_set_id)

#     # Retrieve the flashcards associated with the flashcard set
#     flashcards = flashcard_set.flashcards

#     # Render the single_flashcard.html template with the flashcards
#     return render_template('single-flashcard.html', flashcards=flashcards)


if __name__ == '__main__':
    app.run(debug=True)
