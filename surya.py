from flask import Flask, render_template, redirect, url_for, request, flash,session
import pymysql.cursors
from dotenv import load_dotenv
from datetime import datetime
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


# def insert_student(student_id, password, email, otp, otp_expires_at):
#     """
#     Inserts the student data into the `student_login` table.
#     """
#     connection = get_db_connection()
#     try:
#         with connection.cursor() as cursor:
#             # Insert student login data
#             insert_query = """
#             INSERT INTO student_login (student_id, password, confirm_password, email, otp, otp_expires_at)
#             VALUES (%s, %s, %s, %s, %s, %s)
#             """
#             cursor.execute(insert_query, (student_id, password, password, email, otp, otp_expires_at))
#             connection.commit()
#             print("Student data inserted successfully!")
#     finally:
#         connection.close()
def insert_student(student_id, password, email, otp, otp_expires_at, name):
    """
    Inserts the student data into the `student_login` table, including the name and roll number.
    """
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            # Insert student login data along with the name and roll number (as student_id)
            insert_query = """
            INSERT INTO student_login (student_id, password, email, otp, otp_expires_at, name)
            VALUES (%s, %s, %s, %s, %s, %s)
            """
            cursor.execute(insert_query, (student_id, password, email, otp, otp_expires_at, name))
            insert_query2 = """
            INSERT INTO student (stud_id, stud_name,email)
            VALUES (%s, %s,%s)
            """
            cursor.execute(insert_query2, (student_id, name,email))
            connection.commit()
            print("Student data inserted successfully!")
    finally:
        connection.close()



@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Get data from the form
        name = request.form.get('name')
        roll_number = request.form.get('roll_number')  # Get Roll Number
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        # Basic validation
        if not name or not roll_number or not email or not password or not confirm_password:
            return "All fields are required", 400

        if password != confirm_password:
            return "Passwords do not match", 400

        # Simulate student_id as roll_number (convert it to an integer if necessary)
        student_id = roll_number  # Use roll_number as student_id
        otp = "123456"  # Example OTP. You should generate a dynamic OTP.
        otp_expires_at = (datetime.utcnow() + timedelta(minutes=10)).strftime('%Y-%m-%d %H:%M:%S')

        # Insert student data into the database
        insert_student(student_id, password, email, otp, otp_expires_at, name)

        # Redirect to the homepage after registration
        return redirect(url_for('index'))  # Redirect to the home page (or any other page after successful registration)

    return render_template('register.html')



# @app.route('/register', methods=['GET', 'POST'])
# def register():
#     if request.method == 'POST':
#         # Get data from the form
#         name = request.form['name']
#         email = request.form['email']
#         password = request.form['password']
#         confirm_password = request.form['confirm_password']

#         # Basic validation
#         if not name or not email or not password or not confirm_password:
#             return "All fields are required", 400

#         if password != confirm_password:
#             return "Passwords do not match", 400

#         # Simulating student_id as 1 (In real-world apps, you may want this to be auto-incremented in DB)
#         student_id = 1
#         otp = "123456"  # Example OTP. You should generate a dynamic OTP.
#         otp_expires_at = (datetime.utcnow() + timedelta(minutes=10)).strftime('%Y-%m-%d %H:%M:%S')

#         # Insert student data into the database
#         insert_student(student_id, password, email, otp, otp_expires_at,name)

#         # Redirect to the homepage after registration
#         return redirect(url_for('index'))  # Redirect to the home page (or any other page after successful registration)

#     return render_template('register.html')


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
# def isactive(comp_id):
#     try:
#         connection = get_db_connection()
#         with connection.cursor() as cursor:
#             query = "SELECT end_date FROM company WHERE comp_id = %s"
#             cursor.execute(query, (comp_id,))
#             end_date = cursor.fetchone()
#             if end_date>datetime.now():
#                 return True
#             else:
#                 return False
#     finally:

#             return company['is_active']




