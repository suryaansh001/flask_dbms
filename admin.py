from flask import Flask, render_template, request, redirect, url_for, flash, session
from datetime import datetime, timezone, timedelta

import mysql.connector
from flask import Flask, render_template, redirect, url_for, request, flash,session
import pymysql.cursors
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta
import smtplib
from flask import request, render_template
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)
#app.secret_key = 'your_secret_key'  # Use a strong secret key in production



# Load environment variables from the .env file
load_dotenv()

# Flask config for MySQL connection using environment variables
app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST')
app.config['MYSQL_PORT'] = int(os.getenv('MYSQL_PORT'))
app.config['MYSQL_USER'] = os.getenv('MYSQL_USER')
app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD')
app.config['MYSQL_DB'] = os.getenv('MYSQL_DB')

app.secret_key = os.getenv('SECRET_KEY', 'your_secret_key')  # Use a secure key for session management

def get_db_connection():
    """
    Establishes and returns a connection to the MySQL database using PyMySQL.
    """
    connection = pymysql.connect(
        host=app.config['MYSQL_HOST'],
        user=app.config['MYSQL_USER'],
        password=app.config['MYSQL_PASSWORD'],
        database=app.config['MYSQL_DB'],
        port=app.config['MYSQL_PORT'],
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )
    return connection
@app.route('/')
def home():
    return redirect(url_for('admin_login'))
@app.route('/register_admin', methods=['GET', 'POST'])
def register_admin():
    if request.method == 'POST':
        admin_id = request.form['admin_id']
        email = request.form['email']
        password = request.form['password']
        
        # Connect to the database
        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:  # Use the cursor within the context
                # Insert the new admin into the admin_login table
                cursor.execute("""
                    INSERT INTO admin_login (admin_id, password, email)
                    VALUES (%s, %s, %s)
                """, (admin_id, password, email))  # Use plain text password
                
                connection.commit()  # Commit the changes
                flash("Admin account created successfully!", "success")
                return redirect(url_for('admin_login'))  # Redirect to login page after successful registration
        except Exception as e:
            flash(f"Error: {e}", "danger")
        finally:
            connection.close()  # Close the connection only after all operations are complete

    return render_template('register_admin.html')



   
# Admin login route
import pymysql.cursors

# @app.route('/admin_login', methods=['GET', 'POST'])
# def admin_login():
#     if request.method == 'POST':
#         admin_id = request.form['username']
#         password = request.form['password']
        
#         # Connect to the database
#         connection = get_db_connection()
#         try:
#             # Use DictCursor to return results as dictionaries
#             with connection.cursor(pymysql.cursors.DictCursor) as cursor:
#                 # Fetch the admin by admin_id
#                 cursor.execute("SELECT * FROM admin_login WHERE admin_id = %s", (admin_id,))
#                 admin = cursor.fetchone()

#                 # Check if the admin exists and the password matches
#                 if admin and admin['password'] == password:  
#                     session['admin_id'] = admin['admin_id']
#                     session['username'] = admin['email']  # Assuming you want to store the email in session
#                     flash("Login Successful!", "success")
#                     return redirect(url_for('admin_dashboard'))
#                 else:
#                     flash("Invalid admin ID or password.", "danger")
#         except Exception as e:
#             flash(f"Error: {e}", "danger")
#         finally:
#             connection.close()  # Always close the connection after the operation

#     return render_template('admin_login.html')

@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        admin_id = request.form['username']
        password = request.form['password']
        
        # Connect to the database
        connection = get_db_connection()
        try:
            with connection.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute("SELECT * FROM admin_login WHERE admin_id = %s", (admin_id,))
                admin = cursor.fetchone()

                if admin and admin['password'] == password:
                    session['admin_id'] = admin['admin_id']
                    session['username'] = admin['email']
                    flash("Login Successful!", "success")
                    return redirect(url_for('admin_dashboard'))
                else:
                    flash("Invalid admin ID or password.", "danger")
        except Exception as e:
            flash(f"Error: {e}", "danger")
        finally:
            connection.close()

    return render_template('admin_login.html')

from flask import flash, redirect, url_for


