from flask import Flask, render_template, request, redirect, url_for
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
    flashcards = db.relationship('Flashcard', backref='flashcard_set', lazy=True, cascade='all, delete-orphan')  # Add cascade option

    def __repr__(self):
        return f"FlashcardSet(name='{self.name}')"
    
# Define the Flashcard model representing the flashcard table. Each flashcard has a front and a back
class Flashcard(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    front = db.Column(db.String(100), nullable=False)
    back = db.Column(db.String(100), nullable=False)
    flashcard_set_id = db.Column(db.Integer, db.ForeignKey('flashcard_set.id', ondelete='CASCADE'), nullable=False)  # Add ondelete option

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
    append_option = request.form.get('append_option')
    flashcards = generate_flashcards(study_material, flashcard_count)
  

    if append_option == 'no':
        return render_template('flashcards.html', flashcards=flashcards)
    

    if append_option == "yes":
        # Retrieve the authenticated user
        user_id = session.get('user_id')
        user = User.query.get(user_id)

        # Find the flashcard set with the given name associated with the user
        flashcard_set_name = request.form.get('append_name')
        flashcard_set = FlashcardSet.query.filter_by(name=flashcard_set_name, user=user).first()

        if flashcard_set:
            existing_flashcards = flashcard_set.flashcards
            all_flashcards = existing_flashcards.copy()


        formatted_flashcards = [[flashcard.front, flashcard.back] for flashcard in all_flashcards]
        appended_array = formatted_flashcards + flashcards
        

        return render_template('flashcards.html', flashcards=appended_array)
    
    return redirect('index.html')


@app.route('/your-flashcards', methods=['GET', 'POST'])
def your_flashcards():
    if 'user_id' not in session:
        # User is not authenticated, redirect them to the login page or show an error message
        return render_template('login.html', error_message="Please log in to access your flashcards.")

    # Retrieve the authenticated user
    user_id = session['user_id']
    user = User.query.get(user_id)

    if request.method == 'POST':
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
# Add a new route for editing a flashcard set
@app.route('/edit_flashcard_set/<flashcard_set_name>', methods=['GET', 'POST'])
def edit_flashcard_set(flashcard_set_name):
    if 'user_id' not in session:
        # User is not authenticated, redirect them to the login page or show an error message
        return render_template('login.html', error_message="Please log in to access your flashcards.")

    user_id = session['user_id']
    user = User.query.get(user_id)

    flashcard_set = FlashcardSet.query.filter_by(name=flashcard_set_name, user=user).first()

    if not flashcard_set:
        # Handle the case when the flashcard set is not found
        return "Flashcard set not found"

    if request.method == 'POST':
        # Get the edited flashcard data from the form
        questions = request.form.getlist('question[]')
        answers = request.form.getlist('answer[]')

        # Update the flashcards with the edited data
        flashcards = flashcard_set.flashcards
        for flashcard, question, answer in zip(flashcards, questions, answers):
            flashcard.front = question
            flashcard.back = answer

        # Commit the changes to the database
        db.session.commit()

        # Redirect back to the your-flashcards page after saving changes
        return redirect(url_for('your_flashcards'))

    # Render the edit-flashcard-set.html template with the flashcards
    return render_template('edit-flashcard-set.html', flashcard_set=flashcard_set)


@app.route('/success')
def success():
    return render_template('success.html')

app.route('/single-flashcard')
def single_flashcard():
    return render_template('single-flashcard.html')


@app.route('/aboutus')
def about_us():
    return render_template('aboutus.html')

@app.route('/delete_flashcard_set/<flashcard_set_name>', methods=['DELETE'])
def delete_flashcard_set(flashcard_set_name):
    # Retrieve the authenticated user
    user_id = session.get('user_id')
    user = User.query.get(user_id)


    # Find the flashcard set with the given name associated with the user
    flashcard_set = FlashcardSet.query.filter_by(name=flashcard_set_name, user=user).first()
    print(flashcard_set)
    print("ASD")

    if flashcard_set:
        # Delete the flashcard_set and associated flashcards from the database
        db.session.delete(flashcard_set)
        db.session.commit()
        return '', 204  # Return an empty response with status code 204 (No Content) to indicate successful deletion
    else:
        return 'Flashcard set not found', 404
    
    
@app.route('/search_flashcard_sets', methods=['POST'])
def search_flashcard_sets():
    if 'user_id' not in session:
        # User is not authenticated, redirect them to the login page or show an error message
        return render_template('login.html', error_message="Please log in to access your flashcards.")

    # Retrieve the authenticated user
    user_id = session['user_id']
    user = User.query.get(user_id)

    # Get the keywords/tags from the search form
    search_keywords = request.form.get('search_keywords')

    # Retrieve flashcard sets that match the search criteria
    flashcard_sets = FlashcardSet.query.filter(FlashcardSet.name.ilike(f'%{search_keywords}%'), FlashcardSet.user == user).all()
    if not flashcard_sets:
        # No matching flashcard set found, render a message
        return render_template('your-flashcards.html', flashcard_sets=None, message="No matching flashcard set was found.")

    # Render the your-flashcards.html template with the filtered flashcard sets
    return render_template('your-flashcards.html', flashcard_sets=flashcard_sets)

if __name__ == '__main__':
    app.run(debug=True)
