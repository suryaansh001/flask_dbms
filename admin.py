from flask import Flask, render_template, request, redirect, url_for, flash, session
from datetime import datetime, timedelta
import pymysql.cursors
from dotenv import load_dotenv
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from functools import wraps
import random

app = Flask(__name__)

# Load environment variables from the .env file
load_dotenv()

# Flask config for MySQL connection using environment variables
app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST')
app.config['MYSQL_PORT'] = int(os.getenv('MYSQL_PORT', 3306))
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

def admin_login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin_id' not in session:
            flash("Please log in as admin to access this page.", "warning")
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def home():
    return redirect(url_for('admin_login'))

@app.route('/register_admin', methods=['GET', 'POST'])
def register_admin():
    if request.method == 'POST':
        admin_id = request.form['admin_id']
        email = request.form['email']
        password = request.form['password']

        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO admin_login (admin_id, password, email)
                    VALUES (%s, %s, %s)
                """, (admin_id, password, email))  # Store plain text password

                connection.commit()
                flash("Admin account created successfully!", "success")
                return redirect(url_for('admin_login'))
        except Exception as e:
            flash(f"Error: {e}", "danger")
        finally:
            connection.close()

    return render_template('register_admin.html')

@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        admin_id = request.form['username']
        password = request.form['password']

        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
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

@app.route('/logout')
def logout():
    session.pop('admin_id', None)
    session.pop('username', None)
    flash("You have been logged out.", "info")
    return redirect(url_for('admin_login'))

@app.route('/admin_dashboard')
@admin_login_required

def admin_dashboard():
    connection = get_db_connection()
    new_company_requests = []
    new_student_requests = []

    try:
        with connection.cursor() as cursor:
            # Query to fetch pending company requests
            cursor.execute("""
                SELECT * FROM admin_company WHERE status = 'pending'
            """)
            new_company_requests = cursor.fetchall()

            # Query to fetch pending student queries
            cursor.execute("""
                SELECT * FROM admin_students_queries WHERE status = 'pending'
            """)
            new_student_requests = cursor.fetchall()

    except Exception as e:
        flash(f"Error: {e}", "danger")
    finally:
        connection.close()

    return render_template('admin_dashboard.html', 
                           new_company_requests=new_company_requests, 
                           new_student_requests=new_student_requests)
@app.route('/add_company', methods=['GET', 'POST'])
@admin_login_required
def add_company():
    if request.method == 'POST':
        comp_id = request.form['comp_id']
        comp_name = request.form['comp_name']
        contact_no = request.form['contact_no']
        email = request.form['email']
        linkedin = request.form['linkedin']
        job_role = request.form['job_role']
        description = request.form['description']
        salary = request.form['salary']
        location = request.form['location']

        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO company (comp_id, comp_name, contact_no, comp_email, linkedin_id, job_role, description, salary, location)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (comp_id, comp_name, contact_no, email, linkedin, job_role, description, salary, location))
                connection.commit()
                flash("Company added successfully!", "success")
                return redirect(url_for('company_list'))
        except Exception as e:
            flash(f"Error: {e}", "danger")
        finally:
            connection.close()

    return render_template('add_company.html')

@app.route('/company_list')
@admin_login_required
def company_list():
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT c.comp_id, c.comp_name, c.contact_no, c.comp_email, c.linkedin_id, c.created_at, c.job_role
                FROM company c
            """)
            companies = cursor.fetchall()
            for company in companies:
                company['job_roles'] = [company['job_role']] if company['job_role'] else []
    finally:
        connection.close()

    return render_template('company_list.html', companies=companies)

@app.route('/manage_students')
@admin_login_required
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

@app.route('/edit_student/<string:student_id>', methods=['GET', 'POST'])
@admin_login_required
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

            flash("Student updated successfully!", "success")
            return redirect(url_for('manage_students'))

    except Exception as e:
        flash(f"Error: {e}", "danger")
    finally:
        connection.close()

    return render_template('editStudent.html', student=student)

@app.route('/remove_student/<string:student_id>', methods=['GET'])
@admin_login_required
def remove_student(student_id):
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM student WHERE stud_id = %s", (student_id,))
            connection.commit()
            flash("Student removed successfully!", "success")
    except Exception as e:
        flash(f"Error: {e}", "danger")
    finally:
        connection.close()

    return redirect(url_for('manage_students'))

