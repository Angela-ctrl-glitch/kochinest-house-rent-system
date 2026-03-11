from flask import Flask, render_template, request, redirect, session
import sqlite3
import pandas as pd

app = Flask(
    __name__,
    template_folder="../frontend/templates",
    static_folder="../frontend/static"
)

app.secret_key = "secret123"


# DATABASE CONNECTION
def get_db():
    conn = sqlite3.connect("../database/database.db")
    conn.row_factory = sqlite3.Row
    return conn


# LOGIN PAGE
@app.route("/")
def login():
    return render_template("login.html")


# LOGIN CHECK
@app.route("/login", methods=["POST"])
def check_login():
    email = request.form["email"]
    password = request.form["password"]

    db = get_db()
    user = db.execute(
        "SELECT * FROM users WHERE email=? AND password=?",
        (email, password)
    ).fetchone()

    if user:
        session["user"] = user["name"]
        return redirect("/dashboard")

    return "Invalid Login"


# REGISTER
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        phone = request.form["phone"]
        password = request.form["password"]

        db = get_db()
        db.execute(
            "INSERT INTO users(name,email,phone,password) VALUES (?,?,?,?)",
            (name, email, phone, password)
        )
        db.commit()

        return redirect("/")

    return render_template("register.html")


# DASHBOARD
@app.route("/dashboard")
def dashboard():
    username = session.get("user")
    return render_template("dashboard.html", username=username)


# ADD HOUSE
@app.route("/add_house", methods=["GET", "POST"])
def add_house():
    if request.method == "POST":
        house = request.form["house"]
        place = request.form["place"]
        price = request.form["price"]
        rooms = request.form["rooms"]

        db = get_db()
        db.execute(
            "INSERT INTO houses(house_name,place,price,rooms,status) VALUES (?,?,?,?,?)",
            (house, place, price, rooms, "Available")
        )
        db.commit()

        return redirect("/dashboard")

    return render_template("add_house.html")


# VIEW HOUSES
@app.route("/view_houses")
def view_houses():
    db = get_db()
    houses = db.execute("SELECT * FROM houses").fetchall()
    return render_template("view_houses.html", houses=houses)


# ✅ RENT DUE REMINDER (FIXED)
@app.route("/rent_due", methods=["GET", "POST"])
def rent_due():
    db = get_db()

    # ADD RENT REMINDER
    if request.method == "POST":
        tenant = request.form["tenant"]
        email = request.form["email"]
        house = request.form["house"]
        amount = request.form["amount"]
        due_date = request.form["due_date"]
        status = request.form["status"]

        db.execute(
            """
            INSERT INTO rent_due
            (tenant_name, email, house_name, rent_amount, due_date, status)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (tenant, email, house, amount, due_date, status)
        )
        db.commit()

        return redirect("/rent_due")

    # SHOW RENT RECORDS
    rents = db.execute("SELECT * FROM rent_due ORDER BY due_date ASC").fetchall()
    return render_template("rent_due.html", rents=rents)


# SEARCH STAY
@app.route("/search", methods=["GET", "POST"])
def search():
    stays = None

    if request.method == "POST":
        area = request.form["place"]
        df = pd.read_excel("../dataset/kochi_house_rent_40_real_names.xlsx")
        stays = df[df["Area"].str.contains(area, case=False, na=False)]

    return render_template("search_stay.html", stays=stays)


# BOOK STAY
@app.route("/book", methods=["GET", "POST"])
def book():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        phone = request.form["phone"]
        place = request.form["place"]
        stay = request.form["stay"]
        duration = request.form["duration"]
        price = request.form["price"]

        db = get_db()
        db.execute(
            "INSERT INTO booking(name,email,phone,place,stay_name,duration,price) VALUES (?,?,?,?,?,?,?)",
            (name, email, phone, place, stay, duration, price)
        )
        db.commit()

        return "Booking Confirmed!"

    return render_template("booking.html")


if __name__ == "__main__":
    app.run(debug=True)