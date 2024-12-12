from flask import Flask, render_template, request, redirect, url_for, flash, session
from datetime import datetime, timedelta
import pymysql.cursors
from dotenv import load_dotenv
import os
import logging

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

# Configure logging
logging.basicConfig(level=logging.DEBUG)

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

@app.route('/register_company', methods=['GET', 'POST'])
def register_company():
    if request.method == 'POST':
        company_id = int(request.form['company_id'])
        company_name = request.form['company_name']
        email = request.form['email']
        password = request.form['password']  # Plain text password

        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                # Insert into company_login table
                cursor.execute("""
                    INSERT INTO company_login (company_id, password, email, company_name)
                    VALUES (%s, %s, %s, %s)
                """, (company_id, password, email, company_name))
                
                # Insert into company table
                cursor.execute("""
                    INSERT INTO company (comp_id, comp_name, comp_email)
                    VALUES (%s, %s, %s)
                """, (company_id, company_name, email))
                
                connection.commit()
                flash("Company account created successfully!", "success")
                return redirect(url_for('company_login'))
        except Exception as e:
            flash(f"Error: {e}", "danger")
        finally:
            connection.close()

    return render_template('register_company.html')

@app.route('/company_login', methods=['GET', 'POST'])
def company_login():
    if request.method == 'POST':
        company_id = int(request.form['company_id'])
        password = request.form['password']

        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM company_login WHERE company_id = %s", (company_id,))
                company = cursor.fetchone()

                if company and company['password'] == password:
                    session['company_id'] = company['company_id']
                    session['company_name'] = company['company_name']
                    flash("Login Successful!", "success")
                    return redirect(url_for('submit_job'))
                else:
                    flash("Invalid Company ID or password.", "danger")
        except Exception as e:
            flash(f"Error: {e}", "danger")
        finally:
            connection.close()

    return render_template('company_login.html')

@app.route('/company_logout')
def company_logout():
    session.pop('company_id', None)
    session.pop('company_name', None)
    flash("You have been logged out.", "info")
    return redirect(url_for('company_login'))

@app.route('/')
def home():
    return render_template('company_login.html')
@app.route('/submit_job', methods=['GET', 'POST'])
def submit_job():
    if 'company_id' not in session:
        flash('Please login first', 'danger')
        return redirect(url_for('company_login'))

    if request.method == 'POST':
        # Extract form data
        title = request.form['title']
        description = request.form['description']
        requirements = request.form['requirements']
        salary = request.form['salary']
        location = request.form['location']
        end_date = request.form['end_date']
        company_id = session['company_id']

        # Basic validation
        if not all([title, description]):
            flash('Title and description are required', 'danger')
            return render_template('submit_job.html')

        # Validate end_date
        try:
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
            if end_date < datetime.now().date():
                flash('End date cannot be in the past', 'danger')
                return render_template('submit_job.html')
        except ValueError:
            flash('Invalid date format. Please use YYYY-MM-DD', 'danger')
            return render_template('submit_job.html')

        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                insert_query = """
                INSERT INTO job_posting (
                    company_id, title, description, requirements, 
                    salary, location, end_date, status
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, 'pending')
                """
                cursor.execute(insert_query, (
                    company_id, title, description, requirements,
                    salary, location, end_date
                ))
                connection.commit()
                flash('Job posting submitted successfully!', 'success')
                return redirect(url_for('submit_job'))

        except Exception as e:
            connection.rollback()
            flash(f'Error submitting job posting: {str(e)}', 'danger')
            return render_template('submit_job.html')
        finally:
            connection.close()

    return render_template('submit_job.html')
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)