from flask import Flask, render_template, request, redirect, session
from flask_bcrypt import Bcrypt
from flask_app import app
from flask_app.models.user_model import User
from flask_app.models.adventure_model import Adventure
from flask import flash


bcrypt = Bcrypt(app)


@app.route("/")
def index():
    if 'user_id' in session:
        return redirect('/dashboard')
    return render_template("index.html")

@app.route('/users/register', methods=['POST'])
def reg_user():
    if not User.validator(request.form):
        return redirect('/')
    hashed_pass = bcrypt.generate_password_hash(request.form['password'])
    data = {
        **request.form,
        'password':hashed_pass
    }
    logged_user_id = User.create(data)
    session['user_id'] = logged_user_id
    return redirect('/dashboard')

@app.route('/users/login', methods=['POST'])
def log_user():
    data = {
        'email' : request.form['email']
    }
    user_in_db = User.get_by_email(data)
    if not user_in_db:
        flash("Invalid credentials", "log")
        return redirect('/')
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash("Invalid credentials", "log")
        return redirect('/')
    session['user_id'] = user_in_db.id
    return redirect('/dashboard')

@app.route('/logout')
def log_out():
    session.clear()
    return redirect('/')


# Render the Dashboard

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'id':session['user_id']
    }
    logged_user = User.get_by_id(data)
    all_running_adventures = Adventure.get_all_running()
    all_biking_adventures = Adventure.get_all_biking()
    return render_template("welcome.html", logged_user=logged_user, all_running_adventures=all_running_adventures, all_biking_adventures=all_biking_adventures)