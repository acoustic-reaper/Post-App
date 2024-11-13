import sqlite3

# Connect to the SQLite3 database
connection = sqlite3.connect("Post_App.db")
cursor = connection.cursor()

# Create `users` table with a role column to distinguish between Admin and Normal users
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    hash TEXT NOT NULL,
    role TEXT NOT NULL CHECK (role IN ('Admin', 'Normal'))
);
""")

# Create `posts` table for storing posts created by Admins
cursor.execute("""
CREATE TABLE IF NOT EXISTS posts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    timestamp TEXT DEFAULT CURRENT_TIMESTAMP
);
""")

# Create `comments` table for storing comments on posts made by Normal users
cursor.execute("""
CREATE TABLE IF NOT EXISTS comments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    post_id INTEGER NOT NULL,
    content TEXT NOT NULL,
    timestamp TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (post_id) REFERENCES posts(id)
);
""")

# Commit the changes and close the connection
connection.commit()
connection.close()

print("Database setup complete.")
