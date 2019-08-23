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
#eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJwdWJsaWNfaWQiOjIyLCJleHAiOjE1NjU4NjM5MTF9.FfRsXG_7hCLGL4UJz4Ht8-_SFS3xQm623WNng_7SS3w
@app.route('/api/beentheres',methods=['POST'])
@token_required
def addBeenThere(current_user):
    try:
        conn=mysql.connect()
        cursor=conn.cursor()
        data=request.json[0]
        date=data['date']
        time=data['time']
        res_id=data['restaurant_id']
        usr_id=current_user['id']
        sql="Insert into BeenThere(user_id,restaurant_id,date,time) VALUES(%s,%s,%s,%s)"
        values=(usr_id,res_id,date,time) 
        cursor.execute(sql,values)
        id=get_last_id(cursor)
        conn.commit()
        resp=jsonify({"id":id,"restaurant_id":res_id,"date":date,"time":time})
        resp.status_code=201
        return resp
    except Exception as e:
        print("ERROR ",e," ERROR")
        resp=jsonify("ERROR")
        resp.status_code=400
        return resp
    finally:
        conn.close()
        cursor.close()

