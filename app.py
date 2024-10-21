import sqlite3
import time
from flask import Flask, g, request, jsonify, send_from_directory

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
    return send_from_directory('', 'index.html')

@app.route("/expenses")
def expenses():
    cur = get_db().cursor()
    cur.execute("SELECT * FROM expenses ORDER BY timestamp;")
    return jsonify(cur.fetchall())

@app.route("/add", methods=["POST"])
def add():
    data = request.get_json()
    cur = get_db().cursor()
    cur.execute("INSERT INTO expenses (timestamp, amount, description, category) VALUES (?, ?, ?, ?)",
                (int(time.time()), data['amount'], data['description'], data['category']))
    return {"success": True}, 201

if __name__ == "__main__":
    with get_db() as db:
        db.execute("""
            CREATE TABLE IF NOT EXISTS expenses (
                timestamp INTEGER,
                amount INTEGER,
                description TEXT,
                category TEXT
            )
        """)
    app.run(debug=True)
