CREATE DATABASE dostawy;
USE dostawy;

CREATE TABLE IF NOT EXISTS Kurierzy (
    KurierID INT NOT NULL,
    Imie VARCHAR(50) NOT NULL,
    Miasto VARCHAR(50) NOT NULL,
    CzyDostepny TINYINT NOT NULL,
    PRIMARY KEY(KurierID)
);

TRUNCATE TABLE Kurierzy;
INSERT INTO Kurierzy
	(KurierID, Imie, Miasto, CzyDostepny)
VALUES
	('123','Piotr', 'Warszawa', '1'),
    ('176','Marcin', 'Warszawa', '0'),
    ('234','Artur', 'Wrocław', '1'),
    ('235','Alicja', 'Warszawa', '0'),
    ('456','Marek', 'Leszno', '0'),
    ('555','Leszek', 'Opole', '1'),
    ('612','Piotr', 'Katowice', '1');
       
CREATE TABLE IF NOT EXISTS Przesylki (
    PrzesylkaID INT NOT NULL AUTO_INCREMENT,
    Nadawca VARCHAR(100) NOT NULL,
    DataNadania DATE NOT NULL,
	MiastoDostarczenia VARCHAR(100) NOT NULL,
    Kurier INT,
    DataDostarczenia DATE,
    PRIMARY KEY(PrzesylkaID),
    FOREIGN KEY(Kurier) REFERENCES Kurierzy(KurierID)
);

TRUNCATE TABLE Przesylki;
INSERT INTO Przesylki
	(Nadawca, DataNadania, MiastoDostarczenia, Kurier, DataDostarczenia)
VALUES
	('Nowak Jan', '2021-04-20', 'Wrocław', '234', '2021-05-03'),
	('Urzad Miasta Wroclaw', '2021-05-10', 'Warszawa', '176', NULL),
	('Dudek Tomasz', '2021-04-30', 'Poznań', NULL, NULL),
	('Bakula Joanna', '2021-05-11', 'Wrocław', NULL, NULL),
	('IDEA Oddzial Warszawa', '2021-04-25', 'Opole', '555', '2021-04-28'),
	('Bank Polski',  '2018-05-05', 'Warszawa', '235', NULL);

	
