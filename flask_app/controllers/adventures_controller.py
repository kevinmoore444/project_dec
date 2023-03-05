from flask import Flask, render_template, request, redirect, session
from flask_bcrypt import Bcrypt
from flask_app import app
from flask_app.models.user_model import User
from flask_app.models.adventure_model import Adventure
from flask import flash


# Routes for posting a new adventure on post.html

@app.route('/adventure/new')
def adventure_new():
    if "user_id" not in session:
        return redirect('/')
    data = {
        'id':session['user_id']
    }
    logged_user = User.get_by_id(data)
    return render_template("post.html", logged_user=logged_user)

@app.route('/adventure/create', methods=['POST'])
def create_sighting():
        if "user_id" not in session:
            return redirect('/')
        if not Adventure.validator(request.form):
            return redirect('/adventure/new')
        adventure_data = {
            **request.form,
            'user_id': session['user_id']
        }
        Adventure.create(adventure_data)
        return redirect('/dashboard')

# Delete an Adventure

@app.route('/adventure/<int:id>/delete')
def delete_sighting(id):
    if "user_id" not in session:
        return redirect('/')
    data = {
        'id':id
    }
    Adventure.delete(data)
    return redirect('/dashboard')

# Render update.html in order to edit adventure

@app.route("/adventure/<int:id>/edit")
def edit_adventure(id):
    if "user_id" not in session:
        return redirect('/')
    data = {
        'id':id
    }
    user_data = {
        'id':session['user_id']
    }
    logged_user = User.get_by_id(user_data)
    this_adventure = Adventure.get_one_adventure(data)
    return render_template("update.html", this_adventure=this_adventure, logged_user=logged_user)

# Submit post request in order to update adventure

@app.route("/adventure/<int:id>/update", methods=['POST'])
def update_adventure(id):
    if "user_id" not in session:
        return redirect('/')
    if not Adventure.validator(request.form):
        return redirect(f'/adventure/{id}/edit')
    data = {
        'id':id,
        'activity_type': request.form['activity_type'],
        'route_name': request.form['route_name'],
        'location': request.form['location'],
        'activity_distance': request.form['activity_distance'],
        'vertical_elevation': request.form['vertical_elevation'],
        'terrain_type': request.form['terrain_type'],
        'gpx_link': request.form['gpx_link'],
        'route_logistics': request.form['route_logistics'],
    }
    Adventure.update(data)
    return redirect('/dashboard')


