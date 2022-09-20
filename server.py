from flask import Flask, request, render_template, redirect, url_for
from tinydb import TinyDB
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
db = TinyDB("cardsDB.json")
auth = HTTPBasicAuth()

users = {
    "admin": generate_password_hash("admin"),
    "user": generate_password_hash("user")
}

db_items = [
    {"cardholder": "Alice", "cardnum": 4111111111111111, "trips": 10},
    {"cardholder": "Bob", "cardnum": 4111111111111112, "trips": 20},
    {"cardholder": "Carlos", "cardnum": 4111111111111113, "trips": 50},
    {"cardholder": "Oleg", "cardnum": 4111111111111111, "trips": 3},
    {"cardholder": "Robert", "cardnum": 4111111111111112, "trips": 156},
    {"cardholder": "Michele", "cardnum": 4111111111111113, "trips": 5},
    {"cardholder": "Petya", "cardnum": 4111111111111228, "trips": 0},
    {"cardholder": "PSV MASTER", "cardnum": 5555555555555555, "trips": 1000}
]

@auth.verify_password
def verify_password(username, password):
    if username in users and \
            check_password_hash(users.get(username), password):
        return username

@app.route('/index')
@app.route("/", methods=["GET"])
@auth.login_required
def index():
    users = db.all()
    return render_template('bootstrap_table.html', title='SIMPLE TABLE', users=users)

@auth.login_required
@app.route("/add", methods=["POST"])
def add():
    cardholder = request.form.get('cardholder')
    cardnum = request.form.get('cardnum')
    trips = request.form.get('trips')

    db.insert({"cardholder": cardholder, "cardnum": cardnum, "trips": trips})
    return redirect(url_for("index"))

@auth.login_required
@app.route("/update", methods=["POST"])
def change():
    cardholder = request.form.get('cardholder')
    cardnum = request.form.get('cardnum')
    trips = request.form.get('trips')
    doc_id = request.form.get('doc_id')
    _id = int(doc_id)

    db.update({"cardholder": cardholder, "cardnum": cardnum, "trips": trips}, doc_ids=[_id])
    return redirect(url_for("index"))

@auth.login_required
@app.route("/delete", methods=["POST"])
def delete():
    doc_id = request.form.get('doc_id')
    _id = int(doc_id)
    db.remove(doc_ids=[_id])
    return redirect(url_for("index"))

if __name__ == "__main__":
    db.truncate()
    db.insert_multiple(db_items) 
    app.run()