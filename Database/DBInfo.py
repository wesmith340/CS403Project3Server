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


SELECT_MEETING = """
    SELECT 
        *
    FROM TableTopGame 
"""
INSERT_USER = """
    INSERT INTO User (Username, FirstName, LastName, Password) 
    VALUES(:username,:firstName,:lastName,:password)
"""
DELETE_USER = """
    DELETE FROM User WHERE Username = :username AND Password = :password
"""

CREATE_MEETING = """
    INSERT INTO TableTopGame (Organizer, GameName, MeetingDateTime, TotalOpenSlots, Latitude, Longitude)
    VALUES(:organizer,:gameName,:meetingDateTime,:totalOpenSlots,:latitude,:longitude);
    SET @last_id = LAST_INSERT_ID();
    INSERT INTO Users_TableTopGame (User_TUID, TableTopGame_TUID) 
    VALUES(:user,@last_id);
"""

ATTEND_MEETING = """
    INSERT INTO Users_TableTopGame (User_TUID, TableTopGame_TUID) 
    VALUES(:user,:meeting)
"""

CHECK_ATTENDEE = """
    SELECT * FROM Users_TableTopGame WHERE User_TUID=:user AND TableTopGame_TUID=:meeting
"""