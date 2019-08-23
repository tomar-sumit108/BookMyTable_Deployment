import pymysql
from app import app
from db_config import mysql
from flask import jsonify,request
from util.sendGetResponse import send_get_response
from LoginSignUp.util.required2 import token_required

@app.route('/api/restaurants/bookings')
@token_required
def get_restaurant_bookings(current_user):
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute(
            "SELECT * FROM Booking where restaurant_id=%s",current_user['id'])
        rows = cursor.fetchall()
        return send_get_response(rows,"No Booking Found")
    except Exception as e:
        print(e)
        resp=jsonify("ERROR")
        resp.status_code=500
        return resp
    finally:
        conn.close()
        cursor.close()
