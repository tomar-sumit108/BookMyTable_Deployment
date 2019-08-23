import pymysql
from app import app
from db_config import mysql
from flask import jsonify,flash,request
from Restaurant.util.convertRestaurant import convert_restaurant
from util.sendGetResponse import send_get_response
from LoginSignUp.util.required2 import token_required


    # eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJwdWJsaWNfaWQiOjIyLCJleHAiOjE1NjU4NjAzNzJ9.cIP4Vp4sE9d6C1BIn1tfCjcSkXVwysculT6tZr0BUF4

@app.route('/api/restaurants')
def get_restaurants():
    try:
        _city=request.args.get('city',default='%',type=str)
        _restaurant_id=request.args.get('restaurantId',default="%",type=int)
        _meta=request.args.get('meta',default="NO",type=str)
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute(
            "SELECT * FROM Restaurant where (SELECT city from Location WHERE Location.id=Restaurant.location_id) LIKE %s AND id LIKE %s ",(_city,_restaurant_id))
        rows = cursor.fetchall()
        if _restaurant_id=="%" :
            rows=convert_restaurant(cursor, rows,meta=_meta)
        else:
            rows=convert_restaurant(cursor,rows,reviews=True)
        print(type(rows))

        
        return send_get_response(rows,"No Restaurant Found")
    except Exception as e:
        print(e)
        resp=jsonify("ERROR")
        resp.status_code=500
        return resp
    finally:
        cursor.close()
        conn.close()