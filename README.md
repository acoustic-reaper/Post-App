# Post App

Post App is a simple web application for creating and managing posts. It supports user authentication, role-based access control, and allows users to comment on posts.
(Live Link to access -> https://mohdalauddinnizami.pythonanywhere.com/)
(Use username - "admin1", pass - "password1" to login as an admit and test the app.)

## Table of Contents

- [Setting Up the Project Locally](#setting-up-the-project-locally)
- [Structure of the Application](#structure-of-the-application)
- [How to Use the Application](#how-to-use-the-application)
  - [Normal Users](#normal-users)
  - [Admin Users](#admin-users)
- [Dependencies](#dependencies)
- [Future Enhancements](#future-enhancements)
- [License](#license)

## Setting Up the Project Locally

1. **Clone the repository:**
    ```sh
    git clone https://github.com/yourusername/post-app.git
    cd post-app
    ```

2. **Create a virtual environment:**
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install the dependencies:**
    ```sh
    pip install -r requirements.txt
    ```

4. **Set up the database:**
    The `Post_App.db` file is already included in the repository. However, if you wish to delete it and create a new one, you can run:
    ```sh
    python setup_db.py
    ```

5. **Run the application:**
    ```sh
    flask run
    ```

## Structure of the Application

- `app.py`: Main application file containing route definitions and application logic.
- `helpers.py`: Helper functions and decorators.
- `setup_db.py`: Script to set up the SQLite database.
- `static/`: Directory for static files like CSS.
- `templates/`: Directory for HTML templates.

## How to Use the Application

### Normal Users

1. **Log In:**
    - Navigate to `/login` and enter your username and password.

2. **View Posts:**
    - After logging in, you will be redirected to the home page where you can see the latest posts.

3. **Comment on Posts:**
    - Click on a post to view its details and add comments.

4. **Change Password:**
    - Navigate to `/changepassword` to change your password.

### Admin Users

1. **Log In:**
    - Navigate to `/login` and enter your admin username and password.

2. **Add Posts:**
    - Navigate to `/admin/posts` to add new posts.

3. **Manage Users:**
    - Navigate to `/admin/users` to view and create new users.

## Dependencies

- `cs50`
- `Flask`
- `Flask-Session`
- `requests`

Install all dependencies using:
```sh
pip install -r [requirements.txt](http://_vscodecontentref_/4)
```
## Future Enhancements

### Registration Functionality
Currently, the application does not support user registration. This feature can be implemented in future versions.

### Workaround for Adding Admins
To add admin users manually, you can use SQLite commands in the terminal. Here is an example:

1. Open the SQLite command-line tool:
```sh
sqlite3 Post_App.db
```
2. Insert admin users:
```sh
INSERT INTO users (username, hash, role) VALUES ('admin1', '<hash_for_password1>', 'Admin');
INSERT INTO users (username, hash, role) VALUES ('admin2', '<hash_for_password2>', 'Admin');
INSERT INTO users (username, hash, role) VALUES ('admin3', '<hash_for_password3>', 'Admin');
```
3. Exit the SQLite command-line tool:
```sh
.exit
```
Once the admin users are added, they can log in and create normal users through the application.
