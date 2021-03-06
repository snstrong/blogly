"""Blogly application."""

from flask import Flask, request, redirect, render_template
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post, Tag, PostTag

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "SECRET!"
debug = DebugToolbarExtension(app)

connect_db(app)
# db.create_all()

@app.route("/")
def go_to_user_list():
    """Redirects to user list."""
    return redirect("/users")

#######################
# User-related routes #
#######################

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
    image_url = request.form['image_url'] or None
    user = User(first_name=first_name, last_name=last_name, image_url=image_url)
    db.session.add(user)
    db.session.commit()

    return redirect(f"/users")

@app.route("/users/<int:user_id>")
def show_user(user_id):
    """Show info on a single user."""
    user = User.query.get_or_404(user_id)
    posts = Post.query.filter(Post.user_id == user_id)
    return render_template("user_detail.html", user=user, posts=posts)

@app.route("/users/<int:user_id>/edit", methods=["GET"])
def show_edit_user_form(user_id):
    """Show edit page for user"""
    user = User.query.get_or_404(user_id)
    return render_template("edit_user.html", user=user)

@app.route("/users/<int:user_id>/edit", methods=["POST"])
def edit_user(user_id):
    """Edit user information"""
    user = User.query.get_or_404(user_id)
    user.id = user.id
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.image_url = request.form['image_url'] or None
    db.session.add(user)
    db.session.commit()
    return redirect(f"/users")

@app.route("/users/<int:user_id>/delete", methods=["POST"])
def delete_user(user_id):
    """Delete a user"""
    user = User.query.get_or_404(user_id)
    User.query.filter_by(id=user.id).delete()
    db.session.commit()
    return redirect("/users")

#######################
# Post-related routes #
#######################

@app.route('/users/<int:user_id>/posts/new')
def show_new_post_form(user_id):
    """Shows form to create new post"""
    user = User.query.get_or_404(user_id)
    return render_template('new_post.html', user=user)

@app.route('/users/<int:user_id>/posts/new', methods=["POST"])
def create_new_post(user_id):
    """Handles form data for new post"""
    user = User.query.get_or_404(user_id)
    new_post = Post(title=request.form['title'],
                    content=request.form['content'],
                    user=user)

    db.session.add(new_post)
    db.session.commit()
    return redirect(f'/users/{user.id}')

@app.route('/posts/<int:post_id>')
def show_post(post_id):
    """Display post"""
    post = Post.query.get_or_404(post_id)
    return render_template('post_detail.html', post=post)

@app.route("/posts/<int:post_id>/edit", methods=["GET"])
def show_edit_post_form(post_id):
    """Show edit form for post"""
    post = Post.query.get_or_404(post_id)
    return render_template("edit_post.html", post=post)

@app.route("/posts/<int:post_id>/edit", methods=["POST"])
def edit_post(post_id):
    """Handle form data for edited post"""
    post = Post.query.get_or_404(post_id)
    post.id = post.id
    post.title = request.form['title']
    post.content = request.form['content']
    db.session.add(post)
    db.session.commit()
    return redirect(f"/posts/{post.id}")

@app.route("/posts/<int:post_id>/delete", methods=["POST"])
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    user_id = post.user_id
    Post.query.filter_by(id=post.id).delete()
    db.session.commit()
    return redirect(f"/users/{user_id}")

#######################
# Tag-related routes #
#######################

@app.route("/tags")
def list_tags():
    """Lists all tags"""
    pass

@app.route("/tags/<int:tag_id>")
def show_tag_detail(tag_id):
    """Show details for given tag"""
    pass

@app.route("/tags/new")
def show_new_tag_form():
    """Displays form for making a new tag"""
    pass

@app.route("/tags/new", methods=["POST"])
def create_new_tag():
    """Handles form information for creating a new tag"""
    return redirect("/tags")

@app.route("/tags/<int:tag_id>/edit")
def show_edit_tag_form(tag_id):
    """Displays edit form for tag"""
    pass

@app.route("/tags/<int:tag_id>/edit", methods=["POST"])
def edit_tag(tag_id):
    """Handles form information for editing an existing tag"""
    return redirect("/tags")

@app.rote("/tags/<int:tag_id>/delete", methods=["POST"])
def delete_tag(tag_id):
    """Deletes a given tag"""
    return redirect("/tags")
