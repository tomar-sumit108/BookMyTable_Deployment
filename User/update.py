import pymysql
from app import app
from db_config import mysql
from flask import flash, request,jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import uuid
import datetime
from functools import wraps
from util.lastId import get_last_id
from LoginSignUp.util.required import token_required

@app.route('/api/users',methods=['PUT'])
@token_required
def updateUser(current_user):
    try:
        data=request.json
        hashed_password=generate_password_hash(data[0]['password'],method='sha256')
        conn=mysql.connect()
        cursor=conn.cursor()
        
        sql="UPDATE User SET name=%s,email_id=%s,city=%s,password=%s where id=%s"
        values=(data[0]['name'],data[0]['email_id'],data[0]['city'],hashed_password,current_user['id']) 
        cursor.execute(sql,values)
        conn.commit()
        
        resp=jsonify([{"name":data[0]['name'],"city":data[0]['city'],"email":data[0]['email_id']}])
        resp.status_code=201
        return resp
    except Exception as e:
        print("ERROR ",e," ERROR")
        resp=jsonify("Duplicate Email")
        resp.status_code=400
        return resp
    finally:
        conn.close()
        cursor.close()

