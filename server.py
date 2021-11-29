# app.py
from flask import Flask, json, request, jsonify
import pyodbc
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from Database import DBInfo

app = Flask(__name__)

cnxn = pyodbc.connect('DRIVER={MySql};SERVER='+DBInfo.server+';DATABASE='+DBInfo.database+';UID='+DBInfo.username+';PWD='+ DBInfo.password)
print(cnxn.getinfo(pyodbc.SQL_MAX_CONCURRENT_ACTIVITIES))
# cursor = cnxn.cursor()
# DBURL = f'mysql://{DBInfo.username}:{DBInfo.password}@{DBInfo.server}/{DBInfo.database}'
# engine = create_engine(DBURL)
# Session = sessionmaker(engine)

@app.route('/newuser', methods=['POST'])
def addUser():
    username = request.form.get('username')
    fname = request.form.get('fname')
    lname = request.form.get('lname')
    hashPassword = request.form.get('hashPassword')
    row = None
    success = False
    jsonMsg = jsonify({'success':success,'errorMsg':'Unknown error'})
    with cnxn:
        cursor = cnxn.cursor()

        cursor.execute(DBInfo.SELECT_USER, username)
        row = cursor.fetchall()
        cursor.close()
        
    if (row == None or len(row) == 0):
        with cnxn:
            cursor = cnxn.cursor()
            cursor.execute(DBInfo.INSERT_USER, username, fname, lname, hashPassword)
            success = True
            jsonMsg = jsonify({'success':success})
    else :
        error = 'Username already exists'
        jsonMsg = jsonify({
            'success':success,
            'errorMsg':error
            })
    return jsonMsg

@app.route('/loginuser/<username>', methods=['POST'])
def loginUser(username):
    hashPassword = request.form.get('hashPassword')
    row = None
    jsonMsg = jsonify({'success':False, 'errorMsg':'Username and Password do not match'})
    with cnxn:
        cursor = cnxn.cursor()
        cursor.execute(DBInfo.VERIFY_USER, username, hashPassword)
        row = cursor.fetchall()
    if len(row) > 0:
        jsonMsg = jsonify({'success':True,'msg':'Username and Password are in the database'})
    return jsonMsg



# A welcome message to test our server
@app.route('/')
def index():
    return "<h1>Server version 1.2</h1>"

if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)