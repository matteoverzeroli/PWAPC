from distutils.command.config import config

from flask import Flask, render_template, request, session, flash, redirect, url_for, jsonify
from flask_mysqldb import MySQL

app = Flask(__name__)

# MySQL configuration #TODO TO BE CHANGED
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'database'
app.config['MYSQL_DB'] = 'database'

app.secret_key = 'yoursecretkey '  # TODO to be changed

mysql = MySQL(app)


@app.route('/')
def index():
    if 'logged_in' in session:
        if session['logged_in'] == True:
            return redirect(url_for('homepage'))
    else:
        return redirect(url_for('login'))


@app.route('/homepage', methods=['GET'])
def homepage():
    if 'logged_in' in session:
        if session['logged_in'] == True:

            return render_template('homepage.html')
        else:
            return redirect(url_for('login'))
    else:
        return redirect(url_for('login'))


@app.route('/modificadatiutente', methods=['POST'])
def modifica_dati_utente():
    if 'logged_in' in session:
        print(request.form)

        if session['logged_in'] == True and 'form_modificadatiutente' in request.form:
            print("ok")
            cursor = mysql.connection.cursor()
            cursor.execute(
                "UPDATE UTENTE SET Nome = %s,Cognome = %s,Residenza = %s,Indirizzo = %s,DataNascita = %s,CF = %s,Sesso = %s,Cellulare = %s,Telefono = %s,TelegramUsername = %s,Email = %s WHERE Id = %s",
                [request.form['user_name'], request.form['user_surname'], request.form['user_residency'],
                 request.form['user_address'], request.form['user_birthday'], request.form['user_CF'],
                 request.form['user_sex'], request.form['user_mobile_phone'], request.form['user_telephone'],
                 request.form['user_telegram_account'], request.form['user_email'], session['user_id']])
            mysql.connection.commit()
        return redirect(url_for('homepage'))
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
        cursor.execute("SELECT Id,Stato FROM UTENTE WHERE username = %s AND password = SHA2(%s,256)",
                       [username, password])
        account = cursor.fetchone()
        # control if the account is an active one
        if account:
            if str(account[1]) == "Attivo":
                # Create session data, we can access this data in other routes
                session['logged_in'] = True
                session['user_id'] = account[0]

                # implements Remember Me function
                if remember_me:
                    session.permanent = True

                # Redirect to home page
                return redirect(url_for('homepage'))

            elif str(account[1]) == "Eliminato":
                flash("Errore! Account eliminato!")

            elif str(account[1]) == "Sospeso":
                flash("Errore! Account Sospeso!")

        else:
            # Account doesn't exist or username/password incorrect
            flash("Incorrect username/password!")

    return render_template("login.html")


@app.route('/get_user_data', methods=["POST"])
def get_user_data():
    if 'logged_in' in session:
        if session['logged_in']:
            cursor = mysql.connection.cursor()
            cursor.execute(
                "SELECT Username,MatricolaRegionale,Nome,Cognome,Residenza,Indirizzo,DataNascita,CF,Sesso,Cellulare,Telefono,TelegramUsername,Email,Qualifica,CodiceZona,Ruolo,Stato FROM UTENTE WHERE id = %s",
                [session['user_id']])
            user = cursor.fetchone()
            user_data = {
                'username': user[0],
                'regional_id': user[1],
                'name': user[2],
                'surname': user[3],
                'residency': user[4],
                'address': user[5],
                'birthday': user[6],
                'CF': user[7],
                'sex': user[8],
                'mobile_phone': user[9],
                'telephone': user[10],
                'telegram_username': user[11],
                'email': user[12],
                'qualification': user[13],
                'zone': user[14],
                'role': user[15],
                'state': user[16]
            }

            cursor.execute("SELECT Nome FROM ZONA WHERE CodiceZona = %s", [user_data['zone']])
            zone = cursor.fetchone()
            zone_data = {
                'name': zone[0]
            }
            cursor.execute(
                "SELECT S.NomeSquadra,S.Stato,U.Nome,U.Cognome,U.Cellulare,U.TelegramUsername,U.Email FROM SQUADRA AS S JOIN PARTECIPASQUADRA AS P ON S.Id = P.IdSquadra "
                "JOIN UTENTE U ON S.IdResponsabile = U.Id WHERE (S.Stato = 'A' OR S.Stato = 'I' ) AND P.IdUtente = %s",
                [session['user_id']])
            squadra = cursor.fetchone()

            team_data = {}  # dictionary contains team data
            contact_data = {}  # dictionary contains team master contact data

            if squadra:
                team_data['state'] = get_team_state(squadra[1])
                team_data['master'] = str(squadra[2]) + " " + str(squadra[3])
                team_data['name'] = squadra[0]
                contact_data['mobile_phone'] = squadra[4]
                contact_data['whatsapp'] = squadra[4]
                contact_data['telegram'] = squadra[5]
                contact_data['email'] = squadra[6]
            else:
                team_data['state'] = get_team_state('I')
                team_data['master'] = "Nessun Responsabile"

            return jsonify(user_data=user_data, team_data=team_data, zone_data=zone_data, contact_data=contact_data)
        else:
            return redirect(url_for('login'))
    else:
        return redirect(url_for('login'))


def get_team_state(stato):
    if stato == 'A':
        return 'attivo'
    elif stato == 'I':
        return 'inattivo'


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