@app.route('/task_list')
def task_list():
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            # Fetch ongoing and past companies based on job_posting status and end_date
            ongoing_query = """
                SELECT c.*, jp.title AS job_role 
                FROM company c
                JOIN job_posting jp ON c.comp_id = jp.company_id
                WHERE jp.status = 'approved' AND (jp.end_date IS NULL OR jp.end_date >= NOW())
                ORDER BY c.created_at DESC
            """
            cursor.execute(ongoing_query)
            ongoing_companies = cursor.fetchall()

            past_query = """
                SELECT c.*, jp.title AS job_role 
                FROM company c
                JOIN job_posting jp ON c.comp_id = jp.company_id
                WHERE jp.status = 'approved' AND jp.end_date < NOW()
                ORDER BY c.created_at DESC
            """
            cursor.execute(past_query)
            past_companies = cursor.fetchall()

            # Update past company statuses to 'inactive'
            update_query = """
                UPDATE company 
                SET status = 'inactive'
                WHERE comp_id IN (
                    SELECT company_id 
                    FROM job_posting
                    WHERE status = 'approved' AND end_date < NOW()
                )
            """
            cursor.execute(update_query)
            connection.commit()

    except Exception as e:
        connection.rollback()
        flash(f"Error fetching task list: {e}", "danger")
        ongoing_companies, past_companies = [], []
    finally:
        connection.close()

    return render_template('placement3.html', ongoing_companies=ongoing_companies, past_companies=past_companies)

@app.route('/company_details/<int:comp_id>')
def company_details(comp_id):
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            # Fetch company details based on comp_id
            query = """
            SELECT * FROM company WHERE comp_id = %s
            """
            cursor.execute(query, (comp_id,))
            company = cursor.fetchone()
    except Exception as e:
        print(f"Error: {e}")
        flash('Error fetching company details. Please try again.', 'error')
        company = None
    finally:
        connection.close()

    return render_template('company_details.html', company=company)


@app.route('/settings', methods=['GET', 'POST'])
def settings():
    if 'stud_id' not in session:
        return redirect(url_for('login'))  # Redirect to login if the user is not authenticated

    stud_id = session['stud_id']  # Get the stud_id from the session
    email = session.get('email')  # Get email from session
    print(f"Stud ID: {stud_id}, Email: {email}")  # Debug statement to confirm session values

    connection = get_db_connection()

    try:
        with connection.cursor() as cursor:
            # Fetch the user data based on stud_id and email (from session)
            cursor.execute("SELECT * FROM student WHERE stud_id = %s", (stud_id,))
            user = cursor.fetchone()

            # Check if the user exists
            if user is None:
                flash('User not found', 'error')
                return redirect(url_for('login'))

            # Handling POST request to update user data
            if request.method == 'POST':
                # Retrieve form data, using .get() to avoid key errors if the field is missing
                stud_name = request.form.get('stud_name')
                contact_no = request.form.get('contact_no')
                
                github_id = request.form.get('github_id')
                linkedin_id = request.form.get('linkedin_id')
                portfolio_web = request.form.get('portfolio_web')
                skillset = request.form.get('skillset')

                # Build the update query dynamically based on which fields are provided
                update_query = "UPDATE student SET updated_at = NOW()"
                values = []

                
                if github_id:
                    update_query += ", github_id = %s"
                    values.append(github_id)
                if linkedin_id:
                    update_query += ", linkedin_id = %s"
                    values.append(linkedin_id)
                if portfolio_web:
                    update_query += ", portfolio_web = %s"
                    values.append(portfolio_web)
                if skillset:
                    update_query += ", skillset = %s"
                    values.append(skillset)

                # Add the student ID to the values list for the WHERE clause
                update_query += " WHERE stud_id = %s"
                values.append(stud_id)

                # Execute the query with dynamic values
                cursor.execute(update_query, tuple(values))
                flash('query GENERATEd', 'success')
                print(f"Query: {cursor.mogrify(update_query, tuple(values))}")

                # Commit the transaction
                connection.commit()

                flash('Your changes have been saved successfully!', 'success')
                return redirect(url_for('settings'))

    except Exception as e:
        flash(f"An error occurred: {str(e)}", 'error')
    finally:
        connection.close()

    # Render the settings page with the user data
    return render_template('settings2.html', user=user)
