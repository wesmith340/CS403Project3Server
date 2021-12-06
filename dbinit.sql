DROP TABLE if EXISTS User;
CREATE TABLE User (
	User_TUID INT NOT NULL AUTO_INCREMENT,
	Username VARCHAR(64),
	FirstName VARCHAR(32),
	LastName VARCHAR(32),
	Password VARCHAR(32),
	PRIMARY KEY(User_TUID)
);

DROP TABLE if EXISTS TableTopGame;
CREATE TABLE TableTopGame (
	TableTopGame_TUID INT NOT NULL AUTO_INCREMENT,
	Organizer INT NOT NULL,
	EventName VARCHAR(64),
	GameName VARCHAR(64),
	GameCategory VARCHAR(64),
	EventDateTime DateTime,
	TotalOpenSlots INT,
	Latitude Double,
	Longitude Double,
	PRIMARY KEY(TableTopGame_TUID)
);

DROP TABLE if EXISTS Users_TableTopGame;
CREATE TABLE Users_TableTopGame (
	Users_TableTopGame_TUID INT NOT NULL AUTO_INCREMENT,
	User_TUID INT REFERENCES USER (User_TUID),
	TableTopGame_TUID INT REFERENCES TableTopGame (TableTopGame_TUID),
	PRIMARY KEY(Users_TableTopGame_TUID)
);

DROP TABLE if EXISTS GameCategories;
CREATE TABLE GameCategories (
	GameCategories_TUID INT NOT NULL AUTO_INCREMENT,
	Category VARCHAR(64),
	PRIMARY KEY(GameCategories_TUID)
);

INSERT INTO GameCategories (Category) VALUES
('Board game'),
('Card game'),
('Dice game'),
('Paper and pencil'),
('Tabletop role-playing'),
('Strategy'),
('Tile-based');

DROP TABLE if EXISTS TableTopGame_GameCategories;
CREATE TABLE TableTopGame_GameCategories(
	TableTopGame_GameCategories_TUID INT NOT NULL,
	TableTopGame_TUID INT REFERENCES TableTopGame (TableTopGame_TUID),
	GameCategories_TUID INT REFERENCES GameCategories (GameCategories_TUID), 
	PRIMARY KEY(TableTopGame_GameCategories_TUID)
);

