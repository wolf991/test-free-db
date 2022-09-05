import os
from flask import Flask, render_template, request, redirect
from sqla_wrapper import SQLAlchemy

app = Flask(__name__)

# the replace method is needed due to this issue: https://help.heroku.com/ZKNTJQSK/why-is-sqlalchemy-1-4-x-not-connecting-to-heroku-postgres
db_url = os.getenv("DATABASE_URL", "sqlite:///db.sqlite").replace("postgres://", "postgresql://", 1)
db = SQLAlchemy(db_url)


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String, unique=False)
    text = db.Column(db.String, unique=False)


db.create_all()


@app.route("/", methods=["GET"])
def index():
    messages = db.query(Message).all()

    return render_template("index.html", messages=messages)


@app.route("/add-message", methods=["POST"])
def add_message():
    username = request.form.get("username")
    text = request.form.get("text")

    message = Message(author=username, text=text)
    message.save()

    return redirect("/")


if __name__ == "__main__":
    app.run(use_reloader=True)