# Pass the user data to the template


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

@app.context_processor
def inject_stud_id():
    return dict(stud_id=session.get('stud_id'))



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
                    # Store the email and stud_id in the session
                    session['email'] = email
                    session['stud_id'] = user['student_id']  # Store the student ID
                    return redirect(url_for('dashboard'))
                else:
                    flash('Invalid email or password')
        finally:
            connection.close()
    
    return render_template('login.html')
# @app.route('/login', methods=['GET', 'POST'])
# def login():
    # if request.method == 'POST':
    #     email = request.form['email']
    #     password = request.form['password']
        
    #     connection = get_db_connection()
    #     try:
    #         with connection.cursor() as cursor:
    #             # Query to verify user credentials
    #             query = "SELECT * FROM student_login WHERE email = %s AND password = %s"
    #             cursor.execute(query, (email, password))
    #             user = cursor.fetchone()

    #             if user:
    #                 # Store the email and stud_id in the session
    #                 session['email'] = email
    #                 session['stud_id'] = user['student_id']  # Store the student ID
    #                 return redirect(url_for('dashboard'))
    #             else:
    #                 flash('Invalid email or password')
    #     finally:
    #         connection.close()
    
    # return render_template('login.html')


# @app.route('/dashboard')
# def dashboard():
#     email = session.get('email')  # Get email from the session
#     if not email:
#         flash('You must be logged in to view the dashboard.')
#         return redirect(url_for('login'))

#     connection = get_db_connection()
#     try:
#         with connection.cursor() as cursor:
#             # Query to get the user details
#             query = "SELECT * FROM student_login WHERE email = %s"
#             cursor.execute(query, (email,))
#             user = cursor.fetchone()
#             if user:
#                 return render_template('dashboard.html', user=user)
#             else:
#                 return "User not found", 404
#     finally:
#         connection.close()
import pymysql.cursors

@app.route('/dashboard')
def dashboard():
    email = session.get('email')  # Get email from the session
    if not email:
        flash('You must be logged in to view the dashboard.')
        return redirect(url_for('login'))

    connection = get_db_connection()  # Get database connection
    try:
        with connection.cursor() as cursor:  # Ensure result is returned as a simple tuple
            # Query to get the user details based on the email
            query = "SELECT * FROM student_login WHERE email = %s"
            cursor.execute(query, (email,))
            user = cursor.fetchone()  # Fetch user record

            if not user:
                flash("User not found.", "error")
                return redirect(url_for('login'))

            # Fetch the 5 most recent placement drives
            placement_drives_query = """
            SELECT c.comp_id, c.comp_name, c.contact_no, c.linkedin_id, c.comp_email, c.created_at, c.job_role
            FROM company c
            ORDER BY c.created_at DESC
            LIMIT 5
            """
            cursor.execute(placement_drives_query)
            placement_drives = cursor.fetchall()  # Fetch 5 most recent placement drives

            # Hardcoded sample data for placement counts in a list format (no dictionary)
            placement_counts = [
                ("Amazon", 40),
                ("Flipkart", 13),
                ("FUDR", 23),
                ("Others", 24)  # Remaining percentage
            ]

            # Prepare the data for the pie chart: a simple list
            chart_labels = [count[0] for count in placement_counts]
            chart_data = [count[1] for count in placement_counts]

            if not placement_drives:
                flash("No recent placement drives available.", "info")

            return render_template('dashboard.html', user=user, placement_drives=placement_drives, chart_labels=chart_labels, chart_data=chart_data)

    except Exception as e:
        flash(f"An error occurred: {str(e)}", "error")
        return redirect(url_for('login'))  # Optionally redirect on error
    finally:
        connection.close()  # Ensure the connection is closed
