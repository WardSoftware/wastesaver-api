from flask import Flask, request
import sqlite3
from flask_bcrypt import Bcrypt

app = Flask(__name__)
bcrypt = Bcrypt(app)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.get_json()
        cx = sqlite3.connect("database.db")
        cu = cx.cursor()
        pwdhash = bcrypt.generate_password_hash(data['password'])
        print(bcrypt.check_password_hash(pwdhash, 'password'))
        dbpwd = cu.execute("select password from users where uname = '" + data['username'].lower() + "'").fetchall()
        cx.close()
        if len(dbpwd) == 0:
            
            return {
                'response': "Username Not Found"
            }
        else:

            if (bcrypt.check_password_hash(dbpwd[0][0], data['password'])):
                
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
    password = bcrypt.generate_password_hash(data['password'])
    dbpwd = cu.execute("INSERT INTO Users (uname, password) VALUES (?, ?)", [data['username'].lower(), password])
    cx.commit()

    cx.close()
    return {
        'response': 'Success'
    }