from flask import Flask
from flask_admin import Admin
from flask_admin.theme import Bootstrap4Theme

app = Flask(__name__)

admin = Admin(app, name="microblog", theme=Bootstrap4Theme(swatch="darkly"))


app.run()
