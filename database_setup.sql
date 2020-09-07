CREATE TABLE IF NOT EXISTS UTENTE(
                Id INT AUTO_INCREMENT PRIMARY KEY,
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
                Stato VARCHAR(10) NOT NULL,
                Subscription JSON,
                Operativo BOOLEAN DEFAULT FALSE);
                
CREATE TABLE IF NOT EXISTS ZONA(
                CodiceZona VARCHAR(10), 
                CodiceArea VARCHAR(10),
                Nome VARCHAR(50) NOT NULL UNIQUE,
                IdResponsabile INT, 
                PRIMARY KEY (CodiceZona,CodiceArea));
                
CREATE TABLE IF NOT EXISTS AREA(
                CodiceArea VARCHAR(10) PRIMARY KEY, 
                Luogo VARCHAR(50) NOT NULL UNIQUE);
                
CREATE TABLE IF NOT EXISTS SQUADRA(
                Id INT AUTO_INCREMENT PRIMARY KEY,
                NomeSquadra VARCHAR(20) NOT NULL,
				IdResponsabile INT NOT NULL,
                Stato CHAR NOT NULL DEFAULT 'I', /*I = inattiva, A = attiva, E = eliminata*/
                DataCreazione TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP);
                
CREATE TABLE IF NOT EXISTS PARTECIPASQUADRA(
                IdSquadra INT,
                IdUtente INT,
                PRIMARY KEY (IdSquadra,IdUtente));
                
CREATE TABLE IF NOT EXISTS POSIZIONE(
                IdUtente INT,
                DataRicezione TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                Latitudine DECIMAL(10,8) NOT NULL,
                Longitudine DECIMAL(11,8) NOT NULL,
                Accuratezza INT DEFAULT NULL,
                Altitudine INT DEFAULT NULL,
                AccuratezzaAltitudine INT DEFAULT NULL,
                Direzione INT DEFAULT NULL,
                Velocita INT DEFAULT NULL,
                NodoPercorso CHAR DEFAULT NULL,
                PRIMARY KEY (IdUtente,DataRicezione));

ALTER TABLE UTENTE ADD FOREIGN KEY (CodiceZona) REFERENCES ZONA(CodiceZona);
ALTER TABLE ZONA ADD FOREIGN KEY (CodiceArea) REFERENCES AREA(CodiceArea);
ALTER TABLE ZONA ADD FOREIGN KEY (IdResponsabile) REFERENCES UTENTE(Id);
ALTER TABLE SQUADRA ADD FOREIGN KEY (IdResponsabile) REFERENCES UTENTE(Id);
ALTER TABLE PARTECIPASQUADRA ADD FOREIGN KEY (IdSquadra) REFERENCES SQUADRA(Id);
ALTER TABLE PARTECIPASQUADRA ADD FOREIGN KEY (IdUtente) REFERENCES UTENTE(Id);
ALTER TABLE POSIZIONE ADD FOREIGN KEY (IdUtente) REFERENCES UTENTE(Id);









                
                