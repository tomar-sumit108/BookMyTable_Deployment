import pymysql
from app import app
from db_config import mysql
from flask import jsonify
from Restaurant.util.convertRestaurant import convert_restaurant
from util.sendGetResponse import send_get_response

@app.route('/api/restaurants/<id>')
def get_restaurants_by_id(id):
    
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        sql = "SELECT * from Restaurant WHERE id=%s"
        cursor.execute(sql, (id))
        rows = cursor.fetchall()
        convert_restaurant(cursor, rows,reviews=True)
        return send_get_response(rows,"No Restaurant found for given criteria")
    except Exception as e:
        print(e)
        resp=jsonify("Error")
        resp.status_code=500
        return resp
    finally:
        cursor.close()
        conn.close()