from flask import Flask, render_template, redirect, url_for, request, flash,session
import pymysql.cursors
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta

# Initialize the Flask app
app = Flask(__name__)

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


def insert_student(student_id, password, email, otp, otp_expires_at):
    """
    Inserts the student data into the `student_login` table.
    """
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            # Insert student login data
            insert_query = """
            INSERT INTO student_login (student_id, password, confirm_password, email, otp, otp_expires_at)
            VALUES (%s, %s, %s, %s, %s, %s)
            """
            cursor.execute(insert_query, (student_id, password, password, email, otp, otp_expires_at))
            connection.commit()
            print("Student data inserted successfully!")
    finally:
        connection.close()


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Get data from the form
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        # Basic validation
        if not name or not email or not password or not confirm_password:
            return "All fields are required", 400

        if password != confirm_password:
            return "Passwords do not match", 400

        # Simulating student_id as 1 (In real-world apps, you may want this to be auto-incremented in DB)
        student_id = 1
        otp = "123456"  # Example OTP. You should generate a dynamic OTP.
        otp_expires_at = (datetime.utcnow() + timedelta(minutes=10)).strftime('%Y-%m-%d %H:%M:%S')

        # Insert student data into the database
        insert_student(student_id, password, email, otp, otp_expires_at)

        # Redirect to the homepage after registration
        return redirect(url_for('index'))  # Redirect to the home page (or any other page after successful registration)

    return render_template('register.html')


@app.route('/')
def index():
    """
    Home page route. You can show a success message or other content.
    """
    return render_template('login.html')





# Route to display all tasks
# @app.route('/tasks')
# def task_list():
#     connection = get_db_connection()
#     try:
#         with connection.cursor() as cursor:
#             # Fetch all tasks
#             query = "SELECT * FROM tasks ORDER BY opened_at DESC"
#             cursor.execute(query)
#             tasks = cursor.fetchall()
#     finally:
#         connection.close()

#     # Render task list with tasks from the database
#     return render_template('task_list.html', tasks=tasks)





##############################################################################
# Unnecessary routes (these can be replaced with actual content later)
@app.route('/project', endpoint='project')
def placement_records():
    
    return render_template('placement_record2.html')
@app.route('/task_list')
def task_list():
    # Fetch company data along with job roles
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            # Fetch companies and their associated job roles from the company table
            query = """
            SELECT c.comp_id, c.comp_name, c.contact_no, c.linkedin_id, c.comp_email, c.created_at, c.job_role
            FROM company c
            ORDER BY c.created_at DESC
            """
            cursor.execute(query)
            companies = cursor.fetchall()

            # Debug: Print the fetched data
            print("Fetched Companies with Job Roles:", companies)

    except Exception as e:
        print(f"Error: {e}")
        flash('Error fetching task list. Please try again.', 'error')
        companies = []

    finally:
        connection.close()

    return render_template('placementinfo2.html', companies=companies)
@app.route('/settings', methods=['GET', 'POST'])
def settings():
    user_id = 1  # Replace with the actual user ID from session or authentication
    connection = get_db_connection()
    cursor = connection.cursor()

    # Fetch current user data from the database
    cursor.execute("SELECT * FROM student WHERE stud_id = %s", (user_id,))
    user = cursor.fetchone()

    if request.method == 'POST':
        stud_name = request.form['stud_name']
        cgpa = request.form['cgpa']
        contact_no = request.form['contact_no']
        course_id = request.form['course_id']
        github_id = request.form['github_id']
        linkedin_id = request.form['linkedin_id']
        portfolio_web = request.form['portfolio_web']
        skillset = request.form['skillset']
        gmail_id = request.form['gmail_id']
        alternate_email = request.form['alternate_email']

        # Update the editable fields
        cursor.execute("""
            UPDATE student
            SET stud_name = %s, cgpa = %s, contact_no = %s, course_id = %s,
                github_id = %s, linkedin_id = %s, portfolio_web = %s, skillset = %s,
                gmail_id = %s, alternate_email = %s, updated_at = NOW()
            WHERE stud_id = %s
        """, (stud_name, cgpa, contact_no, course_id, github_id, linkedin_id, 
              portfolio_web, skillset, gmail_id, alternate_email, user_id))

        connection.commit()

        return redirect(url_for('settings'))

    connection.close()  # Close the connection after the operation

    return render_template('settings.html', user=user)
