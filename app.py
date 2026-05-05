from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(_name_)
app.secret_key = 'secret123'

def get_db():
    return sqlite3.connect('users.db')

@app.route('/')
def home():
    if 'user' in session:
        return redirect('/dashboard')
    return redirect('/login')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        user = request.form['username']
        pwd = request.form['password']

        db = get_db()
        db.execute("INSERT INTO users (username, password) VALUES (?, ?)", (user, pwd))
        db.commit()
        return redirect('/login')
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = request.form['username']
        pwd = request.form['password']

        db = get_db()
        result = db.execute("SELECT * FROM users WHERE username=? AND password=?", (user, pwd)).fetchone()

        if result:
            session['user'] = user
            return redirect('/dashboard')
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'user' in session:
        return render_template('dashboard.html', user=session['user'])
    return redirect('/login')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/login')

if _name_ == '_main_':
    app.run(host='0.0.0.0', port=5000)