## run the app
```bash

```

## changes for the refactor to happen

compatibilities:
- mobile version

transfer:
- database synchronisation

design:

security:
- hack sicher (sql incections)

app functionality:
- email notification problem (new email server) -> domain muss noch trandferiert werden!

coding style:
- more beautiful code

uploads ordner:
- wenn jemand seinen post löscht muss das zugehörige bild auch im ploads ordner gelöscht werden!

api? (jeder kann sein eigenes freundschaftsbuch machen mit gewissen parametern)

app für den app store

andere features:
- sprache ändern
- pixelbilder generieren oder malen mit built-in drawing tool

tests!

all design verbesserungen (freunden etc fragen)

readme mit explanation

bei der errorwolkle das login/register feld ausblenden und stattdessen eine button machen try again

try out my own css framework or just a different one

addextras like a pixelmonitor to draw and make illustrations

spread publicity

admin account nicht als seperates scriptp und eine freundschaftsbuch mail-adresse


## used libraries an pricipals
- https://pypi.org/project/Flask-Mail/
- https://flask-mail.readthedocs.io/en/latest/ 
- https://mailtrap.io/blog/flask-email-sending/ (i used mailtrap for sending emails)
- good css help: https://developer.mozilla.org/en-US/docs/Web/CSS/word-spacing 
- email-records on cloudflare:
![alt text](image.png)


## all parts of the huge insane file:
- mail config
- init objects and database
- admin (route /admin)
- landing (/landing) index (/index) about(/about)
- login (/login) logout register (/register) delete_account reactivate_account
- waiting (/waiting)
- show_post post edit_post
- inject_has_post
- reset_password reset_form
- run.py


## mein code unter der lupe
- redirect(url_for('login')) = redirect('/login') --> tells flask to issue a redirect to the specified path
- url_for('login') -> looks up the url-path for the route function called login(), the template which the route-function renders wih render_tamplate
- render_template('login.html')

## key cncepts i have learned
Python Flask Library
- http-requests to certain routes is what triggers the route-functions, their return will be displayed on an html as the response

HTML
- ....

## meine errors und was man dagegen tun kann
- blueprint nicht richtig gehandelt mit den filenamen --> raise BuildError(endpoint, values, method, self)
werkzeug.routing.exceptions.BuildError: Could not build url for endpoint 'index'. Did you mean 'main.index' instead?


## bugs (todo)
- das base.html wird nicht geladen


## fragen
- wie funktioniert eigenlich django?











## test all possible functionalities on the site!
- reigster
- login
- logout
- delete account
- deactivate account (und alles was dann der fall sein muss wie nicht einloggen können oder dass der post nicht erscheint)
- reactivate account
- alle htmls und css wird schön angezeigt
- ein post entsteht wenn ein user hinzugefügt wird
- promote to admin
- deny
- accept
- create an admin account
- edit post create post delete post
- abbrechen des posts
- mails
- reset password/change passwort (nur accounts die existieren können ihr passwort resetten, inaktive oder nicht existieende können das nicht)

bugs: wenn jemand mit einem inaktiven acc sein passwort ändert dann kann dieser user sich mit dem alten passwort einloggen

folgendes muss verbessert werden:
- mail notification wenn ich jemanden accepte oder lösche etc (accepted, deied, deleted, promoted)
- beim löschen eines accounts etwas lustiges einbauen wie ein sades gesicht und noch fragen ob man wirklich sein account löschen will
- regex für die emails, es muss eine email sein
- wenn man einen post bearbeiten will auch die option abbrechen bereitstelen