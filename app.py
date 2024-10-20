import sqlite3

from flask import Flask, g

app = Flask(__name__)


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect("personal_finance.db", autocommit=True)
    return g.db


@app.teardown_appcontext
def teardown_db(exception):
    db = g.pop("db", None)

    if db is not None:
        db.close()


@app.route("/")
def index():
    return open("index.html")


@app.route("/expenses")
def expenses():
    cur = get_db().cursor()
    cur.execute("SELECT * FROM expenses ORDER BY timestamp;")
    return cur.fetchall()


@app.route("/add", methods=["POST"])
def add():
    # YOUR CODE HERE
    pass
