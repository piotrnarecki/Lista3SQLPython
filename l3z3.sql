CREATE DATABASE sprzedaz;
USE sprzedaz;

CREATE TABLE IF NOT EXISTS Produkty (
    ProduktID INT NOT NULL AUTO_INCREMENT,
    Nazwa VARCHAR(50) NOT NULL,
    StanMagazywnowy INT NOT NULL,
    CenaJednostkowa FLOAT NOT NULL,
    PRIMARY KEY(ProduktID)
);

TRUNCATE TABLE Produkty;
INSERT INTO Kurierzy
	(Nazwa, StanMagazywnowy, CenaJednostkowa)
VALUES
    ('Victorinox Skipper','20', '199,99'),
    ('Leatherman Wingman','30','249,99'),
    ('Casio CA-53W','40','99,99');
    
    
       
CREATE TABLE IF NOT EXISTS Zamowienia (
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

	
