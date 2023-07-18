from flask import Flask, render_template, request, redirect
import sqlite3
from bcrypt import hashpw, gensalt

app = Flask(__name__)
conn = sqlite3.connect('your_database.db')
cursor = conn.cursor()

# Create the users table if it doesn't exist
cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    email TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL
                )''')
conn.commit()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def signup():
    email = request.form['email']
    password = request.form['password']
    
    # Check if the email is already registered
    cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
    if cursor.fetchone():
        return "Email already registered"

    # Hash the password
    hashed_password = hashpw(password.encode('utf-8'), gensalt())
    
    # Store the user's information in the database
    cursor.execute("INSERT INTO users (email, password) VALUES (?, ?)", (email, hashed_password))
    conn.commit()
    
    # Redirect the user to a success page or back to the get started page
    return redirect('/success.html')

if __name__ == '__main__':
    app.run()
