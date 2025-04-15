# from flask import Flask,render_template,request,redirect,session
# import mysql.connector
# import os
# app=Flask(__name__)
# app.secret_key=os.urandom(30)
# conn=mysql.connector.connect(host='localhost',user='root',password='Kok@3130',database='intellishop')
# cursor=conn.cursor()
# @app.route('/')
# def login():
#     return render_template('login.html')

# @app.route('/register')
# def register():
#     return render_template('register.html')

# @app.route('/home')
# def home():
#     if('user_id' in session):
#         return render_template('home.html')
#     else:
#         return redirect('/')

# @app.route('/login_validation',methods=['POST'])
# def login_validation():
#     email = request.form.get('email')
#     password = request.form.get('password')
#     # Input validation
#     if not email and not password:
#         return render_template('login.html', error_message="Please enter your credentials.")
#     if not email:
#         return render_template('login.html', error_message="Please enter your email.")
#     if not password:
#         return render_template('login.html', error_message="Please enter your password.")
#     # Secure database query with parameterized inputs
#     try:
#         cursor.execute("""SELECT *FROM `REGISTERED_USERS` WHERE `EMAIL` LIKE '{}' AND `PASSWORD` LIKE '{}'""".format(email,password))
#         users=cursor.fetchall()
#         if users:  # If credentials are correct
#             session['user_id'] = users[0][0]  # Store user ID in session
#             return redirect('/home')  # Redirect to home page
#         else:
#             return render_template('login.html', error_message="Invalid credentials. Please Register first.")
    
#     except Exception as e:
#         # Log the error for debugging
#         print(f"Database error: {str(e)}")
#         return render_template('login.html', error_message="Login failed. Please try again later.")
    
# @app.route('/register_validation',methods=['POST'])
# def register_validation():
#     import re
#     # Get form data
#     name = request.form.get('uname')
#     email = request.form.get('uemail')
#     password = request.form.get('upassword')
#     # Check if all fields are provided
#     if not name and not email and not password:
#         return render_template('register.html', error_message="Please enter all your credentials.")
#     if not name:
#         return render_template('register.html', error_message="Please enter your name.")
#     if not email:
#         return render_template('register.html', error_message="Please enter your email.")
    
#     elif not re.match(r"[^@]+@[^@]+\.[^@]+", email):
#         return render_template('register.html', error_message="Invalid email format.")
    
#     if not password:
#         return render_template('register.html', error_message="Please enter your password.")
    
#     # Validate name (no numeric values)
#     if name and any(char.isdigit() for char in name):
#         return render_template('register.html', error_message="Name must contain only alphabets.")
    
#     # If all validations pass, proceed with database operation
#     try:
#         cursor.execute("""INSERT INTO `REGISTERED_USERS` (`user_id`,`name`,`email`,`password`) VALUES 
#                        (NULL,%s,%s,%s)""", (name, email, password))
#         conn.commit()
#         return "User Registered Successfully."
#     except Exception as e:
#         # Handle potential database errors (like duplicate email)
#         conn.rollback()
#         return render_template('register.html', error_message="Already exist. Please change.")

# @app.route('/logout')
# def logout():
#     session.pop('user_id')
#     return redirect('/')


# if __name__=='__main__':
#     app.run(debug=True)


# ---------------------------------------------------------------------------------------------------
#                         postgresql
# ----------------------------------------------------------------------------------------------------


from flask import Flask, render_template, request, redirect, session
import psycopg2  # Changed from mysql.connector to psycopg2
import os
from psycopg2 import sql

app = Flask(__name__)
app.secret_key = os.urandom(30)

# PostgreSQL connection parameters - update these with your credentials
conn = psycopg2.connect(
    host='localhost',
    user='postgres',  # default PostgreSQL user is 'postgres'
    password='621424',  # your PostgreSQL password
    database='deepscope'
)
cursor = conn.cursor()

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')


@app.route('/home')
def home():
    if 'user_id' in session:
        return render_template('home.html')
    else:
        return redirect('/')
    
@app.route('/founder')  
def founder():
    return render_template('founder.html')

@app.route('/login_validation', methods=['POST'])
def login_validation():
    email = request.form.get('email')
    password = request.form.get('password')
    
    # Input validation
    if not email and not password:
        return render_template('login.html', error_message="Please enter your credentials.")
    if not email:
        return render_template('login.html', error_message="Please enter your email.")
    if not password:
        return render_template('login.html', error_message="Please enter your password.")
    
    # Secure database query with parameterized inputs
    try:
        query = sql.SQL("SELECT * FROM registered_users WHERE email = %s AND password = %s")
        cursor.execute(query, (email, password))
        users = cursor.fetchall()
        
        if users:  # If credentials are correct
            session['user_id'] = users[0][0]  # Store user ID in session
            return redirect('/home')  # Redirect to home page
        else:
            return render_template('login.html', error_message="Invalid credentials. Please Register first.")
    
    except Exception as e:
        # Log the error for debugging
        print(f"Database error: {str(e)}")
        return render_template('login.html', error_message="Login failed. Please try again later.")

@app.route('/register_validation', methods=['POST'])
def register_validation():
    import re
    # Get form data
    name = request.form.get('uname')
    email = request.form.get('uemail')
    password = request.form.get('upassword')
    
    # Check if all fields are provided
    if not name and not email and not password:
        return render_template('register.html', error_message="Please enter all your credentials.")
    if not name:
        return render_template('register.html', error_message="Please enter your name.")
    if not email:
        return render_template('register.html', error_message="Please enter your email.")
    
    elif not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        return render_template('register.html', error_message="Invalid email format.")
    
    if not password:
        return render_template('register.html', error_message="Please enter your password.")
    
    # Validate name (no numeric values)
    if name and any(char.isdigit() for char in name):
        return render_template('register.html', error_message="Name must contain only alphabets.")
    
    # If all validations pass, proceed with database operation
    try:
        # PostgreSQL uses %s as placeholder and SERIAL for auto-increment
        query = sql.SQL("INSERT INTO registered_users (name, email, password) VALUES (%s, %s, %s) RETURNING user_id")
        cursor.execute(query, (name, email, password))
        # Get the auto-generated user_id
        user_id = cursor.fetchone()[0]
        conn.commit()
        # You might want to automatically log the user in after registration
        session['user_id'] = user_id
        return redirect('/home')
    except Exception as e:
        conn.rollback()
        print(f"Registration error: {str(e)}")
        if "duplicate key" in str(e).lower():
            return render_template('register.html', error_message="Email already exists. Please use a different email.")
        return render_template('register.html', error_message="Registration failed. Please try again.")


@app.route('/submit_contact', methods=['POST'])
def submit_contact():
    if request.method == 'POST':
        try:
            name = request.form.get('name')
            email = request.form.get('email')
            company = request.form.get('company')
            message = request.form.get('message')
            
            # Insert into database
            query = sql.SQL("""
                INSERT INTO messages (name, email, company, message) 
                VALUES (%s, %s, %s, %s)
            """)
            cursor.execute(query, (name, email, company, message))
            conn.commit()
            
            return {'status': 'success', 'message': 'Thank you for your message!'}
        except Exception as e:
            conn.rollback()
            print(f"Error saving message: {str(e)}")
            return {'status': 'error', 'message': 'Failed to send message. Please try again.'}, 500
        

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)