@app.route('/add_company', methods=['GET', 'POST'])
def add_company():
    if request.method == 'POST':
        # Get form data
        comp_id = request.form['comp_id']
        comp_name = request.form['comp_name']
        contact_no = request.form['contact_no']
        email = request.form['email']
        linkedin = request.form['linkedin']
        job_role = request.form['job_role']
        description = request.form['description']
        salary = request.form['salary']
        location = request.form['location']

        # Connect to the database
        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                # Insert company data into the database
                cursor.execute("""
                    INSERT INTO company (comp_id, comp_name, contact_no, comp_email, linkedin_id, job_role, description, salary, location)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (comp_id, comp_name, contact_no, email, linkedin, job_role, description, salary, location))

                connection.commit()
                flash("Company added successfully!", "success")
                return redirect(url_for('company_list'))  # Redirect to the company list page (or any page you want)
        
        except Exception as e:
            flash(f"Error: {e}", "danger")  # Flash error if something goes wrong
        
        finally:
            connection.close()

    return render_template('add_company.html')
@app.route('/company_list')
def company_list():
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT c.comp_id, c.comp_name, c.contact_no, c.comp_email, c.linkedin_id, c.created_at, c.job_role
                FROM company c
            """)
            companies = cursor.fetchall()
            
            # Ensure each company has 'job_roles' key (if a role exists)
            for company in companies:
                company['job_roles'] = [company['job_role']] if company['job_role'] else []

    finally:
        connection.close()

    return render_template('company_list.html', companies=companies)
# Route to manage students
@app.route('/manage_students')
def manage_students():
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT s.stud_id, s.stud_name, s.cgpa, s.portfolio_web, s.github_id, s.skillset,
                       s.contact_no, s.linkedin_id, s.gmail_id, s.course_id, s.created_at, s.updated_at, s.email
                FROM student s
            """)
            students = cursor.fetchall()
    finally:
        connection.close()

    return render_template('manageStudent.html', students=students)



# Route to edit a student
@app.route('/edit_student/<int:student_id>', methods=['GET', 'POST'])
def edit_student(student_id):
    connection = get_db_connection()
    student = None

    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT s.stud_id, s.stud_name, s.cgpa, s.portfolio_web, s.github_id, s.skillset,
                       s.contact_no, s.linkedin_id, s.gmail_id, s.course_id, s.created_at, s.updated_at, s.email
                FROM student s WHERE s.stud_id = %s
            """, (student_id,))
            student = cursor.fetchone()

        if request.method == 'POST':
            # Get form data
            stud_name = request.form['stud_name']
            cgpa = request.form['cgpa']
            portfolio_web = request.form['portfolio_web']
            github_id = request.form['github_id']
            skillset = request.form['skillset']
            contact_no = request.form['contact_no']
            linkedin_id = request.form['linkedin_id']
            gmail_id = request.form['gmail_id']
            course_id = request.form['course_id']
            email = request.form['email']

            with connection.cursor() as cursor:
                cursor.execute("""
                    UPDATE student SET stud_name = %s, cgpa = %s, portfolio_web = %s, github_id = %s,
                    skillset = %s, contact_no = %s, linkedin_id = %s, gmail_id = %s, course_id = %s, email = %s
                    WHERE stud_id = %s
                """, (stud_name, cgpa, portfolio_web, github_id, skillset, contact_no, linkedin_id, gmail_id, course_id, email, student_id))
                connection.commit()
            
            return redirect(url_for('manage_students'))

    finally:
        connection.close()

    return render_template('editStudent.html', student=student)

# Route to remove a student
@app.route('/remove_student', methods=['GET'])
def remove_student(student_id):
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM student WHERE stud_id = %s", (student_id,))
            connection.commit()
    finally:
        connection.close()

    return redirect(url_for('manage_students'))







@app.route('/admin_dashboard')
def admin_dashboard():
    if 'admin_id' not in session:
        return redirect(url_for('admin_login'))

    return render_template('admin_dashboard.html')
#declare routes for add student add student
import random
@app.route('/add_student', methods=['GET', 'POST'])


# @app.route('/add_student', methods=['GET', 'POST'])
# def sendemail():
#     if request.method == 'POST':
#         # Retrieve user details from the form or request
#         name = request.form.get('name')
#         email = request.form.get('email')
#         password = request.form.get('password')
#         roll_number = request.form.get('roll_number')

#         try:
#             # Set up the SMTP server
#             server = smtplib.SMTP('smtp.gmail.com', 587)
#             server.ehlo()
#             server.starttls()
#             server.login("2y6d1@example.com", "your_email_password")  # Replace with actual email and password

