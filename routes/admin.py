from flask import Blueprint, render_template, request, redirect, url_for, flash
import mysql.connector

admin = Blueprint("admin", __name__)

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="mohan123",
    database="project"
)

cursor = db.cursor()

# ==========================
# HOME PAGE
# ==========================

@admin.route("/welcome")
def welcome():
    return render_template("welcome.html")


# ==========================
# ADD USER PAGE
# ==========================

@admin.route("/add-user")
def add_user():
    return render_template("manage.html")


# ==========================
# ATTENDANCE PAGE
# ==========================

@admin.route("/attendance")
def attendance():

    cursor.execute("""
        SELECT id, first_name, last_name
        FROM employees
        WHERE is_delete = 0
    """)

    employees = cursor.fetchall()

    return render_template(
        "attendance.html",
        employees=employees
    )


# ==========================
# EMPLOYEE LIST PAGE
# ==========================

@admin.route("/employee-list")
def employee_list():

    cursor.execute("""
        SELECT *
        FROM employees
        WHERE is_delete = 0
    """)

    employees = cursor.fetchall()

    return render_template(
        "employee_list.html",
        employees=employees
    )


# ==========================
# DASHBOARD PAGE
# ==========================

@admin.route("/dashboard")
def dashboard():

    # =====================================
    # TOTAL EMPLOYEES
    # =====================================

    cursor.execute("""
        SELECT COUNT(*)
        FROM employees
        WHERE is_delete=0
    """)

    total_employees = cursor.fetchone()[0]


    # =====================================
    # PRESENT TODAY
    # =====================================

    cursor.execute("""
        SELECT COUNT(*)
        FROM attendances
        WHERE attendance_date = CURDATE()
        AND status='Present'
    """)

    present_today = cursor.fetchone()[0]


    # =====================================
    # ABSENT TODAY
    # =====================================

    cursor.execute("""
        SELECT COUNT(*)
        FROM attendances
        WHERE attendance_date = CURDATE()
        AND status='Absent'
    """)

    absent_today = cursor.fetchone()[0]


    # =====================================
    # PENDING LEAVES
    # =====================================

    cursor.execute("""
        SELECT COUNT(*)
        FROM leaves
        WHERE status='Pending'
    """)

    pending_leave = cursor.fetchone()[0]


    # =====================================
    # TOTAL DEPARTMENTS
    # =====================================

    cursor.execute("""
        SELECT COUNT(DISTINCT department)
        FROM employees
        WHERE is_delete=0
    """)

    departments = cursor.fetchone()[0]


    # =====================================
    # RECENT EMPLOYEES
    # =====================================

    cursor.execute("""
        SELECT
            id,
            first_name,
            last_name,
            department,
            designation,
            status
        FROM employees
        WHERE is_delete=0
        ORDER BY id DESC
        LIMIT 5
    """)

    recent_employees = cursor.fetchall()


    # =====================================
    # RECENT LEAVE REQUESTS
    # =====================================

    cursor.execute("""
        SELECT

        employees.first_name,

        employees.last_name,

        leaves.leave_type,

        leaves.status

        FROM leaves

        JOIN employees

        ON employees.id=leaves.employee_id

        ORDER BY leave_id DESC

        LIMIT 5

    """)

    recent_leaves = cursor.fetchall()


    return render_template(

        "dashboard.html",

        total_employees=total_employees,

        present_today=present_today,

        absent_today=absent_today,

        pending_leave=pending_leave,

        departments=departments,

        recent_employees=recent_employees,

        recent_leaves=recent_leaves

    )

# ==========================
# SAVE EMPLOYEE
# ==========================

@admin.route("/save-employee", methods=["POST"])
def save_employee():

    first_name = request.form["firstname"]
    last_name = request.form["lastname"]
    age = request.form["age"]
    gender = request.form["gender"]
    dob = request.form["dob"]
    phone = request.form["phone"]
    email = request.form["email"]
    address = request.form["address"]
    department = request.form["department"]
    designation = request.form["designation"]
    joining_date = request.form["joining_date"]
    salary = request.form["salary"]
    status = request.form["status"]
    role_id = request.form["role_id"]

    cursor.execute("""
        INSERT INTO employees
        (
            first_name,
            last_name,
            age,
            gender,
            dob,
            phone,
            email,
            address,
            department,
            designation,
            joining_date,
            salary,
            status,
            role_id
        )
        VALUES
        (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """,
    (
        first_name,
        last_name,
        age,
        gender,
        dob,
        phone,
        email,
        address,
        department,
        designation,
        joining_date,
        salary,
        status,
        role_id
    ))

    db.commit()

    flash("Employee Details Saved Successfully!")

    return redirect(url_for("admin.add_user"))





