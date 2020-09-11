
ALTER TABLE UTENTE ADD FOREIGN KEY (CodiceZona) REFERENCES ZONA(CodiceZona);

ALTER TABLE ZONA ADD FOREIGN KEY (CodiceArea) REFERENCES AREA(CodiceArea);
ALTER TABLE ZONA ADD FOREIGN KEY (IdResponsabile) REFERENCES UTENTE(Id);

ALTER TABLE SQUADRA ADD FOREIGN KEY (IdResponsabile) REFERENCES UTENTE(Id);

ALTER TABLE PARTECIPASQUADRA ADD FOREIGN KEY (IdSquadra) REFERENCES SQUADRA(Id);
ALTER TABLE PARTECIPASQUADRA ADD FOREIGN KEY (IdUtente) REFERENCES UTENTE(Id);

ALTER TABLE POSIZIONE ADD FOREIGN KEY (IdUtente) REFERENCES UTENTE(Id);

ALTER TABLE INTERVENTO ADD FOREIGN KEY (IdUtente) REFERENCES UTENTE(Id);
ALTER TABLE INTERVENTO ADD FOREIGN KEY (IdSquadra) REFERENCES SQUADRA(Id);

ALTER TABLE FOTO ADD FOREIGN KEY (IdUtente) REFERENCES UTENTE(Id);
ALTER TABLE FOTO ADD FOREIGN KEY (IdIntervento) REFERENCES INTERVENTO(Id);

ALTER TABLE REPORT ADD FOREIGN KEY (IdUtente) REFERENCES UTENTE(Id);
ALTER TABLE FOTO ADD FOREIGN KEY (IdIntervento) REFERENCES INTERVENTO(Id);