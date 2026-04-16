import os

from flask import Flask, redirect, url_for
from flask_admin import Admin, AdminIndexView, expose
from flask_admin.contrib.sqla import ModelView
from flask_admin.theme import Bootstrap4Theme
from flask_babel import Babel
from flask_sqlalchemy import SQLAlchemy


class MyIndexView(AdminIndexView):
    @expose("/")
    def index(self):
        return self.render("admin/index.html")


def main(debug=False):
    template_folder = os.path.join(os.path.dirname(__file__), "templates")
    static_folder = os.path.join(os.path.dirname(__file__), "static")

    app = Flask(
        __name__,
        template_folder=template_folder,
        static_folder=static_folder,
    )
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

    admin = Admin(
        app,
        name="Admin Panel",
        theme=Bootstrap4Theme(swatch="flatly"),
        index_view=MyIndexView(name="Home", template="admin/index.html", url="/admin"),
    )

    book_type = class_dict["book_type"]
    books = class_dict["books"]
    borrowhistory = class_dict["borrowhistory"]
    members = class_dict["members"]
    superusers = class_dict["superuser"]

    class BookTypeView(ModelView):
        column_list = (
            "isbn",
            "title",
            "author",
            "genre",
            "date_published",
            "latest_revision",
        )
        form_columns = (
            "isbn",
            "title",
            "author",
            "genre",
            "date_published",
            "latest_revision",
        )
        column_labels = {
            "isbn": "ISBN",
            "title": "TITLE",
            "author": "AUTHOR",
            "genre": "GENRE",
            "date_published": "DATE PUBLISHED",
            "latest_revision": "LATEST REVISION",
        }
        column_searchable_list = ["title", "author", "genre"]
        # column_filters = ["genre"]


    class BooksView(ModelView):
        column_list = ("book_id", "isbn", "condition")
        form_columns = ("book_id", "isbn", "condition")
        column_labels = {
            "book_id": "BOOK ID",
            "isbn": "ISBN",
            "condition": "CONDITION",
        }


    class BorrowHisView(ModelView):
        column_list = (
            "borrow_id",
            "book_id",
            "member_id",
            "issued_at",
            "issuer_id",
            "due_by",
        )
        form_columns = (
            "borrow_id",
            "book_id",
            "member_id",
            "issued_at",
            "issuer_id",
            "due_by",
        )
        column_labels = {
            "borrow_id": "BORROW ID",
            "book_id": "BOOK ID",
            "member_id": "MEMBER ID",
            "issued_at": "ISSUED AT",
            "issuer_id": "ISSUER ID",
            "due_by": "DUE BY",
        }


    class MembersView(ModelView):
        column_list = ("member_id", "name", "email", "phone_number", "member_since")
        form_columns = (
            "member_id",
            "name",
            "email",
            "phone_number",
            "member_since",
        )
        column_labels = {
            "member_id": "MEMBER ID",
            "name": "NAME",
            "email": "EMAIL",
            "phone_number": "PHONE NUMBER",
            "member_since": "MEMBER_SINCE",
        }
        column_searchable_list = ["name", "email", "phone_number"]


    class SuperusersView(ModelView):
        column_list = (
            "user_id",
            "username",
            "email",
            "salt",
            "password_hash",
            "role",
        )
        form_columns = (
            "user_id",
            "username",
            "email",
            "salt",
            "password_hash",
            "role",
        )
        column_labels = {
            "user_id": "USER ID",
            "username": "USERNAME",
            "email": "EMAIL",
            "salt": "SALT",
            "password_hash": "PASSWORD HASH",
            "role": "ROLE",
        }
        column_searchable_list = ["username", "email"]


    admin.add_view(BookTypeView(book_type, db.session, name="Book Types"))
    admin.add_view(BooksView(books, db.session, name="Books"))
    admin.add_view(BorrowHisView(borrowhistory, db.session, name="Borrow History"))
    admin.add_view(MembersView(members, db.session, name="Our Members"))
    admin.add_view(SuperusersView(superusers, db.session, name="Superusers"))

    @app.route("/")
    def index():
        return redirect(url_for("admin.index"))

    app.run(debug=debug)


if __name__ == "__main__":
    main(debug=True)
