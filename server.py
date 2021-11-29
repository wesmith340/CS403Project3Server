# app.py
from typing import Text
from flask import Flask, json, request, jsonify
from sqlalchemy import create_engine, text
import pandas as pd
from sqlalchemy.sql.expression import bindparam
from pybase64 import b64encode

from Database import DBInfo

app = Flask(__name__)

DBURL = f'mysql://{DBInfo.username}:{DBInfo.password}@{DBInfo.server}/{DBInfo.database}'
engine = create_engine(DBURL)

def verifyUser(username, password):
    user = pd.read_sql(text(DBInfo.VERIFY_USER).bindparams(username=username,password=password), engine)
    if len(user) > 0:
        return user.to_dict('records')[0]
    else:
        return False

def notAttending(userTUID, meetingTUID):
    attendee = pd.read_sql(text(DBInfo.CHECK_ATTENDEE).bindparams(user=userTUID, meeting=meetingTUID), engine)
    if len(attendee) == 0:
        return True
    else:
        return False

def rowsToDict(rows):
    for r in rows:
        newR = {}


@app.route('/newuser', methods=['POST'])
def addUser():
    print(request.json)
    info = request.json
    username = info['Username'].lower()
    fname = info['FirstName']
    lname = info['LastName']
    hashPassword = b64encode(str.encode(info['Password']))
    row = None
    jsonMsg = jsonify({'success':False,'errorMsg':'Unknown error'})
    with engine.begin() as con:
        row = con.execute(text(DBInfo.CHECK_USER).bindparams(username=username)).fetchall()
        
    if (row == None or len(row) == 0):
        with engine.begin() as con:
            con.execute(text(DBInfo.INSERT_USER).bindparams(username=username,firstName=fname,lastName=lname,password=hashPassword))
            jsonMsg = jsonify({'success':True, 'msg':f'{username} has been added to the database'})
    else : 
        jsonMsg = jsonify({
            'success':False,
            'errorMsg':'Username already exists'
            })
    return jsonMsg

@app.route('/deleteuser', methods=['DELETE'])
def deleteUser():
    print(request.json)
    info = request.json
    username = info['username']
    hashPassword = info['password']
    jsonMsg = jsonify({'success':False, 'msg':f'Unable to delete {username}'})


    if (verifyUser(username, hashPassword)):
        with engine.begin() as con:
            con.execute(text(DBInfo.DELETE_USER).bindparams(username=username, password=hashPassword))
            jsonMsg = jsonify({'success':True, 'msg':f'{username} was successfully deleted'})

    return jsonMsg

@app.route('/createmeeting/<username>', methods=['POST'])
def createMeeting(username):
    print(request.json)
    info = request.json
    hashPassword = b64encode(str.encode(info['Password']))
    gameName = info['gamename']
    meetingDateTime = info['datetime']
    totalOpenSlots = info['openslots']
    latitude = info['latitude']
    longitude = info['longitude']

    jsonMsg = jsonify({'success':False, 'msg':f'Unable to create meeting'})

    user = verifyUser(username, hashPassword)
    
    if user != False:
        with engine.begin() as con:
            con.execute(text(DBInfo.CREATE_MEETING).bindparams(
                organizer=user['User_TUID'],gameName=gameName,meetingDateTime=meetingDateTime,
                totalOpenSlots=totalOpenSlots,latitude=latitude,longitude=longitude, user=user['User_TUID']
                ))
            jsonMsg = jsonify({'success':True, 'msg':f'Successfully added meeting'})

    return jsonMsg

@app.route('/joinmeeting/<username>/<meetingID>', methods=['POST'])
def joinMeeting(username, meetingID):
    password = request.json['password']
    jsonMsg = jsonify({'success':False, 'msg':f'Unable to join meeting'})

    user = verifyUser(username, password)

    if user != False and notAttending(user['User_TUID'], meetingID):
        with engine.begin() as con:
            con.execute(text(DBInfo.ATTEND_MEETING).bindparams(user=user['User_TUID'],meeting=meetingID))
            jsonMsg = jsonify({'success':True, 'msg':f'Successfully joined meeting'})

    return jsonMsg



@app.route('/loginuser/<username>', methods=['POST'])
def loginUser(username):
    info = request.json
    hashPassword = b64encode(str.encode(info['Password']))
    row = None
    jsonMsg = jsonify({'success':False, 'errorMsg':'Username and Password do not match'})
    with engine.begin() as con:
        row = con.execute(text(DBInfo.VERIFY_USER).bindparams(username=username,password=hashPassword)).fetchall()
    if len(row) > 0:
        jsonMsg = jsonify({'success':True,'msg':'Username and Password are in the database'})
    return jsonMsg

@app.route('/getallusers', methods=['GET'])
def getallusers():
    data = pd.read_sql(sql=DBInfo.SELECT_USER, con=engine)
    return jsonify(data.to_dict('records'))

@app.route('/getallmeetings', methods=['GET'])
def getallmeetings():
    data = pd.read_sql(sql=DBInfo.SELECT_MEETING, con=engine)
    return jsonify(data.to_dict('records'))

# A welcome message to test our server
@app.route('/')
def index():
    return "Documentation at "

if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)