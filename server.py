from flask import Flask, render_template, request, session, flash, redirect, url_for
from flask_mysqldb import MySQL

app = Flask(__name__)

# MySQL configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'database'
app.config['MYSQL_DB'] = 'database'

app.secret_key = 'yoursecretkey'  # TODO to be changed

# TODO PASSWORD encryption into db

mysql = MySQL(app)


# database setup
def database_setup():
    try:
        with app.app_context():
            cursor = mysql.connection.cursor()
            cursor.execute(
                "CREATE TABLE IF NOT EXISTS UTENTE("
                "Id INT(10) UNSIGNED AUTO_INCREMENT PRIMARY KEY, "
                "Username CHAR(5) NOT NULL, "
                "Password VARCHAR(10) NOT NULL,"
                "MatricolaRegionale VARCHAR(10) NOT NULL, "
                "Nome VARCHAR(50) NOT NULL, "
                "Cognome VARCHAR(50) NOT NULL, "
                "Residenza VARCHAR(50) NOT NULL, "
                "Indirizzo VARCHAR(50) NOT NULL, "
                "DataNascita DATE NOT NULL, "
                "CF VARCHAR(20) NOT NULL, "
                "Cellulare INT(10) NOT NULL,"
                "Telefono VARCHAR(10), "
                "Qualifica VARCHAR(50) NOT NULL,"
                "CodiceZona VARCHAR(10) NOT NULL REFERENCES ZONA(CodiceZona), "
                "Ruolo VARCHAR(10) NOT NULL, "
                "Stato VARCHAR(10) NOT NULL)")
            mysql.connection.commit()
    except Exception as exception:
        print(exception)
    try:
        with app.app_context():
            cursor = mysql.connection.cursor()
            cursor.execute(
                "CREATE TABLE IF NOT EXISTS ZONA("
                "CodiceZona VARCHAR(10), "
                "CodiceArea VARCHAR(10) REFERENCES AREA(CodiceArea), "
                "Luogo VARCHAR(50) NOT NULL, "
                "MatricolaResponsabile VARCHAR(10) REFERENCES UTENTE(MatricolaResponsabile), "
                "PRIMARY KEY (CodiceZona,CodiceArea))")
            mysql.connection.commit()
    except Exception as exception:
        print(exception)

    try:
        with app.app_context():
            cursor = mysql.connection.cursor()
            cursor.execute(
                "CREATE TABLE IF NOT EXISTS AREA("
                "CodiceArea VARCHAR(10) PRIMARY KEY, "
                "Luogo VARCHAR(50) NOT NULL)")
            mysql.connection.commit()
    except Exception as exception:
        print(exception)

    try:
        with app.app_context():
            cursor = mysql.connection.cursor()
            cursor.execute(
                "CREATE TABLE IF NOT EXISTS PARTECIPASQUADRA("
                "NomeSquadra VARCHAR(10) REFERENCES SQUADRA(NomeSquadra), "
                "Matricola VARCHAR(10) REFERENCES UTENTE(MatricolaRegionale), "
                "PRIMARY KEY (NomeSquadra,Matricola))")
            mysql.connection.commit()
    except Exception as exception:
        print(exception)

    try:
        with app.app_context():
            cursor = mysql.connection.cursor()
            cursor.execute(
                "CREATE TABLE IF NOT EXISTS SQUADRA("
                "NomeSquadra VARCHAR(10) PRIMARY KEY,"
                "MatricolaResponsabile VARCHAR(10) REFERENCES UTENTE(MatricolaRegionale))")
            mysql.connection.commit()
    except Exception as exception:
        print(exception)


    try:
        with app.app_context():
            cursor = mysql.connection.cursor()
            cursor.execute(
                "INSERT INTO AREA VALUES ('A','SOVERE')")
            cursor.execute(
                "INSERT INTO ZONA VALUES ('A','A','SOVERE',NULL)")
            cursor.execute(
                "INSERT INTO UTENTE VALUES (1,'00000','00000','0','M','V','A','A','00/1/1','AA',035,035,'A','A','MASTER','Attivo')")
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
        cursor.execute('SELECT * FROM UTENTE WHERE username = %s AND password = %s', (username, password))
        account = cursor.fetchone

        #control if the account is an active one
        if account:
            if str(account[15]) == "Attivo":
                # Create session data, we can access this data in other routes
                session['loggedin'] = True
                session['userId'] = account[0]

                # implements Remember Me function
                if remember_me:
                    session.permanent = True

                # Redirect to home page
                return redirect(url_for('home'))
            elif str(account[15]) == "Eliminato":
                flash("Errore! Account eliminato!")

            elif str(account[15]) == "Sospeso":
                flash("Errore! Account Sospeso!")

        else:
            # Account doesn't exist or username/password incorrect
            flash("Incorrect username/password!")

    return render_template("login.html")


# database initialization
database_setup()

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
