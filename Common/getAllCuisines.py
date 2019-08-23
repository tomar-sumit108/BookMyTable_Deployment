import pymysql
from app import app
from db_config import mysql
from flask import jsonify
from util.sendGetResponse import send_get_response

@app.route('/api/cuisines')
def get_cuisines():
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute(
            "SELECT name FROM Cuisines")
        rows = cursor.fetchall()
        ans=[]
        for row in rows:
            ans.append(row['name'])
        return send_get_response(ans,"No Booking Found")
    except Exception as e:
        print(e)
        resp=jsonify("ERROR")
        resp.status_code=500
        return resp
    finally:
        cursor.close()
        conn.close()
