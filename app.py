"""Blogly application."""

from flask import Flask, request, redirect, render_template
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "SECRET!"
debug = DebugToolbarExtension(app)

connect_db(app)
# db.create_all()

@app.route("/")
def go_to_users():
    """Redirects to user list."""
    return redirect("/users")

@app.route("/users")
def show_users():
    """List users and show add button."""
    users = User.query.all()
    return render_template("user_list.html", users=users)

@app.route("/users/new", methods=["GET"])
def show_user_form():
    """Show new user sign-up form"""
    return render_template("new_user_form.html")

@app.route("/users/new", methods=["POST"])
def add_user():
    """Add user and redirect to new user detail page."""
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    image_url = request.form['image_url']
    image_url = image_url if image_url else "default image url"

    user = User(first_name=first_name, last_name=last_name, image_url=image_url)
    db.session.add(user)
    db.session.commit()

    return redirect(f"/users")

@app.route("/users/<int:user_id>")
def show_user(user_id):
    """Show info on a single user."""
    user = User.query.get_or_404(user_id)
    return render_template("user_detail.html", user=user)

@app.route("/users/<int:user_id>/edit", methods=["GET"])
def show_edit_user_form(user_id):
    """Show edit page for user"""
    user = User.query.get_or_404(user_id)
    return render_template("edit_user.html", user=user)

@app.route("/users/<int:user_id>/edit", methods=["POST"])
def edit_user(user_id):
    """Edit user information"""
    user = User.query.get_or_404(user_id)
    return redirect(f"/users/{user_id}")

@app.route("/users/<int:user_id>/delete")
def delete_user(user_id):
    """Delete a user"""
    user = User.query.get_or_404(user_id)
    return redirect("/users")

