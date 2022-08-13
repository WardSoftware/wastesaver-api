from flask import Flask, request
import sqlite3

app = Flask(__name__)



@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.get_json()
        cx = sqlite3.connect("database.db")
        cu = cx.cursor()
        dbpwd = cu.execute("select password from users where uname = '" + data['username'].lower() + "'").fetchall()
        cx.close()
        if len(dbpwd) == 0:
            
            return {
                'response': "Username Not Found"
            }
        else:
            if data['password'] == dbpwd[0][0]:
                
                return {
                    'response': "Success"
                }
            else:
                return {
                    'response': "Incorrect Password"
                }
        
    return {
        'response': "False"
    }

@app.route("/signup", methods=['POST'])
def signup():
    data = request.get_json()
    cx = sqlite3.connect("database.db")
    cu = cx.cursor()
    dbpwd = cu.execute("INSERT INTO Users (uname, password) VALUES (?, ?)", [data['username'].lower(), data['password']])
    cx.commit()

    cx.close()
    return {
        'response': 'Success'
    }