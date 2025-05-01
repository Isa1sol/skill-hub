from flask import render_template, request, jsonify, session, redirect, url_for
from flask_login import login_user, logout_user, current_user, login_required
from app import app, db
from app.models import User

# ⌨️ Home Page (Postmodern Styled)
@app.route('/')
def home():
    return render_template("index.html")

# 📝 Registration Page (Form or JSON)
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        data = request.get_json() or request.form
        username = data.get('username')
        password = data.get('password')
        role = data.get('role', 'student')

        if not username or not password:
            return jsonify({"message": "Missing fields"}), 400

        if User.query.filter_by(username=username).first():
            return jsonify({"message": "Username already exists"}), 409

        new_user = User(username=username, password=password, role=role)
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"message": "Registered successfully!"})
    return render_template("register.html")

# 🔐 Login Page (Form or JSON)
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.get_json() or request.form
        username = data.get('username')
        password = data.get('password')

        user = User.query.filter_by(username=username, password=password).first()
        if user:
            login_user(user)
            return jsonify({"message": "Logged in", "role": user.role})
        return jsonify({"message": "Invalid credentials"}), 401
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
