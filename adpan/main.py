from flask import Flask, redirect, url_for
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_admin.theme import Bootstrap4Theme
from flask_babel import Babel
from flask_sqlalchemy import SQLAlchemy


def main(debug=False):
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "narainthegoatandkrishnathegoat"

    babel = Babel(app)

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///../library.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db = SQLAlchemy(app)

    with app.app_context():
        db.metadata.reflect(bind=db.engine)

    class_dict = {}

    for table_name, table in db.metadata.tables.items():
        cls = type(table_name.capitalize(), (db.Model,), {"__table__": table})
        class_dict[table_name] = cls

    admin = Admin(app, name="Admin Panel", theme=Bootstrap4Theme(swatch="darkly"))

    aliases = {
        "auth": "Superusers",
        "book_type": "Book Type",
        "books": "Books",
        "members": "Our Members",
        "borrowhistory": "Borrow History",
    }

    def create_view(table_model, db_session, name=None, **kwargs):
        """
        Function that displays Primary Keys and Foreign Keys and makes them editable.
        """

        columns = [col.name for col in table_model.__table__.columns]

        class DynamicModelView(ModelView):
            column_list = columns
            form_columns = columns

        return DynamicModelView(table_model, db_session, name=name, **kwargs)

    for table_name, model_class in class_dict.items():
        display_name = aliases.get(table_name, table_name.capitalize())
        view = create_view(model_class, db.session, name=display_name)
        admin.add_view(view)

    @app.route("/")
    def index():
        return redirect(url_for("admin.index"))

    app.run(debug=debug)


if __name__ == "__main__":
    main(debug=True)
