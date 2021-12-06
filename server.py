# app.py
from flask import Flask, json, request, jsonify
from sqlalchemy import create_engine, text
import pandas as pd
from pybase64 import b64encode

from Database import DBInfo

app = Flask(__name__)

DBURL = f'mysql://{DBInfo.username}:{DBInfo.password}@{DBInfo.server}/{DBInfo.database}'
engine = create_engine(DBURL)

# Function for checking if a username and password match in the database
def verifyUser(username, password):
    print(username, password)
    user = pd.read_sql(text(DBInfo.VERIFY_USER).bindparams(username=username,password=password), engine)
    if len(user) > 0:
        return user.to_dict('records')[0]
    else:
        return False

# Function returns true if user is not attending event
def notAttending(userTUID, eventTUID):
    attendee = pd.read_sql(text(DBInfo.CHECK_ATTENDEE).bindparams(user=userTUID, event=eventTUID), engine)
    if len(attendee) == 0:
        return True
    else:
        return False

# Route for creating a new user
@app.route('/newuser', methods=['POST'])
def addUser():
    print(request.json)
    info = request.json
    username = info['Username'].lower()
    fname = info['FirstName']
    lname = info['LastName']
    hashPassword = b64encode(str.encode(info['Password']))
    row = None
    jsonMsg = jsonify({'Success':False,'Msg':'Unknown error'})
    with engine.begin() as con:
        row = con.execute(text(DBInfo.CHECK_USER).bindparams(username=username)).fetchall()
        
    if (row == None or len(row) == 0):
        with engine.begin() as con:
            con.execute(text(DBInfo.INSERT_USER).bindparams(username=username,firstName=fname,lastName=lname,password=hashPassword))
            jsonMsg = jsonify({'Success':True, 'Msg':f'{username} has been added to the database'})
    else : 
        jsonMsg = jsonify({
            'Success':False,
            'Msg':'Username already exists'
            })
    return jsonMsg

@app.route('/deleteuser/<username>', methods=['DELETE'])
def deleteUser(username):
    print(request.json)
    info = request.json
    hashPassword = info['Password']
    jsonMsg = jsonify({'Success':False, 'Msg':f'Unable to delete {username}'})

    if (verifyUser(username, hashPassword)):
        with engine.begin() as con:
            con.execute(text(DBInfo.DELETE_USER).bindparams(username=username, password=hashPassword))
            jsonMsg = jsonify({'Success':True, 'Msg':f'{username} was successfully deleted'})

    return jsonMsg

@app.route('/createevent/<username>', methods=['POST'])
def createEvent(username):
    print(request.json)
    info = request.json
    hashPassword = b64encode(str.encode(info['Password']))
    eventName = info['EventName']
    gameName = info['GameName']
    eventDateTime = info['DateTime']
    totalOpenSlots = info['OpenSlots']
    latitude = info['Latitude']
    longitude = info['Longitude']
    categories = info['Categories']

    jsonMsg = jsonify({'Success':False, 'Msg':f'Unable to create event'})

    user = verifyUser(username, hashPassword)
    
    if user != False:
        for x in categories:
            print(x, " : ",str(text(DBInfo.UPDATE_CATEGORY).bindparams(categoryID=x)))
        with engine.begin() as con:
            con.execute(
                text(DBInfo.CREATE_EVENT).bindparams(
                    organizer=user['User_TUID'],eventName=eventName,gameName=gameName,eventDateTime=eventDateTime,
                    totalOpenSlots=totalOpenSlots,latitude=latitude,longitude=longitude, user=user['User_TUID']
                ))
            for x in categories:
                con.execute(text(DBInfo.UPDATE_CATEGORY).bindparams(categoryID=x))
            jsonMsg = jsonify({'Success':True, 'Msg':f'Successfully added event'})

    return jsonMsg

@app.route('/joinevent/<username>/<eventID>', methods=['POST'])
def joinEvent(username, eventID):
    hashPassword = b64encode(str.encode(request.json['Password']))
    jsonMsg = jsonify({'Success':False, 'Msg':f'Unable to join event'})

    user = verifyUser(username, hashPassword)
    print(user)
    if user != False and notAttending(user['User_TUID'], eventID):
        with engine.begin() as con:
            con.execute(text(DBInfo.ATTEND_EVENT).bindparams(user=user['User_TUID'],event=eventID))
            jsonMsg = jsonify({'Success':True, 'Msg':f'Successfully joined event'})

    return jsonMsg


@app.route('/loginuser/<username>', methods=['POST'])
def loginUser(username):
    info = request.json
    hashPassword = b64encode(str.encode(info['Password']))
    row = None
    jsonMsg = jsonify({'Success':False, 'Msg':'Username and Password do not match'})
    with engine.begin() as con:
        row = con.execute(text(DBInfo.VERIFY_USER).bindparams(username=username,password=hashPassword)).fetchall()
    if len(row) > 0:
        jsonMsg = jsonify({'Success':True,'Msg':'Username and Password are in the database'})
    return jsonMsg

@app.route('/getallusers', methods=['GET'])
def getallusers():
    data = pd.read_sql(sql=DBInfo.SELECT_ALL_USERS, con=engine)
    print(data.to_dict('records'))
    return jsonify(data.to_dict('records'))

@app.route('/getallevents', methods=['GET'])
def getallevents():
    data = pd.read_sql(sql=DBInfo.SELECT_EVENT, con=engine)
    return jsonify(data.to_dict('records'))

@app.route('/getallcategories', methods=['GET'])
def getallcategories():
    data = pd.read_sql(sql=DBInfo.SELECT_CATEGORIES, con=engine)
    return jsonify(data.to_dict('records'))

# Just a small change

# A welcome message to test our server
@app.route('/')
def index():
    return """
    <h1>VERSION 2</h1>
    <h2>Documentation at <a href="https://github.com/wesmith340/CS403Project3Server/blob/main/info.txt">Github Repo</a></h2>
    """

if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000, debug=True)