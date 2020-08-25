INSERT INTO AREA VALUES ('A','LAGO ISEO');
INSERT INTO ZONA VALUES ('A','A','SOVERE',NULL);
INSERT INTO UTENTE(Username,Password,MatricolaRegionale,Nome,Cognome,Residenza,Indirizzo,DataNascita,CF,Sesso,Cellulare,Telefono,Email,Qualifica,CodiceZona,Ruolo,Stato) VALUES ('00000','00000','0000','Matteo','Verzeroli','res','ind','00/1/1','CF','M',035,035,'A@A.IT','qua','A','Administrator','Attivo');
INSERT INTO SQUADRA VALUES ('Nomesqua','1');
UPDATE UTENTE SET NomeSquadra='Nomesqua' WHERE Id='1';