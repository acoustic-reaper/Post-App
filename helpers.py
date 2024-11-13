import os
from flask import redirect, render_template, session, flash
from functools import wraps
from cs50 import SQL

def apology(message, code=400):
    """Render message as an apology to user."""
    def escape(s):
        """
        Escape special characters.
        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=escape(message), message=message), code

def login_required(f):
    """Decorator to require login for routes."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            flash("Please log in to access this page.")
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    """Decorator to require admin role for routes."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_role") != "Admin":
            flash("Unauthorized access. Admins only.")
            return redirect("/")
        return f(*args, **kwargs)
    return decorated_function