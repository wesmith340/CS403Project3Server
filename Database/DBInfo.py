username = 'w97y1ayp039ur36m'
password = 'fw9gwxxzkmofzfsa'
server = 'dcrhg4kh56j13bnu.cbetxkdyhwsb.us-east-1.rds.amazonaws.com:3306'
database = 'mfvexsc1zrm922nb'
SELECT_USER = """
    SELECT 
        User_TUID,
        Username,
        FirstName,
        LastName
    FROM User 
"""
INSERT_USER = """
    INSERT INTO User (Username, FirstName, LastName, Password) 
"""
DELETE_USER = """
    DELETE FROM User 
"""
CREATE_MEETING = """
    INSERT INTO TableTopGame (Organizer, GameName, MeetingDateTime, TotalOpenSlots, Latitude, Longitude) 
"""

ATTEND_MEETING = """
    INSERT INTO Users_TableTopGame (User_TUID, TableTopGame_TUID) 
"""

CHECK_ATTENDEE = """
    SELECT * FROM Users_TableTopGame
"""