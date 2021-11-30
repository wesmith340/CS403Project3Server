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
	GameName VARCHAR(64),
	MeetingDateTime DateTime,
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