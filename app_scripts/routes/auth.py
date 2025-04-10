from app_scripts.extensions import mail
from app_scripts.database import get_db_connection

from flask import Blueprint, render_template, request, redirect, session, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
import secrets
from flask_mail import Message # Mail und Message sind Klassen


# bluepront
bp = Blueprint('auth', __name__)

# register
@bp.route('/register', methods=['GET', 'POST'])
def register():
    error_message = None  # Initialize a variable to store the error message

    if 'user_id' in session:
        return redirect(url_for('main.index'))

    if request.method == 'POST':
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']

        conn = get_db_connection()

        # Check if the username already exists
        user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()

        if user:
            # Set an error message if the username already exists
            error_message = "Username already exists. Please choose a different one."
        else:
            # If the username is unique, proceed with registration
            password_hash = generate_password_hash(password)

            conn.execute('INSERT INTO users (email, username, password) VALUES (?, ?, ?)', (email, username, password_hash))
            conn.commit()

            # Send notification email to the admin
            admin_link = url_for('admin.admin', _external=True)
            msg = Message('New User Registration Awaiting Approval', 
                          recipients=['zoe.flumini@gmail.com'])  # Admin-E-Mail hier einfügen
            msg.body = f'A new user ({username}, {email}) has registered and is awaiting approval. Please review: {admin_link}'
            mail.send(msg)

            conn.close()

            # Redirect to the login page after successful registration
            return redirect(url_for('auth.login'))

        conn.close()

    # Pass the error_message to the template (if any)
    return render_template('register.html', error_message=error_message)


# login
@bp.route('/login', methods=['GET', 'POST'])
def login():
    error_message = None  # Initialize the error message

    if 'user_id' in session:
        return redirect(url_for('main.index'))

    if request.method == 'POST':
        username_or_email = request.form['username_or_email']  # Can be either username or email
        password = request.form['password']
        
        conn = get_db_connection()
        # Check if the user exists and is active
        user = conn.execute('SELECT * FROM users WHERE username = ? OR email = ?', (username_or_email, username_or_email)).fetchone()
        conn.close()

        if user:
            # Check if the password is correct
            if check_password_hash(user['password'], password):
                session['user_id'] = user['id']
                session['username'] = user['username']
                session['is_admin'] = bool(user['is_admin'])  # Convert is_admin to a boolean
                
                if user['is_active'] == -1:
                    return redirect(url_for('main.waiting'))
                elif user['is_active'] == 1:
                    # is_admin, id and username are the names of the database columns from users
                    return redirect(url_for('main.index'))
                else:
                    error_message = "Invalid credentials."
        else:
            # If the user is inactive or doesn't exist
            error_message = "Account is inactive or doesn't exist."

    return render_template('login.html', error_message=error_message)


# logout
@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('main.landing'))


# delete account
@bp.route('/delete', methods=['POST', 'GET'])
def delete_account():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))  # Redirect to login if not logged in



    if request.method == 'POST':
        # Check if 'action' is in the form data
        action = request.form.get('action1')  # Use .get() to avoid KeyError

        if action == 'deactivate':
            # Deactivate account and posts (soft delete)
            conn = get_db_connection()
            conn.execute('UPDATE posts SET is_active = 0 WHERE user_id = ?', (session['user_id'],))
            conn.execute('UPDATE users SET is_active = 0 WHERE id = ?', (session['user_id'],))
            conn.commit()
            conn.close()
            flash('Your account has been deactivated.', 'info')
        
        elif action == 'delete':
            # Permanently delete the user and their posts
            conn = get_db_connection()
            conn.execute('DELETE FROM posts WHERE user_id = ?', (session['user_id'],))
            conn.execute('DELETE FROM users WHERE id = ?', (session['user_id'],))
            conn.commit()
            conn.close()
            flash('Your account has been permanently deleted.', 'info')

        # Clear the session
        session.clear()

        return redirect(url_for('main.landing'))  # Redirect to the landing page

    # For GET requests, render the delete confirmation page
    return render_template('delete.html')


# reset
@bp.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    error_message = None
    if request.method == 'POST':
        email = request.form['email']
        conn = get_db_connection()
        # fetch user by their email
        user = conn.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()
        conn.close()

        if user:
            reset_token = secrets.token_urlsafe(16)
            conn = get_db_connection()
            conn.execute('UPDATE users SET reset_token = ? WHERE email = ?', (reset_token, email))
            conn.commit()
            conn.close()

            # Send reset email
            reset_link = url_for('auth.reset_form', token=reset_token, _external=True)
            msg = Message('Reset your password', recipients=[email])
            msg.body = f'Click the link to reset your password: {reset_link}'
            mail.send(msg)

            flash('A password reset link has been sent to your email.')
            return redirect(url_for('auth.login'))
        # if the email provided does not exist there comes this error message
        error_message = "Email not found!"
    return render_template('reset.html', error_message=error_message)


# reset
@bp.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_form(token):
    # handle the form submission
    if request.method == 'POST':
        new_password = request.form['new_password']
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE reset_token = ?', (token,)).fetchone()

        if user:
            hashed_password = generate_password_hash(new_password)
            conn.execute('UPDATE users SET password = ?, reset_token = NULL WHERE reset_token = ?', (hashed_password, token))
            conn.commit()
            conn.close()

            flash('Password successfully reset. Please log in.')
            return redirect(url_for('auth.login'))
        else:
            flash('Invalid or expired token.')
            return redirect(url_for('forgot_password'))

    return render_template('reset2.html', token=token)


# reactivate
@bp.route('/reactivate_account', methods=['POST', 'GET'])
def reactivate_account():
    error_message = None  # Initialize the error message

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db_connection()

        # Check if the user exists in the users table but is inactive
        inactive_user = conn.execute('SELECT * FROM users WHERE username = ? AND is_active = 0', (username,)).fetchone()

        if inactive_user and check_password_hash(inactive_user['password'], password):
            # Reactivate the user by setting is_active to 1
            conn.execute('UPDATE users SET is_active = 1 WHERE username = ?', (username,))

            # Reactivate all their posts by setting is_active to 1
            conn.execute('UPDATE posts SET is_active = 1 WHERE user_id = ?', (inactive_user['id'],))

            conn.commit()
            conn.close()

            # Log the user in by creating a session
            session['user_id'] = inactive_user['id']
            session['username'] = inactive_user['username']

            return redirect(url_for('main.index'))
        else:
            # Account not found or invalid credentials
            error_message = "Account not found or invalid credentials"
            conn.close()

    # Render the template with or without the error message
    return render_template('reactivate.html', error_message=error_message)