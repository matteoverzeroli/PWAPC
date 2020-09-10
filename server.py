from flask import Flask, render_template, request, session, flash, redirect, url_for, jsonify
from flask_mysqldb import MySQL
import json
from pywebpush import webpush

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
        if session['logged_in']:
            return redirect(url_for('homepage'))
    else:
        return redirect(url_for('login'))


@app.route('/homepage', methods=['GET'])
def homepage():
    if 'logged_in' in session:
        if session['logged_in']:
            return render_template('homepage.html')
        else:
            return redirect(url_for('login'))
    else:
        return redirect(url_for('login'))


@app.route('/modificadatiutente', methods=['POST'])
def modifica_dati_utente():
    if 'logged_in' in session:
        if session['logged_in'] and 'form_modificadatiutente' in request.form:
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
    if 'logged_in' in session:
        if session['logged_in']:
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
                "SELECT Username,MatricolaRegionale,Nome,Cognome,Residenza,Indirizzo,DataNascita,CF,Sesso,Cellulare,Telefono,TelegramUsername,Email,Qualifica,CodiceZona,Ruolo,Stato,Operativo FROM UTENTE WHERE Id = %s",
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
                'state': user[16],
                'operative': user[17]
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
                team_data['name'] = "Nessuna Squadra!"
                team_data['state'] = get_team_state('I')
                team_data['master'] = "Nessun Responsabile!"

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


@app.route('/add_user_subscription', methods=["POST"])
def add_user_subscription():
    if 'logged_in' in session:
        if session['logged_in']:
            cursor = mysql.connection.cursor()
            cursor.execute("UPDATE UTENTE SET Subscription =  %s WHERE Id = %s",
                           [json.dumps(request.json), session['user_id']])
            mysql.connection.commit()
            return ("", 204)
        else:
            redirect(url_for('login'))
    else:
        redirect(url_for('login'))


@app.route('/set_user_operation_status', methods=["POST"])
def set_user_operation_status():
    if 'logged_in' in session:
        if session['logged_in']:
            cursor = mysql.connection.cursor()
            cursor.execute("UPDATE UTENTE SET Operativo =  %s WHERE Id = %s",
                           [request.json['operativo'], session['user_id']])
            mysql.connection.commit()

            if request.json['operativo'] == True:
                send_notification("STATO: OPERATIVO !!!")
            else:
                send_notification("STATO: NON OPERATIVO !!!")
            return ("", 204)
        else:
            return redirect(url_for('login'))
    else:
        return redirect(url_for('login'))


def send_notification(data):
    if 'logged_in' in session:
        if session['logged_in']:
            cursor = mysql.connection.cursor()
            cursor.execute("SELECT Subscription FROM UTENTE WHERE Id = %s", [session['user_id']])
            subscription_info = cursor.fetchone()

            cursor.execute("SELECT Valore FROM CHIAVE")
            vapid_private = cursor.fetchone()[0]

            webpush(json.loads(subscription_info[0]),
                    data=data,
                    vapid_private_key=vapid_private,
                    vapid_claims={"sub": "mailto:matteoverzeroli@live.it"})
        return redirect(url_for('login'))
    return redirect(url_for('login'))


@app.route('/set_user_position', methods=["POST"])
def set_user_position():
    if 'logged_in' in session:
        if session['logged_in']:
            pos = {
                'lat': float(request.json['lat']),
                'long': float(request.json['long']),
                'acc': int(request.json['acc']) if request.json['acc'] else None,
                'alt': int(request.json['alt']) if request.json['alt'] else None,
                'accalt': int(request.json['accalt']) if request.json['accalt'] else None,
                'heading': int(request.json['heading']) if request.json['heading'] else None,
                'speed': int(request.json['speed']) if request.json['speed'] else None,
                'node': request.json['node'] if request.json['node'] else None
            }
            try:
                cursor = mysql.connection.cursor()
                cursor.execute(
                    "INSERT INTO POSIZIONE(IdUtente,Latitudine,Longitudine,Accuratezza,Altitudine,AccuratezzaAltitudine,Direzione,Velocita,NodoPercorso) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                    [session['user_id'], pos['lat'], pos['long'], pos['acc'],
                     pos['alt'], pos['accalt'], pos['heading'], pos['speed'], pos['node']])
                mysql.connection.commit()

            except Exception as Exc:
                print(Exc)
                return (str(Exc), 501)
            return ("", 204)
        return redirect(url_for('login'))
    return redirect(url_for('login'))

@app.route('/get_team_list', methods=["POST"])
def get_team_list():
    if 'logged_in' in session:
        if session['logged_in']:
            cursor = mysql.connection.cursor()
            cursor.execute(
                "SELECT U.Nome,U.Cognome FROM UTENTE U JOIN PARTECIPASQUADRA P ON P.IdUtente = U.Id WHERE IdSquadra = ("
                "SELECT IdSquadra FROM PARTECIPASQUADRA WHERE IdUtente = %s)",
                [session['user_id']])
            team_list = cursor.fetchall()
            return jsonify(team_list)
        else:
            return redirect(url_for('login'))
    else:
        return redirect(url_for('login'))




if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
