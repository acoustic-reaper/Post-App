import os
from datetime import datetime
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import apology, login_required, admin_required

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///Post_App.db")

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/")
@login_required
def index():
    """Show the latest posts"""
    posts = db.execute("SELECT * FROM posts ORDER BY timestamp DESC")
    return render_template("index.html", posts=posts)

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""
    session.clear()
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if not username or not password:
            return apology("Username and password are required")

        rows = db.execute("SELECT * FROM users WHERE username = ?", username)
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], password):
            return apology("Invalid username and/or password")

        session["user_id"] = rows[0]["id"]
        session["user_role"] = rows[0]["role"]
        return redirect("/")
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    """Log user out"""
    session.clear()
    return redirect("/")

@app.route("/changepassword", methods=["GET", "POST"])
@login_required
def changepassword():
    if request.method == "POST":
        oldpassword = request.form.get("oldpassword")
        newpassword = request.form.get("newpassword")
        newpasswordagain = request.form.get("newpasswordagain")

        if not oldpassword or not newpassword or not newpasswordagain:
            return apology("All fields are required", 400)

        rows = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])
        if not check_password_hash(rows[0]["hash"], oldpassword):
            return apology("Old password is incorrect", 400)
        if newpassword != newpasswordagain:
            return apology("New passwords do not match", 400)

        newhash = generate_password_hash(newpassword)
        db.execute("UPDATE users SET hash = ? WHERE id = ?", newhash, session["user_id"])

        flash("Password updated successfully")
        return redirect("/")
    else:
        return render_template("changepass.html")

@app.route("/admin/users")
@login_required
@admin_required
def admin_users():
    """Show list of all users"""
    users = db.execute("SELECT * FROM users")
    return render_template("admin_users.html", users=users)

@app.route("/admin/posts", methods=["GET", "POST"])
@login_required
@admin_required
def admin_posts():
    """Add new posts"""
    if request.method == "POST":
        title = request.form.get("title")
        content = request.form.get("content")
        if not title or not content:
            return apology("Title and content are required", 400)

        db.execute("INSERT INTO posts (title, content, timestamp) VALUES (?, ?, ?)",
                   title, content, datetime.now())
        flash("Post added successfully")
        return redirect("/admin/posts")
    else:
        return render_template("admin_posts.html")

@app.route("/posts/<int:post_id>", methods=["GET", "POST"])
@login_required
def post_detail(post_id):
    """View and add comments to a post"""
    if request.method == "POST":
        content = request.form.get("content")
        if not content:
            return apology("Comment content is required", 400)

        db.execute("INSERT INTO comments (user_id, post_id, content, timestamp) VALUES (?, ?, ?, ?)",
                   session["user_id"], post_id, content, datetime.now())
        flash("Comment added successfully")
        return redirect(f"/posts/{post_id}")
    else:
        post = db.execute("SELECT * FROM posts WHERE id = ?", post_id)
        comments = db.execute("SELECT * FROM comments WHERE post_id = ? ORDER BY timestamp DESC", post_id)
        return render_template("post_detail.html", post=post[0], comments=comments)

if __name__ == "__main__":
    app.run(debug=True)