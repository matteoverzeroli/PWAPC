INSERT INTO AREA VALUES ('A','LAGO ISEO');
INSERT INTO ZONA VALUES ('A','A','SOVERE',NULL);
INSERT INTO UTENTE(Username,Password,MatricolaRegionale,Nome,Cognome,Residenza,Indirizzo,DataNascita,CF,Sesso,Cellulare,Telefono,TelegramUsername,Email,Qualifica,CodiceZona,Ruolo,Stato) VALUES ('00000',SHA2('0000000000',256),'0000','Matteo','Verzeroli','res','ind','00/1/1','CF','M',3407580457,393407580457,'matteoverzeroli','A@A.IT','qua','A','Administrator','Attivo');
INSERT INTO SQUADRA(NomeSquadra,IdResponsabile,Stato) VALUES ('Nomesquadra','1','A');
INSERT INTO PARTECIPASQUADRA(IdSquadra,IdUtente) VALUES ('1','1');
