import pymysql
from app import app
from db_config import mysql
from flask import jsonify
from flask import flash, request
from LoginSignUp.util.required import token_required

@app.route('/api/users/bookings',methods=['DELETE'])
@token_required
def delete_booking(current_user):
        conn=mysql.connect()
        cursor=conn.cursor(pymysql.cursors.DictCursor)
        id=request.args.get('id',default='%',type=int)
        if(id=='%'):
            return jsonify("BAD REQUEST"),400
        cursor.execute("SELECT user_id from Booking where id=%s",id)
        rows=cursor.fetchall()
        if len(rows)==0 or rows[0]['user_id']!=current_user['id']:
            return jsonify("Unauthorized"),401
        cursor=conn.cursor()
        try:
            cursor.execute("DELETE FROM Booking where id=%s",id)
            conn.commit()
            resp=jsonify("Success")
            resp.status_code=204
            return resp
        except Exception as e:
            print("Booking ",e," Booking")
            return jsonify("ERROR"),500
          
        finally:
            conn.close()
            cursor.close()
