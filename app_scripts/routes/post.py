from app_scripts.database import get_db_connection
from flask import Blueprint, current_app, render_template, request, redirect, session, url_for
import os
from werkzeug.utils import secure_filename

bp = Blueprint("post", __name__)


# helperfunction
UPLOAD_FOLDER = 'static/uploads/'
ALLOWED_EXTENSIONS = {'png'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# ensures that the has_post-variable is used globally and for all the templates and views
@bp.context_processor
def inject_has_post():
    if 'user_id' in session:
        conn = get_db_connection()
        user_post = conn.execute('SELECT * FROM posts WHERE user_id = ?', (session['user_id'],)).fetchone()
        conn.close()
        # if there is something in the users table that means that the corresponding user already has a post
        has_post = user_post is not None
    else:
        has_post = False

    return dict(has_post=has_post)


# CREATE A POST
@bp.route('/post', methods=['GET', 'POST'])
def post():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    conn = get_db_connection()

    # Get the user information, including 'is_active' status
    user = conn.execute('SELECT * FROM users WHERE id = ?', (session['user_id'],)).fetchone()

    # If the user is inactive and awaiting approval, redirect them to the waiting page
    if user['is_active'] == -1:
        conn.close()
        return redirect(url_for('main.waiting'))

    # in dieser variable werden alle daten des posts der eingeloggten person gespeichert!
    user_post = conn.execute('SELECT * FROM posts WHERE user_id = ?', (session['user_id'],)).fetchone()
    
    if request.method == 'POST':
        # Handle the "Abbrechen" button first
        if 'abbrechen' in request.form:
            if user_post:
                conn.execute('DELETE FROM posts WHERE user_id = ?', (session['user_id'],))
                conn.commit()
            conn.close()
            return redirect(url_for('main.index'))

        # save the input-information submitted into the form in a variable: 'content' is the name of the textfield of the form
        # es existiert eine variable für jedes inputfeld des forms (ausser für das image nicht!)
        content = request.form['content']
        bday = request.form['bday'] 
        color = request.form['favcolor']
        food = request.form['Food']
        redFlag = request.form['rFlag']
        greenFlag = request.form['gFlag']
        pinterest = request.form['Pinterest']
        name = request.form['name']
        personnality = request.form['personnality']
        zoe = request.form['zoe']
        interest = request.form['interest']
        desinterest = request.form['desinterest']
        lernen = request.form['lernen']
        idol = request.form['idol']
        serie = request.form['serie']
        musik = request.form['musik']
        fashion = request.form['fashion']
        zukunft = request.form['zukunft']
        love = request.form['love']
        date = request.form['date']
        pleasure = request.form['pleasure']
        regret = request.form['regret']
        party_movie = request.form.get('party_movie')
        ski_snowboard = request.form.get('ski_snowboard')
        wg_alleine = request.form.get('wg_alleine')
        hund_katze = request.form.get('hund_katze')
        regen_sonne = request.form.get('regen_sonne')
        spotify = request.form.get('spotify')


        # Handle the file upload
        if 'image' in request.files:
            file = request.files['image']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
                file.save(file_path)
            else:
                file_path = None
        else:
            file_path = None  # No image uploaded

        
        # falls noch kein post existiert...
        # Create new post with image path
        # INSERT: Spaltenname in der Datenbank
        # VALUES: Variablen
        # Adjust the form field variable names and column names
        conn.execute('''
            INSERT INTO posts (
                user_id, content, birthday, color, food, redFlags, greenFlags, pinterest, name, personnality, zoe, interest, 
                desinterest, lernen, idol, serie, musik, fashion, zukunft, love, date, pleasure, regret, party_movie, 
                ski_snowboard, wg_alleine, hund_katze, regen_sonne, spotify, image_path
            ) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            session['user_id'], content, bday, color, food, redFlag, greenFlag, pinterest, name, personnality, zoe, 
            interest, desinterest, lernen, idol, serie, musik, fashion, zukunft, love, date, pleasure, regret, 
            party_movie, ski_snowboard, wg_alleine, hund_katze, regen_sonne, spotify, file_path
        ))

        conn.commit()
        conn.close()
        return redirect(url_for('main.index'))


    conn.close()

    # Render the appropriate template based on whether the user has a post
    if user_post:
        return render_template('edit_post.html', post=user_post)
    else:
        return render_template('post.html')


# das template wo man einen post bearbeitet wenn man bereits einen hat
@bp.route('/edit_post', methods=['GET', 'POST'])
def edit_post():
    # wenn der user nicht eingeloggt ist dann wird man zur login-page gelinkt
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    conn = get_db_connection()

    # Get the user information, including 'is_active' status
    user = conn.execute('SELECT * FROM users WHERE id = ?', (session['user_id'],)).fetchone()

    # If the user is inactive and awaiting approval, redirect them to the waiting page
    if user['is_active'] == -1:
        conn.close()
        return redirect(url_for('main.waiting'))

    # der post des eingeloggten users werden "geholt" (wenn nichts drin ist dann ist post = None)
    post = conn.execute('SELECT * FROM posts WHERE user_id = ?', (session['user_id'],)).fetchone()

    # Calculate whether the user has a post (used for the "Edit Post"/"Create Post" button)
    # nur die user die bereits einen post haben können ihn editet (onst wird die create-function aufgerufen!)
    has_post = post is not None

    # if something was posted
    if request.method == 'POST':
        # if the update-button gets clicked
        if 'update' in request.form:
            # the updated content is stored in a variable
            content = request.form['content']
            bday = request.form['bday'] 
            color = request.form['favcolor']
            food = request.form['Food']
            redFlag = request.form['rFlag']
            greenFlag = request.form['gFlag']
            pinterest = request.form['Pinterest']
            name = request.form['name']
            personnality = request.form['personnality']
            zoe = request.form['zoe']
            interest = request.form['interest']
            desinterest = request.form['desinterest']
            lernen = request.form['lernen']
            idol = request.form['idol']
            serie = request.form['serie']
            musik = request.form['musik']
            fashion = request.form['fashion']
            zukunft = request.form['zukunft']
            love = request.form['love']
            date = request.form['date']
            pleasure = request.form['pleasure']
            regret = request.form['regret']
            party_movie = request.form.get('party_movie')
            ski_snowboard = request.form.get('ski_snowboard')
            wg_alleine = request.form.get('wg_alleine')
            hund_katze = request.form.get('hund_katze')
            regen_sonne = request.form.get('regen_sonne')
            spotify = request.form.get('spotify')


            # Initialize image path as None
            file_path = None

            # if an image is uploaded
            if 'image' in request.files:
                file = request.files['image']
                
                # Check if the file is allowed and has a filename
                if file and allowed_file(file.filename):
                    # Secure the filename and save the new image
                    filename = secure_filename(file.filename)
                    file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
                    file.save(file_path)
                    print(f"New image uploaded: {file_path}")  # Debugging print

                    # Optional: Remove old image if a new one is uploaded
                    if post and post['image_path']:
                        old_image_path = post['image_path']
                        if os.path.exists(old_image_path):
                            os.remove(old_image_path)
                            print(f"Old image removed: {old_image_path}")  # Debugging print

                else:
                    file_path = post['image_path']  # Keep old image if no new image uploaded
                    print("No new image uploaded, keeping the old image.")

            else:
                file_path = post['image_path']  # Keep old image if no new image uploaded
                print("No image uploaded at all, retaining current image.")

            # Update the post with the new content and the (new or old) image path
            # content = ? (content is the column name of the database) and the other content in the brackets after where is a variable
            conn.execute('''
                UPDATE posts 
                SET content = ?, birthday = ?, color = ?, redFlags = ?, greenFlags = ?, food = ?, pinterest = ?, 
                    name = ?, personnality = ?, zoe = ?, interest = ?, desinterest = ?, lernen = ?, idol = ?, 
                    serie = ?, musik = ?, fashion = ?, zukunft = ?, love = ?, date = ?, pleasure = ?, regret = ?, 
                    party_movie = ?, ski_snowboard = ?, wg_alleine = ?, hund_katze = ?, regen_sonne = ?, 
                    spotify = ?, image_path = ?
                WHERE user_id = ? 
            ''', (
                content, bday, color, redFlag, greenFlag, food, pinterest, name, personnality, zoe, interest, 
                desinterest, lernen, idol, serie, musik, fashion, zukunft, love, date, pleasure, regret, party_movie, 
                ski_snowboard, wg_alleine, hund_katze, regen_sonne, spotify, file_path, session['user_id']
            ))
            conn.commit()
            conn.close()
            print("Post updated in the database.")  # Debugging print
            return redirect(url_for('main.index'))

        # if the delete-button gets clicked
        elif 'delete' in request.form:
            print("Delete button clicked")  # Debugging print
            # Delete the post
            conn.execute('DELETE FROM posts WHERE user_id = ?', (session['user_id'],))
            conn.commit()
            conn.close()
            print("Post deleted.")  # Debugging print
            return redirect(url_for('main.index'))


    conn.close()
    
    # Pass `has_post` along with the post to the template
    return render_template('edit_post.html', post=post, has_post=has_post)


# einzelne posts zum durchklicken
# NEW FUNCTION: Display a single post with forward/backward navigation
@bp.route('/buchseiten/<username>', methods=['GET'])
def show_post(username):
    conn = get_db_connection()
    
    # Get active user by username
    user = conn.execute('SELECT * FROM users WHERE username = ? AND is_active = 1', (username,)).fetchone()
    
    if not user:
        conn.close()
        return "User not found or inactive", 404


    # Fetch the user's post
    post = conn.execute('SELECT * FROM posts WHERE user_id = ? AND is_active = 1', (user['id'],)).fetchone()

    # Get all active usernames for navigation
    users = conn.execute('SELECT username FROM users WHERE is_active = 1 ORDER BY username').fetchall()
    conn.close()

    # Prepare navigation links
    usernames = [u['username'] for u in users]
    current_index = usernames.index(username)
    next_username = usernames[current_index + 1] if current_index < len(usernames) - 1 else None
    prev_username = usernames[current_index - 1] if current_index > 0 else None

    return render_template('userpage.html', post=post, username=username, prev_username=prev_username, next_username=next_username)
