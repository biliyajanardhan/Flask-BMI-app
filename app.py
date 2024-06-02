from flask import Flask, render_template, request,redirect,url_for
from db import connect_db
from function import underweight_diet,obese_diet,overweight_diet,normal_diet
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        username = request.form.get('username')
        password = request.form.get('password')

        conn = connect_db()
        cur = conn.cursor()

        try:
            # Insert data into PostgreSQL table
            cur.execute("INSERT INTO login (name, username, password,usertype) VALUES (%s, %s, %s,%s)", (name, username, password,'user'))
            conn.commit()
            cur.close()
            conn.close()
            message = "Registration successful!"
            return render_template('login.html', message=message)  # Return a response indicating success
        except Exception as e:
            return f'Error: {str(e)}', 500  # Return error response if registration fails

    # If request method is GET or any other method, render the registration form
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Get username and password from the form
        username = request.form.get('username')
        password = request.form.get('password')

        # Connect to the database
        conn = connect_db()
        cur = conn.cursor()

        # Check if the username and password match and fetch the user type
        cur.execute("SELECT name, usertype FROM login WHERE username = %s AND password = %s", (username, password))
        user = cur.fetchone()

        # Close database connection
        cur.close()
        conn.close()

        if user:
            name, usertype = user
            if usertype == 'admin':
                # Redirect to admin1.html for admin users
                return render_template('admin1.html', name=name)
            elif usertype == 'user':
                # Redirect to admin.html for regular users
                return render_template('admin.html', name=name)
        else:
            return render_template('login.html', message="Invalid username or password")

    return render_template('login.html')


@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/admin1')
def admin1():
    return render_template('admin1.html')


@app.route('/normal_exercise')
def normal_exercise():
    return render_template('normal_exercise.html')

@app.route('/normal_doctor')
def normal_doctor():
    return render_template('normal_doctor.html')

@app.route('/underweight_exercise')
def underweight_exercise():
    return render_template('underweight_exercise.html')

@app.route('/underweight_doctor')
def underweight_doctor():
    return render_template('underweight_doctor.html')

@app.route('/overweight_exercise')
def overweight_exercise():
    return render_template('overweight_exercise.html')

@app.route('/overweight_doctor')
def overweight_doctor():
    return render_template('overweight_doctor.html')


@app.route('/obese_exercise')
def obese_exercise():
    return render_template('obese_exercise.html')

@app.route('/obese_doctor')
def obese_doctor():
    return render_template('obese_doctor.html')


@app.route('/bmi_calculator', methods=['GET', 'POST'])
def bmi():
    return render_template('bmi.html')
@app.route('/bmi_normal', methods=['GET', 'POST'])
def bmi_normal():
    vegetarian_diet, non_vegetarian_diet = normal_diet()
    return render_template('normal.html', title="Normal Diet Plan", 
                           vegetarian_diet=vegetarian_diet, 
                           non_vegetarian_diet=non_vegetarian_diet)

@app.route('/underweight')
def underweight():
    vegetarian_diet, non_vegetarian_diet = underweight_diet()
    return render_template('underweight.html', title="Underweight Diet Plan", 
                           vegetarian_diet=vegetarian_diet, 
                           non_vegetarian_diet=non_vegetarian_diet)

@app.route('/overweight')
def overweight():
    vegetarian_diet, non_vegetarian_diet = overweight_diet()
    return render_template('overweight.html', title="Overweight Diet Plan", 
                           vegetarian_diet=vegetarian_diet, 
                           non_vegetarian_diet=non_vegetarian_diet)

@app.route('/obese')
def obese():
    vegetarian_diet, non_vegetarian_diet = obese_diet()
    return render_template('obese.html', title="Obesity Diet Plan", 
                           vegetarian_diet=vegetarian_diet, 
                           non_vegetarian_diet=non_vegetarian_diet)
@app.route('/viewuser')
def manage_users():
    # Admin functionality to manage users
    # Connect to the database and fetch user data where usertype is 'user'
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT name, username, password FROM login WHERE usertype = 'user'")
    users = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('manage_users.html', users=users, enumerate=enumerate)


@app.route('/logout')
def logout():
    return render_template('index.html') 


if __name__ == '__main__':
    app.run(debug=True)