#             # Create the email content
#             subject = "Registration Confirmation"
#             body = f"""
#             As per your request, you have been registered. Following are your credentials:

#             Name: {name}
#             Email: {email}
#             Password: {password}
#             Roll Number: {roll_number}
#             """

#             # Create the email message
#             msg = MIMEMultipart()
#             msg['From'] = "2y6d1@example.com"
#             msg['To'] = email
#             msg['Subject'] = subject

#             # Attach the body with the msg instance
#             msg.attach(MIMEText(body, 'plain'))

#             # Send the email
#             server.sendmail(msg['From'], msg['To'], msg.as_string())
#             server.close()

#             return "Email sent successfully!"

#         except Exception as e:
#             return f"Failed to send email: {str(e)}"

#     return render_template('add_student.html')  # Or whichever template you're using

        
# def add_student():
#     if request.method == 'POST':
#         # Get form data
#         student_id = request.form['stud_id']
#         name = request.form['stud_name']
#         email = request.form['email']
#         password = f"{student_id}{random.randint(1000, 9999)}"  # Generate a random password
        
#         # Connect to the database
#         connection = get_db_connection()
#         try:
#             with connection.cursor() as cursor:
#                 # Insert student data into the database
#                 cursor.execute("""
#                     INSERT INTO student_login (student_id, name, email,password)
#                     VALUES (%s, %s, %s, %s, %s, %s)
#                 """, (stud_id, name,password,email,password))
#                 connection.commit()
#                 # Display passsword to the user
#                 flash(f"Student added successfully! Password: {password}", "success")
#                 flash("Student added successfully!", "success")
#                 return redirect(url_for('manage_students'))
#         except Exception as e:
#             flash(f"Error: {e}", "danger")
#         finally:
#             connection.close()

#     return render_template('add_student.html')
@app.route('/add_student', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        # Get form data
        student_id = request.form['stud_id']
        name = request.form['stud_name']
        email = request.form['email']
        otp = "123456"  # Example OTP. You should generate a dynamic OTP.
        otp_expires_at = (datetime.utcnow() + timedelta(minutes=10)).strftime('%Y-%m-%d %H:%M:%S')
        
        # Generate a random password using student ID + random number
        password = f"{student_id}{random.randint(1000, 9999)}"

        # Connect to the database
        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                # Insert student data into the database
                cursor.execute("""
                    INSERT INTO student_login (student_id, name, email, password, otp, otp_expires_at)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (student_id, name, email, password, otp, otp_expires_at))
                connection.commit()
                cursor.execute(""" 
                INSERT INTO student (stud_id, stud_name, email)
                VALUES (%s, %s, %s)
                """), (student_id, name, email)
                connoection.commit()

                # Send email with credentials
                #send_email(name, email, password, student_id)

                # Notify the user about the success
                flash(f"Student added successfully! Password: {password}", "success")
                return redirect(url_for('add_student'))  # Redirect to the same page after successful registration
        except Exception as e:
            flash(f"Error: {e}", "danger")
        finally:
            connection.close()

    return render_template('add_student.html')  # Render form template


def send_email(name, email, password, student_id):
    try:
        # Set up the SMTP server
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.login("2y6d1@example.com", "your_email_password")  # Replace with actual email and password

        # Create the email content
        subject = "Registration Confirmation"
        body = f"""
        As per your request, you have been registered. Following are your credentials:

        Name: {name}
        Email: {email}
        Password: {password}
        Roll Number: {student_id}
        """

        # Create the email message
        msg = MIMEMultipart()
        msg['From'] = "2y6d1@example.com"
        msg['To'] = email
        msg['Subject'] = subject

        # Attach the body with the msg instance
        msg.attach(MIMEText(body, 'plain'))

        # Send the email
        server.sendmail(msg['From'], msg['To'], msg.as_string())
        server.close()

        print(f"Email sent to {email} with credentials.")
    except Exception as e:
        print(f"Failed to send email: {str(e)}")

#route for logout 
@app.route('/logout')
def logout():
    session.pop('admin_id', None)
    session.pop('username', None)
    flash("You have been logged out.", "info")
    return redirect(url_for('admin_login')) 

if __name__ == '__main__':
     app.run(host='0.0.0.0', port=8000) 