# @app.route('/dashboard')
# def dashboard():
#     email = session.get('email')  # Get email from the session
#     if not email:
#         flash('You must be logged in to view the dashboard.')
#         return redirect(url_for('login'))

#     connection = get_db_connection()  # Get database connection
#     try:
#         with connection.cursor() as cursor:  # Ensure result is returned as a simple tuple
#             # Query to get the user details based on the email
#             query = "SELECT * FROM student_login WHERE email = %s"
#             cursor.execute(query, (email,))
#             user = cursor.fetchone()  # Fetch user record

#             if not user:
#                 flash("User not found.", "error")
#                 return redirect(url_for('login'))

#             # Fetch the 5 most recent placement drives
#             placement_drives_query = """
#             SELECT c.comp_id, c.comp_name, c.contact_no, c.linkedin_id, c.comp_email, c.created_at, c.job_role
#             FROM company c
#             ORDER BY c.created_at DESC
#             LIMIT 5
#             """
#             cursor.execute(placement_drives_query)
#             placement_drives = cursor.fetchall()  # Fetch 5 most recent placement drives

#             # Hardcoded sample data for placement counts in a list format (no dictionary)
#             placement_counts = [
#                 ("Amazon", 40),
#                 ("Flipkart", 13),
#                 ("FUDR", 23),
#                 ("Others", 24)  # Remaining percentage
#             ]

#             # Prepare the data for the pie chart: a simple list
#             chart_labels = [count[0] for count in placement_counts]
#             chart_data = [count[1] for count in placement_counts]

#             if not placement_drives:
#                 flash("No recent placement drives available.", "info")

#             return render_template('dashboard.html', user=user, placement_drives=placement_drives, chart_labels=chart_labels, chart_data=chart_data)

#     except Exception as e:
#         flash(f"An error occurred: {str(e)}", "error")
#         return redirect(url_for('login'))  # Optionally redirect on error
#     finally:
#         connection.close()  # Ensure the connection is closed

@app.route('/student_query_submit', methods=['GET', 'POST'])
def query():
    stud_id = session.get('stud_id')
    if not stud_id:
        flash('Please login first', 'danger')
        return redirect(url_for('login'))

    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            # Fetch user details
            cursor.execute("SELECT * FROM student WHERE stud_id = %s", (stud_id,))
            user = cursor.fetchone()

            if request.method == 'POST':
                stud_query = request.form['stud_query']
                insert_query = """
                INSERT INTO student_queries (stud_id, query) 
                VALUES (%s, %s)
                """
                cursor.execute(insert_query, (stud_id, stud_query))
                connection.commit()
                flash('Query submitted successfully!', 'success')
                return redirect(url_for('query'))

            # Fetch previous queries
            cursor.execute("""
            SELECT query, status FROM student_queries WHERE stud_id = %s
            """, (stud_id,))
            queries = cursor.fetchall()

    except Exception as e:
        print(f"Error: {e}")
        flash('There was an error submitting your query. Please try again.', 'danger')
        queries = []
    finally:
        connection.close()

    return render_template('student_query.html', user=user, queries=queries)

@app.route('/queries')
def view_queries():
    stud_id = session.get('stud_id')
    if not stud_id:
        flash('Please login first', 'danger')
        return redirect(url_for('login'))

    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            # Fetch user details
            cursor.execute("SELECT * FROM student WHERE stud_id = %s", (stud_id,))
            user = cursor.fetchone()

            # Fetch queries and replies
            cursor.execute("""
            SELECT query, reply, status 
            FROM student_queries 
            WHERE stud_id = %s
            """, (stud_id,))
            queries = cursor.fetchall()

    except Exception as e:
        print(f"Error: {e}")
        flash('There was an error fetching your queries. Please try again.', 'danger')
        queries = []
    finally:
        connection.close()

    return render_template('view_queries.html', user=user, queries=queries)

@app.route('/logout')
def logout():
    session.pop('email', None)
    return redirect(url_for('login'))
    
if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0', port=7000)
