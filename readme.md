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
- .env file

app functionality:
- email notification problem (new email server)
- email notification when i accepted someone

file structure:
- better file structure
- api
- riesiges skript in mehrere kleinere aufteilen

coding style:
- more beautiful code

api? (jeder kann sein eigenes freundschaftsbuch machen mit gewissen parametern)

app für den app store

andere features:
- sprache ändern
- piselbilder generieren oder malen mit built-in drawing tool

tests!

readme mit explanation

try out my own css framework or just a different one

addextras like a pixelmonitor to draw and make illustrations

spread publicity


## used libraries an pricipals
- https://pypi.org/project/Flask-Mail/
- https://flask-mail.readthedocs.io/en/latest/ 
- https://mailtrap.io/blog/flask-email-sending/ (i used mailtrap for sending emails)
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