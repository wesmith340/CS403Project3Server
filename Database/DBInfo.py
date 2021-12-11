username = 'w97y1ayp039ur36m'
password = 'fw9gwxxzkmofzfsa'
server = 'dcrhg4kh56j13bnu.cbetxkdyhwsb.us-east-1.rds.amazonaws.com:3306'
database = 'mfvexsc1zrm922nb'

SELECT_ALL_USERS = """
    SELECT
        User_TUID,
        Username,
        FirstName,
        LastName
    FROM User 
"""
CHECK_USER = SELECT_ALL_USERS + """WHERE Username = :username """
VERIFY_USER = CHECK_USER + """AND Password = :password"""

SELECT_EVENT = """
    SELECT 
        *
    FROM TableTopGame 
"""
SELECT_ALL_EVENTS = """
    SELECT 
        TTG.TableTopGame_TUID
		,EventName
        ,GameName
        ,Username as Organizer
        ,EventDateTime
        ,TotalTakenSlots
        ,TotalOpenSlots
        ,Latitude
        ,Longitude
        ,Categories
    FROM TableTopGame AS TTG
    INNER JOIN (
        SELECT 
            TTG_C.TableTopGame_TUID,
            CONCAT('[',GROUP_CONCAT(DISTINCT TTG_C.Category_TUID SEPARATOR ','),']') AS Categories
        FROM TableTopGame_Category AS TTG_C
        GROUP BY TTG_C.TableTopGame_TUID
    ) AS C
    ON TTG.TableTopGame_TUID = C.TableTopGame_TUID
    INNER JOIN (
        SELECT 
            U_TTG.TableTopGame_TUID,
            COUNT(U_TTG.User_TUID) AS TotalTakenSlots
        FROM Users_TableTopGame AS U_TTG
        GROUP BY U_TTG.TableTopGame_TUID
    ) AS Tot_Slots
    ON TTG.TableTopGame_TUID = Tot_Slots.TableTopGame_TUID
    INNER JOIN User
    ON TTG.Organizer = User.User_TUID
"""

GET_MY_EVENTS = SELECT_ALL_EVENTS +""" WHERE TTG.Organizer =:userID"""
GET_JOINED_EVENTS = """
     INNER JOIN Users_TableTopGame as U_TTG
    ON TTG.TableTopGame_TUID = U_TTG.TableTopGame_TUID
    Where U_TTG.User_TUID = :userID
"""

GET_EVENT = SELECT_ALL_EVENTS + """ WHERE TTG.TableTopGame_TUID = :eventID"""
GET_USER = SELECT_ALL_USERS + """ WHERE User_TUID = :userID"""

INSERT_USER = """
    INSERT INTO User (Username, FirstName, LastName, Password) 
    VALUES(:username,:firstName,:lastName,:password)
"""
DELETE_USER = """
    DELETE FROM User WHERE Username = :username AND Password = :password
"""

DELETE_EVENT = """
    DELETE FROM TableTopGame WHERE TableTopGame_TUID = :eventID AND Organizer = :userID;
"""
LEAVE_EVENT = """
    DELETE FROM Users_TableTopGame WHERE TableTopGame_TUID = :eventID AND User_TUID = :userID;
"""

CREATE_EVENT = """
    INSERT INTO TableTopGame (Organizer, EventName, GameName, EventDateTime, TotalOpenSlots, Latitude, Longitude)
    VALUES(:organizer,:eventName,:gameName,:eventDateTime,:totalOpenSlots,:latitude,:longitude);
    SET @last_id = LAST_INSERT_ID();
    INSERT INTO Users_TableTopGame (User_TUID, TableTopGame_TUID) 
    VALUES(:user,@last_id);
"""
UPDATE_CATEGORY = """
    INSERT INTO TableTopGame_Category (TableTopGame_TUID, Category_TUID) 
    VALUES (@last_id, :categoryID);
"""

ATTEND_EVENT = """
    INSERT INTO Users_TableTopGame (User_TUID, TableTopGame_TUID) 
    VALUES(:user,:event)
"""

CHECK_ATTENDEE = """
    SELECT * FROM Users_TableTopGame WHERE User_TUID=:user AND TableTopGame_TUID=:event
"""