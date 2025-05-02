from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import User
from app import db

bp = Blueprint('main', __name__)

# ⌨️ Home Page
@bp.route('/')
def home():
    return render_template("index.html")

# 📝 Registration Page (Form Handling)
@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        role = request.form.get('role', 'student')

        if not username or not password:
            flash("Please fill out all fields.")
            return redirect(url_for('main.register'))

        if User.query.filter_by(username=username).first():
            flash("Username already exists.")
            return redirect(url_for('main.register'))

        hashed_pw = generate_password_hash(password)
        new_user = User(username=username, password=hashed_pw, role=role)
        db.session.add(new_user)
        db.session.commit()

        login_user(new_user)
        flash("Registered successfully!")
        return redirect(url_for('main.dashboard'))

    return render_template("register.html")

# 🔐 Login Page
@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            flash("Logged in successfully!")
            return redirect(url_for('main.dashboard'))
        else:
            flash("Invalid credentials")
            return redirect(url_for('main.login'))

    return render_template("login.html")

# 🧠 Dashboard with Role-Based Routing
@bp.route('/dashboard')
@login_required
def dashboard():
    if current_user.role == 'admin':
        return render_template("dashboard_admin.html", user=current_user)
    elif current_user.role == 'instructor':
        return render_template("dashboard_instructor.html", user=current_user)
    else:
        return render_template("dashboard_student.html", user=current_user)

# 🔓 Logout
@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.home'))
