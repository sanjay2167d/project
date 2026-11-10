# from flask import Flask, render_template, request, redirect, url_for
# import mysql.connector

# app = Flask(__name__)
# app = Flask(__name__, static_folder="static")

# # MySQL Connection
# db = mysql.connector.connect(
#     host="localhost",
#     user="root",
#     password="mohan123",
#     database="project"
# )

# cursor = db.cursor()

# # =========================
# # HOME PAGE (LOGIN)
# # =========================
# @app.route("/")
# def home():
#     return render_template("login.html")


# # =========================
# # REGISTER PAGE
# # =========================
# @app.route("/register_page")
# def register_page():
#     return render_template("register.html")


# # =========================
# # REGISTER USER
# # =========================
# @app.route("/register", methods=["POST"])
# def register():

#     username = request.form["username"]
#     password = request.form["password"]
#     email = request.form["email"]
#     phone = request.form["phone"]

#     # Check if username already exists
#     cursor.execute(
#         "SELECT * FROM users WHERE username=%s",
#         (username,)
#     )

#     user = cursor.fetchone()

#     if user:
#         return "Username already exists"

#     # Insert user
#     cursor.execute(
#         """
#         INSERT INTO users(username,password,email,phone)
#         VALUES(%s,%s,%s,%s)
#         """,
#         (username, password, email, phone)
#     )

#     db.commit()

#     # Go back to login page
#     return redirect(url_for("home"))


# # =========================
# # LOGIN
# # =========================
# @app.route("/login", methods=["POST"])
# def login():

#     username = request.form["username"]
#     password = request.form["password"]
#     role_id = request.form["role_id"]

#     # Check if registered
#     cursor.execute(
#         "SELECT * FROM users WHERE username=%s",
#         (username,)
#     )

#     user = cursor.fetchone()

#     if not user:
#         return "User not registered. Please register first."

#     # Check username and password
#     cursor.execute(
#         """
#         SELECT * FROM users
#         WHERE username=%s
#         AND password=%s
#         """,
#         (username, password)
#     )

#     user = cursor.fetchone()

#     if not user:
#         return "Invalid Username or Password"

#     # Check Role ID assigned
#     cursor.execute(
#         "SELECT role_id FROM users WHERE username=%s",
#         (username,)
#     )

#     role = cursor.fetchone()

#     if role[0] is None:
#         return "No Role ID assigned. Contact Admin."

#     # Verify Role ID
#     cursor.execute(
#         """
#         SELECT * FROM users
#         WHERE username=%s
#         AND password=%s
#         AND role_id=%s
#         """,
#         (username, password, role_id)
#     )

#     user = cursor.fetchone()

#     if not user:
#         return "Invalid Role ID"

#     return "Login Successful"


# # =========================
# # CHANGE PASSWORD
# # =========================
# @app.route("/change_password", methods=["POST"])
# def change_password():

#     username = request.form["username"]
#     new_password = request.form["new_password"]
#     confirm_password = request.form["confirm_password"]

#     if new_password != confirm_password:
#         return "Passwords do not match"

#     cursor.execute(
#         "SELECT * FROM users WHERE username=%s",
#         (username,)
#     )

#     user = cursor.fetchone()

#     if not user:
#         return "User not found"

#     cursor.execute(
#         """
#         UPDATE users
#         SET password=%s
#         WHERE username=%s
#         """,
#         (new_password, username)
#     )

#     db.commit()

#     return "Password Updated Successfully"


# # =========================
# # RUN APP
# # =========================
# if __name__ == "__main__":
#     app.run(debug=True)


from flask import Flask

from routes.auth import auth
from routes.admin import admin

app = Flask(__name__, static_folder="static")





# Required for flash messages
app.secret_key = "aura_solutions_secret_key"

# Register Blueprints
app.register_blueprint(auth)
app.register_blueprint(admin)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)