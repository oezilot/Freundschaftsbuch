# dieses skript verient alle blueprints der routen miteinader und dem init der datenbank und der app, mail und session objekts

# python librares/objects
from dotenv import load_dotenv
import os
from flask import Flask

# blueprints (files from the app_scriptsfolder)
from app_scripts.extensions import mail # this is not a blueprint but the rest is (mail is importet to use like a funtion)
from app_scripts.database import init_db # this is not a blueprint but the rest is (mail is importet to use like a funtion)
from app_scripts.routes.admin import bp as admin_bp
from app_scripts.routes.auth import bp as auth_bp
from app_scripts.routes.post import bp as post_bp
from app_scripts.routes.main import bp as main_bp

load_dotenv()

def create_app():

    # create the app
    app = Flask(__name__)
    app.secret_key = "secret_key"

    # mail config
    app.config['MAIL_SERVER']= os.getenv('MAIL_SERVER')
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
    app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USE_SSL'] = False
    app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_DEFAULT_SENDER') # diese account sendet alle emails

    # initialize mail with the specified config
    mail.init_app(app)

    # den ordner definieren wo dann alle files hingelangen die auf die website geladen werdn (von der datenbank)
    app.config['UPLOAD_FOLDER'] = 'static/uploads/'

    # init database (datenbank kreieren oder so lasen wenn sie bereits existiert)
    init_db()

    # Register routes (but keep route logic hidden in other files)
    app.register_blueprint(admin_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(post_bp)
    app.register_blueprint(main_bp)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, port=8080)


''' fragen
- sollte ich nicht ein vriable initialisieren die für die datenbank steht?
- wo initialisiere ich das session-objekt?
'''