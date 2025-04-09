# this script just sends an email using the new configuration with mailtrap and oezilot.ch
# tsting emails with: https://mailtrap.io/inboxes/3597981/messages 
# setting up domain on mailtrap for poduction: ...

from flask import Flask, render_template, request, redirect, session, url_for, flash
from flask_mail import Mail, Message # Mail und Message sind Klassen


# init flask app
app = Flask(__name__)

# using mailtraps testig functionality here...
app.config['MAIL_SERVER']='live.smtp.mailtrap.io'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'api'
app.config['MAIL_PASSWORD'] = 'd434f80ac59fd887432881fe0a0fffd7'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_DEFAULT_SENDER'] = 'freundschaftsbuch@oezilot.ch' # diese account sendet alle emails

mail = Mail(app)

def send_mail(content, subject, receivers): # string, liste von strings
    message = Message(
        subject=subject, 
        #sender= # steht bereits im config drin
        recipients=receivers, 
        body=content
    )
    mail.send(message)

# function to send an email
@app.route("/")
def send_test_mail():

    # funktion aufrufen
    send_mail("iiiii omg Papa lug mal was ich gschafft han, diheime tuen ich denn de richtigi mailserver iirichte ich freu mich scho ich han alli nix-files scho iigrichtet iiiiiiiiiiiii", "Fruits", ["zoe.flumini@gmail.com", "DandoloFlumini@gmail.com"])

    # das was man returned wird dann im html im browser angezeigt! # the routes just is what triggers the functions!
    return "Email send successfully!"


# launches the flask server (listens to localhost:portnumber, returns http-responses, calls route functions (htps-responses --> it is a small websever))
if __name__ == "__main__":
    app.run(debug=True, port=8080)