from flask import Flask, render_template, request, session, flash, redirect, url_for
from flask_mysqldb import MySQL

app = Flask(__name__)

# MySQL configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'database'
app.config['MYSQL_DB'] = 'database'

app.secret_key = 'yoursecretkey '  # TODO to be changed

# TODO PASSWORD encryption into db

mysql = MySQL(app)

@app.route('/')
def index():
    if 'logged_in' in session:
        if session['logged_in'] == True:
            return render_template('index.html')
    else:
        return redirect(url_for('login'))

@app.route('/homepage')
def homepage():
    if 'logged_in' in session:
        if session['logged_in'] == True:
            cursor = mysql.connection.cursor()
            cursor.execute('SELECT Nome,Cognome,Ruolo,CodiceZona FROM UTENTE WHERE id = %s', [session['user_id']])
            user = cursor.fetchone()
            cursor.execute('SELECT Nome FROM ZONA WHERE CodiceZona = %s', [user[3]])
            zone = cursor.fetchone()
            return render_template('homepage.html',user_name = user[0],user_surname = user[1], user_role = user[2], user_zone = str(zone[0]).upper())
    else:
        return redirect(url_for('login'))


@app.route('/service-worker.js')
def sw():
    return app.send_static_file('service-worker.js')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for access
        username = request.form['username']
        password = request.form['password']
        remember_me = request.form.get('rememberMe')

        cursor = mysql.connection.cursor()
        cursor.execute('SELECT Id,Stato FROM UTENTE WHERE username = %s AND password = %s', [username, password])
        account = cursor.fetchone()
        #control if the account is an active one
        if account:
            if str(account[1]) == "Attivo":
                # Create session data, we can access this data in other routes
                session['logged_in'] = True
                session['user_id'] = account[0]

                # implements Remember Me function
                if remember_me:
                    session.permanent = True

                # Redirect to home page
                return redirect(url_for('index'))

            elif str(account[1]) == "Eliminato":
                flash("Errore! Account eliminato!")

            elif str(account[1]) == "Sospeso":
                flash("Errore! Account Sospeso!")

        else:
            # Account doesn't exist or username/password incorrect
            flash("Incorrect username/password!")

    return render_template("login.html")

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
