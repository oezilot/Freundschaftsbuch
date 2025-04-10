# html-pages where not really much happens and the main page

# helperfunctions
from app_scripts.database import get_db_connection

# python libraries
from flask import Blueprint, render_template, redirect, session, url_for

# blueprnt
bp = Blueprint('main', __name__)


# ------------------------------
# |        stativ pages        | 
# ------------------------------

# ------------------ landing.html
@bp.route('/')
def landing():
    # If the user is logged in, redirect them to the main index page
    if 'user_id' in session:
        return redirect(url_for('index'))        
    
    # If the user is not logged in, show the landing page
    return render_template('landing.html')

# ------------------ about.html
@bp.route('/about')
def about():
    return render_template('about.html')

# ------------------ waiting.html
@bp.route('/waiting')
def waiting():
    return render_template('waiting.html')


# --------------------------
# |        main page       | 
# --------------------------

# ------------------ index.html
@bp.route('/buchseiten/inhaltsverzeichnis')
def index():
    conn = get_db_connection()

    if 'user_id' not in session:
        user_post = None
        has_post = False
    else:
        user_post = conn.execute('SELECT * FROM posts WHERE user_id = ? AND is_active = 1', (session['user_id'],)).fetchone()
        has_post = user_post is not None

    # Query to get all active users (admins and normal users separately)
    admins = conn.execute('SELECT username FROM users WHERE is_active = 1 AND is_admin = 1 ORDER BY username ASC').fetchall()
    users = conn.execute('SELECT username FROM users WHERE is_active = 1 AND is_admin = 0 ORDER BY username ASC').fetchall()

    # Get admin posts
    admin_posts = []
    for admin in admins:
        post = conn.execute('SELECT content, created_at FROM posts WHERE user_id = (SELECT id FROM users WHERE username = ?) AND is_active = 1', (admin['username'],)).fetchone()
        admin_posts.append({
            'username': admin['username'],
            'content': post['content'] if post else None,
            'created_at': post['created_at'] if post else None
        })

    # Get non-admin user posts
    user_posts = []
    for user in users:
        post = conn.execute('SELECT content, created_at FROM posts WHERE user_id = (SELECT id FROM users WHERE username = ?) AND is_active = 1', (user['username'],)).fetchone()
        user_posts.append({
            'username': user['username'],
            'content': post['content'] if post else None,
            'created_at': post['created_at'] if post else None
        })

    # Initialize the all_posts list
    all_posts = []

    # Add admin posts to all_posts
    for admin in admins:
        post = conn.execute('SELECT content, created_at FROM posts WHERE user_id = (SELECT id FROM users WHERE username = ?) AND is_active = 1', (admin['username'],)).fetchone()
        all_posts.append({
            'username': admin['username'],
            'content': post['content'] if post else None,
            'created_at': post['created_at'] if post else None,
            'is_admin': True  # Add a flag to indicate this is an admin post
        })

    # Add user posts to all_posts
    for user in users:
        post = conn.execute('SELECT content, created_at FROM posts WHERE user_id = (SELECT id FROM users WHERE username = ?) AND is_active = 1', (user['username'],)).fetchone()
        all_posts.append({
            'username': user['username'],
            'content': post['content'] if post else None,
            'created_at': post['created_at'] if post else None,
            'is_admin': False  # Add a flag to indicate this is a normal user post
        })
    # Now all_posts contains both admin and user posts
    all_posts.sort(key=lambda x: x['username'].lower())

    conn.close()

    return render_template('index.html', admin_posts=admin_posts, user_posts=user_posts, has_post=has_post, all_posts=all_posts)