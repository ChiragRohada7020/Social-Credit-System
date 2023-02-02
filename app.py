from flask import Flask
from flask import render_template
from flask import url_for
from flask import request
from flask import abort, redirect, url_for,session
import pymongo
import json
from flask_mysqldb import MySQL

app = Flask(__name__)
 
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'social_credit_system'



 




mysql = MySQL(app)
#Creating a connection cursor


if __name__ == '__main__':
    app.run(host='0.0.0.0')





@app.route("/")
def index():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM social_credit_score")
    data = cur.fetchall()
    print(data)
    return render_template("index.html",data=data)



@app.route("/data/<username>")
def data(username):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM social_credit_score WHERE Individual_ID = % s', (username, ))
    data = cur.fetchall()
    his=data[0][2]
    
 
    

    cur.execute('SELECT * FROM criminal_records WHERE Individual_ID = % s', (username, ))
    criminal_records = cur.fetchall()
    cur.execute('SELECT * FROM behaviour_records WHERE Individual_ID = % s', (username, ))
    behaviour_records= cur.fetchall()
    cur.execute('SELECT * FROM credit_score WHERE Individual_ID = % s', (username, ))
    credit_score= cur.fetchall()
    cur.execute('SELECT * FROM family_details WHERE Individual_ID = % s', (username, ))
    family_details= cur.fetchall()
    family_length=len(family_details)
    if credit_score[0][3]==0:
        ratio='NIL'
    else:
        ratio=(credit_score[0][4]-credit_score[0][3])/credit_score[0][3]
    
    credit_score_length=len(credit_score)
    length=len(criminal_records)

    
    

   
    

    return render_template("chi.html",data=data,criminal_records=criminal_records,length=length,behaviour_records=behaviour_records,credit_score=credit_score,ratio=ratio,family_details=family_details,family_length=family_length)

