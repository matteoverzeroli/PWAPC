from flask import Flask, render_template, request, session, flash, redirect, url_for
from flask_mysqldb import MySQL

app = Flask(__name__)

# MySQL configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'database'
app.config['MYSQL_DB'] = 'database'

app.secret_key = 'yoursecretkey '  # TODO to be changed

mysql = MySQL(app)

# database setup
def database_setup():
    try:
        with app.app_context():
            cursor = mysql.connection.cursor()
            cursor.execute(
                "CREATE TABLE IF NOT EXISTS UTENTI("
                "id INT(10) UNSIGNED AUTO_INCREMENT PRIMARY KEY, "
                "Username INT(5) NOT NULL, "
                "Password VARCHAR(10) NOT NULL, "
                "Nome VARCHAR(50) NOT NULL, "
                "Cognome VARCHAR(50) NOT NULL, "
                "Ruolo VARCHAR(10) NOT NULL, "
                "Stato VARCHAR(10) NOT NULL)")
            mysql.connection.commit()
    except Exception as exception:
        print(exception)
    try:
        with app.app_context():
            cursor = mysql.connection.cursor()
            cursor.execute(
            "INSERT INTO UTENTI(Username,Password,Nome,Cognome,Ruolo,Stato) VALUES (00000,'00000','Matteo','Verzeroli','Master','Attivo')")
            mysql.connection.commit()
    except Exception as exception:
        print(exception)


@app.route('/')
def home():
    if 'loggedin' in session:
        if session['loggedin'] == True:
            return render_template('index.html')
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
        cursor.execute('SELECT * FROM UTENTI WHERE username = %s AND password = %s', (username, password))
        account = cursor.fetchone()

        #TODO control if it is an active account
        if account:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['userId'] = account[0]

            if remember_me:
                session.permanent = True

            # Redirect to home page
            return redirect(url_for('home'))

        else:
            # Account doesnt exist or username/password incorrect
            flash("Incorrect username/password!")

    return render_template("login.html")

#database initialization
database_setup()

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
