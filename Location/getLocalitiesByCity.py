import pymysql
from app import app
from db_config import mysql
from flask import jsonify
from flask import flash, request
from util.sendGetResponse import send_get_response

@app.route('/api/localities')
def get_localities():
    city=request.args.get('city')
    if city==None:
        resp=jsonify("City Required")
        resp.status_code=400
        return resp
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        # cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT locality FROM Location WHERE city=%s",city)
        rows = cursor.fetchall()
        return send_get_response(rows,"No city found")
    except Exception as e:
        print(e)
        resp=jsonify("ERROR")
        resp.status_code=500
        return resp
    finally:
        cursor.close()
        conn.close()