import pymysql
from app import app
from db_config import mysql
from flask import jsonify
from flask import flash, request

@app.route('/api/bookings',methods=['DELETE'])
def delete_all_booking():
    try:
        conn=mysql.connect()
        cursor=conn.cursor()
        cursor.execute("DELETE FROM Booking")
        conn.commit()
        return "done"
    except Exception as e:
        print("Booking ",e," Booking")
    finally:
        conn.close()
        cursor.close()