@app.route('/apply', methods=['GET', 'POST'])
def apply():
    # Handling form submission (POST request)
    if request.method == 'POST':
        # Get the form data
        name = request.form['name']
        email = request.form['email']
        alt_email = request.form.get('alt_email')  # Optional field
        linkedin_url = request.form.get('linkedin_url')
        github_url = request.form.get('github_url')

        # # Handle the file upload (resume)
        # resume = request.files['resume']
        # if resume:
        #     filename = os.path.join(app.config['UPLOAD_FOLDER'], resume.filename)
        #     resume.save(filename)
        
        # Application logic here (e.g., save to database)
        # For now, just flash a success message and render the success page
        flash(f"Successfully applied for {request.args.get('job_role')} at company {request.args.get('company_id')}.", 'success')

        return render_template('apply_position.html', applied=True)

    # If GET request, render the application form
    company_id = request.args.get('company_id')
    job_role = request.args.get('job_role')
    
    return render_template('apply_position.html', company_id=company_id, job_role=job_role)
@app.route('/submit_interview', methods=['GET', 'POST'])
def submit_interview():
    if request.method == 'POST':
        stud_name = request.form['stud_name']
        comp_name = request.form['comp_name']
        exp_text = request.form['exp_text']

        # Insert into the experience table
        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                insert_query = """
                INSERT INTO experience (stud_name, comp_name, exp_text)
                VALUES (%s, %s, %s)
                """
                cursor.execute(insert_query, (stud_name, comp_name, exp_text))
                connection.commit()
                
                # Flash success message
                flash('Interview Experience submitted successfully!', 'success')

        except Exception as e:
            print(f"Error: {e}")
            flash('There was an error submitting your experience. Please try again.', 'error')
        finally:
            connection.close()

        return redirect(url_for('submit_interview'))

    return render_template('submit_interview.html') # Temporary placeholder, replace with actual page later

@app.route('/performance_report')
def performance_report():
    return render_template('login.html')  # Temporary placeholder, replace with actual page later
@app.route('/interview_experiences')
def interview_experiences():
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            query = "SELECT stud_name, comp_name, exp_text FROM experience"
            cursor.execute(query)
            experiences = cursor.fetchall()
        return render_template('interview_experiences.html', experiences=experiences)
    finally:
        connection.close()
@app.route('/view_interviews', methods=['GET'])
def view_interviews():
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            # Fetch all interview experiences from the database
            cursor.execute("SELECT * FROM experience")
            experiences = cursor.fetchall()

        return render_template('view_interview.html', experiences=experiences)

    except Exception as e:
        print(f"Error: {e}")
        flash('Error fetching interview experiences. Please try again.', 'error')
        return redirect(url_for('submit_interview'))
    
    finally:
        connection.close()





# Flask config for MySQL connection using environment variables
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                # Query to verify user credentials
                query = "SELECT * FROM student_login WHERE email = %s AND password = %s"
                cursor.execute(query, (email, password))
                user = cursor.fetchone()

                if user:
                    # Store the email in the session
                    session['email'] = email
                    return redirect(url_for('dashboard'))
                else:
                    flash('Invalid email or password')
        finally:
            connection.close()
    
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    email = session.get('email')  # Get email from the session
    if not email:
        flash('You must be logged in to view the dashboard.')
        return redirect(url_for('login'))

    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            # Query to get the user details
            query = "SELECT * FROM student_login WHERE email = %s"
            cursor.execute(query, (email,))
            user = cursor.fetchone()
            if user:
                return render_template('dashboard.html', user=user)
            else:
                return "User not found", 404
    finally:
        connection.close()
@app.route('/logout')
def logout():
    session.pop('email', None)
    return redirect(url_for('login'))
    
if __name__ == '__main__':
    app.run(debug=True)
