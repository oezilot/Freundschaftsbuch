from flask import Blueprint, render_template, request, redirect, session, url_for
from app_scripts.database import get_db_connection
from app_scripts.extensions import mail
from flask_mail import Message

bp = Blueprint('admin', __name__)

#admin-account: only the admin can access this page (admin is the user with id=1)
@bp.route('/admin', methods=['GET', 'POST'])
def admin():
    # Check if the user is logged in and is an admin
    if 'user_id' in session:
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE id = ?', (session['user_id'],)).fetchone()
        
        active_users = conn.execute('SELECT * FROM users WHERE is_active = 1 AND is_admin = 0').fetchall()
        inactive_users = conn.execute('SELECT * FROM users WHERE is_active = 0 AND is_admin = 0').fetchall()
        waiting_users = conn.execute('SELECT * FROM users WHERE is_active = -1 AND is_admin = 0').fetchall() # only use fetchone or fetchall when returning something!
        admin_accounts = conn.execute('SELECT * FROM users WHERE is_admin = 1').fetchall()

        # Handle the form submission for approving or denying users (database-level)
        if request.method == 'POST':
            user_id = request.form['user_id']  # Get the user_id from the form
            action = request.form['action']  # Get the action (approve/deny) from the button clicked
            email = conn.execute('SELECT email FROM users WHERE id = ?', (user_id,)).fetchone()['email']
            link_personal_page = url_for('main.index', _external=True)
            link_admin = url_for('admin.admin', _external=True)

            if action == 'activate':
                conn.execute('UPDATE users SET is_active = 1 WHERE id = ?', (user_id,))
                # mail to the user
                msg = Message(subject='Account Registration at freundschaftsbuch', body=f'Your Account has been activated, thanks so much for subscribing! This is the beginnig of a real freindship!, Link to your page: {link_personal_page}', recipients=[f'{email}'])
                mail.send(msg)

            if action == 'deactivate':
                conn.execute('UPDATE users SET is_active = 0 WHERE id = ?', (user_id,))
                msg = Message(subject='Account Registration at freundschaftsbuch', body=f'Your Account has been deactivated', recipients=[f'{email}'])
                mail.send(msg)

            if action == 'delete':
                conn.execute('DELETE FROM users WHERE id = ?', (user_id,))
                msg = Message(subject='Account Registration at freundschaftsbuch', body=f'Your Account has been deleted', recipients=[f'{email}'])
                mail.send(msg)

            if action == 'promote':
                conn.execute('UPDATE users SET is_admin = 1 WHERE id = ?', (user_id,))
                msg = Message(subject='Account Registration at freundschaftsbuch', body=f'Your Account has been promoted, explore admin rights here: {link_admin}', recipients=[f'{email}'])
                mail.send(msg)

            if action == 'depromote':
                conn.execute('UPDATE users SET is_admin = 0 WHERE id = ?', (user_id,))
                msg = Message(subject='Account Registration at freundschaftsbuch', body=f'Your Account has been depromoted!', recipients=[f'{email}'])
                #mail.send(msg)

            conn.commit()  # Save the changes to the database
            return redirect(url_for('admin.admin'))  # Refresh the admin page after changes
        
        conn.close()

        # If the user is an admin, render the admin page
        # is_admin is a boolean therefore when it is true this case gets runned (if user['is_admin] is the same as if the user has a true in the column admin)
        if user and user['is_admin']:
            return render_template('admin.html', inactive_users=inactive_users, active_users=active_users, waiting_users=waiting_users, admin_accounts=admin_accounts)
        else:
            # If the user is not an admin, show an unauthorized message
            return "Unauthorized access", 403
    else:
        return redirect(url_for('auth.login'))