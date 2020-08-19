CREATE TABLE IF NOT EXISTS UTENTE(
                Id INT AUTO_INCREMENT PRIMARY KEY,
                Username CHAR(5) NOT NULL UNIQUE, 
                Password VARCHAR(10) NOT NULL,
                MatricolaRegionale VARCHAR(10) NOT NULL UNIQUE, 
                Nome VARCHAR(50) NOT NULL, 
                Cognome VARCHAR(50) NOT NULL, 
                Residenza VARCHAR(50) NOT NULL, 
                Indirizzo VARCHAR(50) NOT NULL, 
				DataNascita DATE NOT NULL, 
                CF VARCHAR(20) NOT NULL UNIQUE,
                Sesso CHAR NOT NULL,
                Cellulare INT NOT NULL UNIQUE,
                Telefono VARCHAR(10) UNIQUE, 
                Email VARCHAR(50) NOT NULL UNIQUE,
                Qualifica VARCHAR(50) NOT NULL,
                CodiceZona VARCHAR(10) NOT NULL, 
                Ruolo VARCHAR(15) NOT NULL, 
                Stato VARCHAR(10) NOT NULL);
                
CREATE TABLE IF NOT EXISTS ZONA(
                CodiceZona VARCHAR(10), 
                CodiceArea VARCHAR(10),
                Nome VARCHAR(50) NOT NULL UNIQUE,
                IdResponsabile INT, 
                PRIMARY KEY (CodiceZona,CodiceArea));
                
CREATE TABLE IF NOT EXISTS AREA(
                CodiceArea VARCHAR(10) PRIMARY KEY, 
                Luogo VARCHAR(50) NOT NULL UNIQUE);
                
CREATE TABLE IF NOT EXISTS PARTECIPASQUADRA(
                NomeSquadra VARCHAR(10), 
                Id INT, 
                PRIMARY KEY (NomeSquadra,Id));   
CREATE TABLE IF NOT EXISTS SQUADRA(
                NomeSquadra VARCHAR(10) PRIMARY KEY,
				IdResponsabile INT);

ALTER TABLE UTENTE ADD FOREIGN KEY (CodiceZona) REFERENCES ZONA(CodiceZona);
ALTER TABLE ZONA ADD FOREIGN KEY (CodiceArea) REFERENCES AREA(CodiceArea);
ALTER TABLE ZONA ADD FOREIGN KEY (IdResponsabile) REFERENCES UTENTE(Id);
ALTER TABLE PARTECIPASQUADRA ADD FOREIGN KEY (NomeSquadra) REFERENCES SQUADRA(NomeSquadra);
ALTER TABLE PARTECIPASQUADRA ADD FOREIGN KEY (Id) REFERENCES UTENTE(Id);
ALTER TABLE SQUADRA ADD FOREIGN KEY (IdResponsabile) REFERENCES UTENTE(Id);







                
                