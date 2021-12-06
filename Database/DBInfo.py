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
        EventName
        ,GameName
        ,GameCategory
        ,EventDateTime
        ,TotalOpenSlots
        ,Latitude
        ,Longitude
        ,Categories
    FROM TableTopGame AS TTG
    INNER JOIN (
        SELECT 
            TTG_C.TableTopGame_TUID,
            GROUP_CONCAT(DISTINCT TTG_C.Category_TUID SEPARATOR ',') AS Categories
        FROM TableTopGame_Category AS TTG_C
        GROUP BY TTG_C.TableTopGame_TUID
    ) AS C
    ON TTG.TableTopGame_TUID = C.TableTopGame_TUID
"""
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