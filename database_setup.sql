CREATE TABLE IF NOT EXISTS UTENTE(
                Id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
                Username CHAR(5) NOT NULL UNIQUE, 
                Password CHAR(64) NOT NULL,
                MatricolaRegionale VARCHAR(10) NOT NULL UNIQUE, 
                Nome VARCHAR(50) NOT NULL, 
                Cognome VARCHAR(50) NOT NULL, 
                Residenza VARCHAR(50) NOT NULL, 
                Indirizzo VARCHAR(50) NOT NULL, 
				DataNascita DATE NOT NULL, 
                CF VARCHAR(20) NOT NULL UNIQUE,
                Sesso CHAR NOT NULL,
                Cellulare VARCHAR(20) NOT NULL UNIQUE,
                Telefono VARCHAR(20) UNIQUE, 
                TelegramUsername VARCHAR(50) UNIQUE,
                Email VARCHAR(50) NOT NULL UNIQUE,
                Qualifica VARCHAR(50) NOT NULL,
                CodiceZona VARCHAR(10) NOT NULL,
                Ruolo VARCHAR(15) NOT NULL, 
                Stato VARCHAR(10) NOT NULL DEFAULT 'attivo',
                Subscription JSON,
                Operativo BOOLEAN DEFAULT FALSE);
                
CREATE TABLE IF NOT EXISTS ZONA(
                CodiceZona VARCHAR(10), 
                CodiceArea VARCHAR(10),
                Nome VARCHAR(50) NOT NULL UNIQUE,
                IdResponsabile INT UNSIGNED, 
                PRIMARY KEY (CodiceZona,CodiceArea));
                
CREATE TABLE IF NOT EXISTS AREA(
                CodiceArea VARCHAR(10) PRIMARY KEY, 
                Luogo VARCHAR(50) NOT NULL UNIQUE);
                
CREATE TABLE IF NOT EXISTS SQUADRA(
                Id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
                NomeSquadra VARCHAR(20) NOT NULL,
				IdResponsabile INT UNSIGNED NOT NULL,
                Stato CHAR NOT NULL DEFAULT 'I', 
                DataCreazione TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP);
                
CREATE TABLE IF NOT EXISTS PARTECIPASQUADRA(
                IdSquadra INT UNSIGNED,
                IdUtente INT UNSIGNED,
                PRIMARY KEY (IdSquadra,IdUtente));
                
CREATE TABLE IF NOT EXISTS POSIZIONE(
                IdUtente INT UNSIGNED,
                DataRicezione TIMESTAMP(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
                DataInvio TIMESTAMP NOT NULL,
                Latitudine DECIMAL(10,8) NOT NULL,
                Longitudine DECIMAL(11,8) NOT NULL,
                Accuratezza INT DEFAULT NULL,
                Altitudine INT DEFAULT NULL,
                AccuratezzaAltitudine INT DEFAULT NULL,
                Direzione INT DEFAULT NULL,
                Velocita INT DEFAULT NULL,
                NodoPercorso CHAR DEFAULT NULL,
                PRIMARY KEY (IdUtente,DataRicezione));
                
CREATE TABLE IF NOT EXISTS INTERVENTO(
				Id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
                Indirizzo VARCHAR(50) NOT NULL,
				Latitudine DECIMAL(10,8) NOT NULL,
                Longitudine DECIMAL(11,8) NOT NULL,
                IdSquadra INT UNSIGNED,
                NomeRichiedente VARCHAR(50) NOT NULL,
                CognomeRichiedente VARCHAR(50),
                TelefonoRichiedente VARCHAR(20),
                TipoSegnalazione VARCHAR(20) NOT NULL,
                Note TEXT,
                MaterialeNecessario TEXT,
                IdUtente INT UNSIGNED NOT NULL, /*UTENTE CHE HA INSERITO LA SEGNALAZIONE*/
                DataRicezione TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                DataInizioIntervento TIMESTAMP,
                DataFineIntervento TIMESTAMP,
                CodiceColore TINYINT NOT NULL,
                Tipologia CHAR NOT NULL,
				Stato CHAR NOT NULL DEFAULT 'A' 
);

CREATE TABLE IF NOT EXISTS FOTO(
              Id INT UNSIGNED AUTO_INCREMENT,
              IdIntervento INT UNSIGNED,
              IdUtente INT UNSIGNED NOT NULL, /*UTENTE CHE HA INSERITO LA SEGNALAZIONE*/
              Foto VARCHAR(255) NOT NULL, /*PATH FOTO*/
              DataRicezione TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
              PRIMARY KEY (Id,IdIntervento));
              
CREATE TABLE IF NOT EXISTS REPORT(
              Id INT UNSIGNED AUTO_INCREMENT,
              IdIntervento INT UNSIGNED,
              IdUtente INT UNSIGNED NOT NULL, /*UTENTE CHE HA INSERITO LA SEGNALAZIONE*/
              Report VARCHAR(255) NOT NULL, /*PATH REPORT*/
			  DataRicezione TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
              PRIMARY KEY (Id,IdIntervento));









                
                