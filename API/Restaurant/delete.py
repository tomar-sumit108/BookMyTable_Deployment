import pymysql
from app import app
from db_config import mysql
from flask import jsonify
from flask import flash, request
from LoginSignUp.util.required2 import token_required

@app.route('/api/restaurants',methods=['DELETE'])
@token_required
def delete_restaurant(current_user):
    try:
        conn=mysql.connect()
        cursor=conn.cursor()
        id=current_user['id']
        cursor.execute("DELETE FROM Photo where review_id=(SELECT id from Review where Review.restaurant_id=%s)",id)
        cursor.execute("DELETE FROM Review where restaurant_id=%s",id)
        cursor.execute("DELETE FROM Slot where restaurant_id=%s",id)
        cursor.execute("DELETE FROM Booking where restaurant_id=%s",id)
        cursor.execute("DELETE FROM Bookmark where restaurant_id=%s",id)
        cursor.execute("DELETE FROM BeenThere where restaurant_id=%s",id)
        cursor.execute("DELETE FROM Day where restaurant_id=%s",id)
        cursor.execute("DELETE FROM Restaurant where id=%s",id)
        # cursor.execute("DELETE FROM Location where id=(SELECT location_id from Restaurant where id=%s)",id)
        conn.commit()
        resp=jsonify("Sucessful")
        resp.status_code=204
        return resp
    except Exception as e:
        print("Restaurant ",e," Restaurant")
        resp=jsonify("ERROR")
        resp.status_code=500
        return resp
    finally:
        conn.close()
        cursor.close()
