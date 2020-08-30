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
            cursor.execute(
                "SELECT S.NomeSquadra,S.Stato,U.Nome,U.Cognome,U.Telefono,U.Cellulare,U.TelegramUsername,U.Email FROM SQUADRA AS S JOIN PARTECIPASQUADRA AS P ON S.Id = P.IdSquadra "
                "JOIN UTENTE U ON S.IdResponsabile = U.Id WHERE (S.Stato = 'A' OR S.Stato = 'I' ) AND P.IdUtente = %s",
                [session['user_id']])
            squadra = cursor.fetchone()
            if squadra:
                team_state = get_team_state(squadra[1])
                team_master = str(squadra[2]) + " " + str(squadra[3])
                team_name = squadra[0]
                contact_telephone = squadra[4]
                contact_whatsapp = squadra[5]
                contact_telegram = squadra[6]
                contact_email = squadra[7]
            else:
                team_state = get_team_state('I')
                team_master = "Nessun Responsabile"
            return render_template('homepage.html', user_username=user_data['username'],
                                   user_regional_id=user_data['regional_id'], user_name=user_data['name'],
                                   user_surname=user_data['surname'], user_residency=user_data['residency'],
                                   user_address=user_data['address'], user_birthday=user_data['birthday'],
                                   user_CF=user_data['CF'], user_sex=user_data['sex'],
                                   user_mobile_phone=user_data['mobile_phone'],
                                   user_telephone=user_data['telephone'],
                                   user_telegram_account=user_data['telegram_username'],
                                   user_email=user_data['email'],
                                   user_qualification=user_data['qualification'], user_role=user_data['role'],
                                   user_zone=str(zone[0]).upper(), team_name=team_name, team_state=team_state,
                                   team_master=team_master, contact_telephone=contact_telephone,
                                   contact_whatsapp=contact_whatsapp, contact_telegram=contact_telegram,
                                   contact_email=contact_email)
        else:
            return redirect(url_for('login'))
    else:
        return redirect(url_for('login'))


def get_team_state(stato):
    if stato == 'A':
        return 'attivo'
    elif stato == 'I':
        return 'inattivo'


@app.route('/modificadatiutente', methods=['POST'])
def modifica_dati_utente():
    if 'logged_in' in session:
        print(request.form)

        if session['logged_in'] == True and 'form_modificadatiutente' in request.form:
            print("ok")
            cursor = mysql.connection.cursor()
            cursor.execute(
                "UPDATE UTENTE SET Nome = %s,Cognome = %s,Residenza = %s,Indirizzo = %s,DataNascita = %s,CF = %s,Sesso = %s,Cellulare = %s,Telefono = %s,TelegramUsername = %s,Email = %s WHERE Id = %s",
                [request.form['user_name'],request.form['user_surname'],request.form['user_residency'],request.form['user_address'],request.form['user_birthday'],request.form['user_CF'],request.form['user_sex'],request.form['user_mobile_phone'],request.form['user_telephone'],request.form['user_telegram_account'],request.form['user_email'],session['user_id']])
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


@app.route('/jquery', methods=["POST"])
def add_numbers():
    if 'logged_in' in session:
        if session['logged_in'] == True:
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

            return jsonify(user_data=user_data)

        else:
            return redirect(url_for('login'))
    else:
        return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
