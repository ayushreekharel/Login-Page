from flask import Flask,render_template,request,redirect,url_for,flash,session
from flask_mysqldb import MySQL
from datetime import datetime
from config import Config

app=Flask(__name__)
app.config.from_object(Config)
mysql=MySQL(app)

app.secret_key='****'


@app.route('/')
def hello_world():
    print("heyy")
    return render_template('login.html')



@app.route('/form_login',methods=['POST','GET'])
def login():
     if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM login_signup WHERE username = %s AND confirm_password = %s", (username, password))
        user = cur.fetchone()
        cur.close()

        if user:
            user_id = user[0]
            session['user_id'] = user_id
            return render_template('home.html')
        else:
            return render_template('login.html', error='Invalid username or password')
     return render_template('login.html')



@app.route('/create_account', methods=['POST', 'GET'])
def create():
    if request.method == 'POST':
        first_name = request.form['first_name']
        middle_name = request.form['middle_name']
        last_name = request.form['last_name']
        phone_number = request.form['phone_number']
        email = request.form['email']
        username = request.form['username']
        set_password = request.form['set_password']
        confirm_password = request.form['confirm_password']
        

        if set_password != confirm_password:
            flash("Passwords do not match")
            return render_template('signup.html')
        else:
            cur = mysql.connection.cursor()
            cur.execute("SELECT * FROM login_signup WHERE username = %s OR email = %s", (username, email))
            existing_user = cur.fetchone()
            if existing_user:
                flash("Username or email already exists", "error")
                return render_template('signup.html')

            else:
                cur.execute("INSERT INTO login_signup (first_name,middle_name,last_name,phone_no,email, username,set_password,confirm_password) VALUES (%s, %s, %s,%s, %s,%s, %s, %s)", (first_name,middle_name,last_name,phone_number,email, username, set_password,confirm_password))
                mysql.connection.commit()
                cur.close()
                
                return redirect(url_for('login'))
    return render_template('signup.html')

if __name__ == "__main__":
    app.run(debug=True)