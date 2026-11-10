from flask import Blueprint, render_template, request, redirect, url_for, flash
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint("auth", __name__)

# Database Connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="mohan123",
    database="project"
)

cursor = db.cursor()

# ==========================
# Entry Page
# ==========================
# 
@auth.route("/")
def selection():
    print("Reached selection route")
    return render_template("entry.html")

# ==========================
# Admin / Employee Login Page
# ==========================
@auth.route("/admin-login")
@auth.route("/employee-login")
def admin_login():
    return render_template("login.html")


# ==========================
# Admin Register Page
# ==========================
@auth.route("/register_page")
def register_page():
    return render_template("register.html")


# ==========================
# Register Admin
# ==========================
# ==========================
# Register Admin
# ==========================

@auth.route("/register", methods=["POST"])
def register():

    try:
        # Get form data
        username = request.form["username"]
        password = request.form["password"]
        email = request.form["email"]
        phone = request.form["phone"]

        # Check if username already exists
        cursor.execute(
            "SELECT * FROM users WHERE username = %s",
            (username,)
        )

        if cursor.fetchone():
            return render_template(
                "register.html",
                error="Username already exists!"
            )

        # Hash the password
        hashed_password = generate_password_hash(password)

        # Insert new user
        cursor.execute("""
            INSERT INTO users
            (username, password, email, phone)
            VALUES
            (%s, %s, %s, %s)
        """,
        (
            username,
            hashed_password,
            email,
            phone
        ))

        # Save changes
        db.commit()

        print("User inserted successfully!")

        flash("Registration Successful! Please login.", "success")

        return redirect(url_for("auth.admin_login"))

    except Exception as e:

        db.rollback()

        print("MYSQL ERROR:", e)

        return render_template(
            "register.html",
            error=f"Database Error: {e}"
        )


# ==========================
# Admin Login
# ==========================
@auth.route("/login", methods=["POST"])
def login():

    username = request.form["username"]
    password = request.form["password"]

    cursor.execute("""
        SELECT *
        FROM users
        WHERE username=%s
    """, (username,))

    user = cursor.fetchone()

    if not user:
        return render_template(
            "login.html",
            error="Invalid Username or Password"
        )

    stored_password = user[2]

    if not check_password_hash(stored_password, password):
        return render_template(
            "login.html",
            error="Invalid Username or Password"
        )

    return redirect(url_for("admin.welcome"))

# ==========================
# Change Password
# ==========================
@auth.route("/change_password", methods=["POST"])
def change_password():

    username = request.form["username"]
    new_password = request.form["new_password"]
    confirm_password = request.form["confirm_password"]

    if new_password != confirm_password:
        return "Passwords do not match"

    hashed_password = generate_password_hash(new_password)

    cursor.execute("""
        UPDATE users
        SET password=%s
        WHERE username=%s
    """,
    (hashed_password, username))

    db.commit()

    return "Password Updated Successfully"