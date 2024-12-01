from flask import Flask, render_template, request, redirect, url_for, flash, session

import mysql.connector
from flask import Flask, render_template, redirect, url_for, request, flash,session
import pymysql.cursors
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta

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

@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        admin_id = request.form['username']
        password = request.form['password']
        
        # Connect to the database
        connection = get_db_connection()
        try:
            # Use DictCursor to return results as dictionaries
            with connection.cursor(pymysql.cursors.DictCursor) as cursor:
                # Fetch the admin by admin_id
                cursor.execute("SELECT * FROM admin_login WHERE admin_id = %s", (admin_id,))
                admin = cursor.fetchone()

                # Check if the admin exists and the password matches
                if admin and admin['password'] == password:  
                    session['admin_id'] = admin['admin_id']
                    session['username'] = admin['email']  # Assuming you want to store the email in session
                    flash("Login Successful!", "success")
                    return redirect(url_for('admin_dashboard'))
                else:
                    flash("Invalid admin ID or password.", "danger")
        except Exception as e:
            flash(f"Error: {e}", "danger")
        finally:
            connection.close()  # Always close the connection after the operation

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
        
        # Connect to the database
        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                # Insert company data into the database
                cursor.execute("""
                    INSERT INTO company (comp_id, comp_name, contact_no, comp_email, linkedin_id, job_role)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (comp_id, comp_name, contact_no, email, linkedin, job_role))
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

@app.route('/admin_dashboard')
def admin_dashboard():
    if 'admin_id' not in session:
        return redirect(url_for('admin_login'))

    return render_template('admin_dashboard.html')

if __name__ == '__main__':
     app.run(host='0.0.0.0', port=8000) ?