# ==========================
# SAVE ATTENDANCE
# ==========================

@admin.route("/save-attendance", methods=["POST"])
def save_attendance():

    employee_id = request.form["employee_id"]
    attendance_date = request.form["attendance_date"]
    check_in = request.form["check_in"]
    check_out = request.form["check_out"]
    status = request.form["status"]

    cursor.execute("""
        INSERT INTO attendances
        (
            employee_id,
            attendance_date,
            check_in,
            check_out,
            status
        )
        VALUES
        (%s,%s,%s,%s,%s)
    """,
    (
        employee_id,
        attendance_date,
        check_in,
        check_out,
        status
    ))

    db.commit()

    flash("Attendance Saved Successfully!")

    return redirect(url_for("admin.attendance"))


# ==========================
# LEAVE MANAGEMENT PAGE
# ==========================

@admin.route("/leave-manage")
def leave_manage():

    cursor.execute("""
        SELECT id, first_name, last_name
        FROM employees
        WHERE is_delete = 0
    """)

    employees = cursor.fetchall()

    return render_template(
        "leave_manage.html",
        employees=employees
    )


# ==========================
# SAVE LEAVE
# ==========================

@admin.route("/save-leave", methods=["POST"])
def save_leave():

    employee_id = request.form["employee_id"]
    leave_type = request.form["leave_type"]
    from_date = request.form["from_date"]
    to_date = request.form["to_date"]
    reason = request.form["reason"]

    cursor.execute("""
        INSERT INTO leaves
(
employee_id,
leave_type,
from_date,
to_date,
reason,
status
)
        VALUES
        (%s,%s,%s,%s,%s,%s)
    """,
    (
employee_id,
leave_type,
from_date,
to_date,
reason,
"Pending"
))

    db.commit()

    flash("Leave Request Submitted Successfully!")

    return redirect(url_for("admin.leave_manage"))


# ==========================
# EDIT EMPLOYEE PAGE
# ==========================

@admin.route("/edit-employee/<int:id>")
def edit_employee(id):

    cursor.execute("""
        SELECT *
        FROM employees
        WHERE id = %s
    """, (id,))

    employee = cursor.fetchone()

    return render_template(
        "edit_employee.html",
        employee=employee
    )
# ==========================
# DELETE EMPLOYEE
# ==========================
# ==========================
# DELETE EMPLOYEE
# ==========================

@admin.route("/delete-employee/<int:id>")
def delete_employee(id):

    cursor.execute("""
        UPDATE employees
        SET is_delete = 1
        WHERE id = %s
    """, (id,))

    db.commit()

    flash("Employee Deleted Successfully!")

    return redirect(url_for("admin.employee_list"))


# ==========================
# UPDATE EMPLOYEE
# ==========================

@admin.route("/update-employee", methods=["POST"])
def update_employee():

    employee_id = request.form["id"]

    first_name = request.form["firstname"]
    last_name = request.form["lastname"]
    age = request.form["age"]
    gender = request.form["gender"]
    dob = request.form["dob"]
    phone = request.form["phone"]
    email = request.form["email"]
    address = request.form["address"]
    department = request.form["department"]
    designation = request.form["designation"]
    joining_date = request.form["joining_date"]
    salary = request.form["salary"]
    status = request.form["status"]
    role_id = request.form["role_id"]

    cursor.execute("""
        UPDATE employees
        SET
            first_name=%s,
            last_name=%s,
            age=%s,
            gender=%s,
            dob=%s,
            phone=%s,
            email=%s,
            address=%s,
            department=%s,
            designation=%s,
            joining_date=%s,
            salary=%s,
            status=%s,
            role_id=%s
        WHERE id=%s
    """,
    (
        first_name,
        last_name,
        age,
        gender,
        dob,
        phone,
        email,
        address,
        department,
        designation,
        joining_date,
        salary,
        status,
        role_id,
        employee_id
    ))

    db.commit()

    flash("Employee Updated Successfully!")

    return redirect(url_for("admin.employee_list"))


    # ==========================
# LEAVE REQUESTS PAGE
# ==========================

@admin.route("/leave-requests")
def leave_requests():

    cursor.execute("""
    SELECT
        employees.first_name,
        employees.last_name,
        leaves.leave_type,
        leaves.from_date,
        leaves.to_date,
        leaves.status
    FROM leaves
    JOIN employees
        ON employees.id = leaves.employee_id
    WHERE leaves.is_delete = 0
    ORDER BY leaves.leave_id DESC
""")

    requests = cursor.fetchall()

    return render_template(
        "leave_requests.html",
        requests=requests
    )