@app.route('/add_student', methods=['GET', 'POST'])
@admin_login_required
def add_student():
    if request.method == 'POST':
        stud_id = request.form['stud_id']
        name = request.form['stud_name']
        email = request.form['email']
        otp = str(random.randint(100000, 999999))
        otp_expires_at = (datetime.utcnow() + timedelta(minutes=10)).strftime('%Y-%m-%d %H:%M:%S')
        password = f"{stud_id}{random.randint(1000, 9999)}"

        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO student_login (student_id, name, email, password, otp, otp_expires_at)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (stud_id, name, email, password, otp, otp_expires_at))
                cursor.execute("""
                    INSERT INTO student (stud_id, stud_name, email)
                    VALUES (%s, %s, %s)
                """, (stud_id, name, email))
                connection.commit()

                # Optionally, send email with credentials
                # send_email(name, email, password, stud_id)

                flash(f"Student added successfully! Password: {password}", "success")
                return redirect(url_for('manage_students'))
        except Exception as e:
            flash(f"Error: {e}", "danger")
        finally:
            connection.close()

    return render_template('add_student.html')

def send_email(name, email, password, student_id):
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.login("2y6d1@example.com", "your_email_password")  # Replace with actual credentials

        subject = "Registration Confirmation"
        body = f"""
        As per your request, you have been registered. Following are your credentials:

        Name: {name}
        Email: {email}
        Password: {password}
        Roll Number: {student_id}
        """

        msg = MIMEMultipart()
        msg['From'] = "2y6d1@example.com"
        msg['To'] = email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        server.sendmail(msg['From'], msg['To'], msg.as_string())
        server.close()

        print(f"Email sent to {email} with credentials.")
    except Exception as e:
        print(f"Failed to send email: {str(e)}")
@app.route('/pending_jobs')
@admin_login_required
def pending_jobs():
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT 
                    jp.id, 
                    jp.title, 
                    jp.description, 
                    jp.requirements, 
                    jp.salary, 
                    jp.location,
                    jp.end_date,
                    jp.date_posted,
                    c.comp_name,
                    jp.company_id
                FROM job_posting jp
                JOIN company c ON jp.company_id = c.comp_id
                WHERE jp.status = 'pending'
                ORDER BY jp.date_posted DESC
            """)
            pending_jobs = cursor.fetchall()
    except Exception as e:
        flash(f"Error fetching pending jobs: {e}", "danger")
        pending_jobs = []
    finally:
        connection.close()

    return render_template('pending_jobs.html', pending_jobs=pending_jobs)
@app.route('/approve_job/<int:job_id>', methods=['POST'])
@admin_login_required
def approve_job(job_id):
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            # Fetch job title
            cursor.execute("""
                SELECT title 
                FROM job_posting 
                WHERE id = %s
            """, (job_id,))
            job = cursor.fetchone()
            if not job:
                flash("Job posting not found.", "danger")
                return redirect(url_for('pending_jobs'))

            title = job['title']

            # Update job status
            cursor.execute("""
                UPDATE job_posting
                SET status = 'approved'
                WHERE id = %s
            """, (job_id,))
            
            # Update company status and job role
            cursor.execute("""
                UPDATE company 
                SET status = 'active', job_role = %s
                WHERE comp_id IN (
                    SELECT company_id 
                    FROM job_posting
                    WHERE id = %s
                )
            """, (title, job_id))
            
            connection.commit()
            flash("Job posting approved successfully.", "success")
            flash("Company status updated to active", "success")
            
    except Exception as e:  
        connection.rollback()
        flash(f"Error approving job posting: {e}", "danger")
    finally:
        connection.close()

    return redirect(url_for('pending_jobs'))

@app.route('/reject_job/<int:job_id>', methods=['POST'])
@admin_login_required
def reject_job(job_id):
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                UPDATE job_posting
                SET status = 'rejected'
                WHERE id = %s
            """, (job_id,))
            connection.commit()
            flash("Job posting rejected successfully.", "success")
    except Exception as e:
        flash(f"Error rejecting job posting: {e}", "danger")
    finally:
        connection.close()

    return redirect(url_for('pending_jobs'))

@app.route('/approved_jobs')
@admin_login_required
def approved_jobs():
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT jp.id, jp.title, jp.description, jp.requirements, jp.salary, jp.location,
                       c.comp_name, c.comp_email, c.linkedin_id
                FROM job_posting jp
                JOIN company c ON jp.company_id = c.comp_id
                WHERE jp.status = 'approved'
            """)
            approved_jobs = cursor.fetchall()
    finally:
        connection.close()

    return render_template('approved_jobs.html', approved_jobs=approved_jobs)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=9000)