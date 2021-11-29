username = 'w97y1ayp039ur36m'
password = 'fw9gwxxzkmofzfsa'
server = 'dcrhg4kh56j13bnu.cbetxkdyhwsb.us-east-1.rds.amazonaws.com:3306'
database = 'mfvexsc1zrm922nb'
SELECT_USER = """
    SELECT 
        *
    FROM User
    WHERE Username = ?
"""
VERIFY_USER = """
    SELECT
        *
    FROM User
    WHERE Username = ?
        AND Password = ?
"""
INSERT_USER = """
    INSERT INTO User (Username, FirstName, LastName, Password)
    Values (?,?,?,?)
"""