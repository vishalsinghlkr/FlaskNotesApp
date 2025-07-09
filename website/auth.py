#in which we define the authentication routes for our Flask application.
# File: website/auth.py
## This file contains the authentication routes for the Flask application.
#why we use this file:
# -          To handle user authentication, including login, logout, and sign-up functionality.

from flask import Blueprint,render_template,request,flash,redirect,url_for
from .models import User
from . import db  # Import the db object from your application module
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required,current_user


auth=Blueprint('auth', __name__)
@auth.route('/login', methods=['GET', 'POST'])  # Define the route for login
def login():
    if request.method == 'POST':
        email = request.form.get("email")  # Retrieve email from the form
        password = request.form.get("password")  # Retrieve password from the form

        # Check if email and password are provided
        if not email or not password:
            flash("Please fill out both email and password fields.", category='error')
            return render_template("login.html")

        user = User.query.filter_by(email=email).first()  # Query the database for a user with the provided email

        if user:
            if check_password_hash(user.password, password):  # Check if the password matches the hashed password
                flash("Logged in successfully!", category='success')
                login_user(user,remember=True)  # Log in the user using Flask-Login
                # You can also set the user session
                return redirect(url_for('views.home'))  # Redirect to the home page after successful login
            else:
                flash("Incorrect password, try again.", category='error')
        else:
            flash("Email does not exist.", category='error')

    return render_template("login.html",user=current_user)  # Render the login.html template
     

@auth.route('/logout')
@login_required  # Ensure that the user is logged in before allowing logout
def logout():
    logout_user() # Log out the user using Flask-Login
    return redirect(url_for("auth.login")) # Redirect to the login page after logout


@auth.route('/sign-up', methods=['GET', 'POST'])  # Define the route for sign-up
def signup():
    if request.method == 'POST':
        email = request.form.get("email")
        first_name = request.form.get("firstname")  # Fixed typo
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")

        user = User.query.filter_by(email=email).first()
        if user:
            flash("Email already exists.", category='error')
        elif len(email) < 4:
            flash("Email must be greater than 4 characters.", category='error')
        elif len(first_name) < 2:  # Fixed typo
            flash("First name must be greater than 2 characters.", category='error')
        elif len(password1) < 7:
            flash("Password must be at least 7 characters long.", category='error')
        elif password1 != password2:
            flash("Passwords don't match.", category='error')
        else:
            new_user = User(email=email, first_name=first_name, password=generate_password_hash(password1, method='pbkdf2:sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash("Account created!", category='success')
            return redirect(url_for('views.home'))

    return render_template("sign_up.html", user=current_user)  # Render the sign-up template with the current user context

