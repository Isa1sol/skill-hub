from flask import render_template, request, jsonify, session, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user, login_required
from app import app, db
from app.models import User
from werkzeug.security import check_password_hash, generate_password_hash

# ⌨️ Home Page (Postmodern Styled)
@app.route('/')
def home():
    return render_template("index.html")

# 📝 Registration Page (Form Handling)
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        role = request.form.get('role', 'student')

        # Ensure that username and password are provided
        if not username or not password:
            flash("Please fill out all fields.")
            return redirect(url_for('register'))

        # Check if username already exists
        if User.query.filter_by(username=username).first():
            flash("Username already exists.")
            return redirect(url_for('register'))

        # Create a new user
        hashed_pw = generate_password_hash(password)
        new_user = User(username=username, password=hashed_pw, role=role)
        db.session.add(new_user)
        db.session.commit()

        # Log in the new user
        login_user(new_user)
        flash("Registered successfully!")
        return redirect(url_for('home'))

    return render_template("register.html")

# 🔐 Login Page (Form Handling)
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Check if user exists and validate password
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            flash("Logged in successfully!")
            return redirect(url_for('dashboard'))  # Redirect to dashboard after login
        else:
            flash("Invalid credentials")
            return redirect(url_for('login'))

    return render_template("login.html")

# 🧠 Dashboard Route with Role-Based Display
@app.route('/dashboard')
@login_required
def dashboard():
    if current_user.role == 'admin':
        return render_template("dashboard_admin.html", user=current_user)
    elif current_user.role == 'instructor':
        return render_template("dashboard_instructor.html", user=current_user)
    else:
        return render_template("dashboard_student.html", user=current_user)

# 🔓 Logout
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))
