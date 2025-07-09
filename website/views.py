#why we use this file:
# -          To define the views and routes for the Flask application, such as the home page
from flask import Blueprint, render_template
from flask_login import login_user, logout_user, login_required,current_user
from .models import Note
from flask import request, flash, redirect, url_for
from . import db  # Import the db object from your application module
import json,jsonify  # Import json to handle JSON data

views=Blueprint('views', __name__)
@views.route('/', methods=['GET', 'POST'])  # Define the route for the home page
@login_required  # Ensure that the user is logged in before accessing the home page
def home():
    if request.method == 'POST':
        note = request.form.get("note")  # Retrieve the note from the form
        if not note or len(note) < 1:
            flash("Note is too short!", category='error')
        else:
            new_note = Note(data=note, user_id=current_user.id)  # Create a new note instance
            db.session.add(new_note)  # Add the note to the database session
            db.session.commit()  # Commit the changes to the database
            flash("Note added!", category='success')  # Display a success message

    notes = Note.query.filter_by(user_id=current_user.id).all()  # Retrieve all notes for the current user
    return render_template("home.html", user=current_user, notes=notes)  # Pass notes to the template
@views.route('/delete-note', methods=['POST'])  # Define the route for deleting a note
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
    return jsonify({})  # Return an empty JSON response
