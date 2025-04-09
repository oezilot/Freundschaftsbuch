# dieses skript verient alle anderen python files und muss gerunnt werden!

# python libraries
from flask import Flask, render_template, request, redirect, session, url_for, flash

# my own python scripts


app = Flask(__name__)
app.secret_key = 'secret_key' # For session management (damit man sich einloggen kann braucht es einen secret key!)

if __name__ == '__main__':
    app.run(debug=True)
