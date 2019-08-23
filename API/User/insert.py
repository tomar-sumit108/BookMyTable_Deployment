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

#eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJwdWJsaWNfaWQiOjIyLCJleHAiOjE1NjU4NjM5MTF9.FfRsXG_7hCLGL4UJz4Ht8-_SFS3xQm623WNng_7SS3w
@app.route('/api/users',methods=['POST'])
def addUser():
    try:
        data=request.json
        hashed_password=generate_password_hash(data[0]['password'],method='sha256')
        conn=mysql.connect()
        cursor=conn.cursor()
        # username=str(uuid.uuid4())
        
        sql="Insert into User(name,email_id,city,password) VALUES(%s,%s,%s,%s)"
        values=(data[0]['name'],data[0]['email_id'],data[0]['city'],hashed_password) 
        cursor.execute(sql,values)
        conn.commit()
        id=get_last_id(cursor)
        token=jwt.encode({
            'public_id':id,
            'exp':datetime.datetime.utcnow()+datetime.timedelta(minutes=app.config['token_expire_time']),
            'name':data[0]['name'],
            'email':data[0]['email_id'],
            'restaurant':0

            }, app.config['SECRET_KEY'])
        
        resp=jsonify([{"name":data[0]['name'],"city":data[0]['city']}])
        resp.status_code=201
        resp.headers.add('x-token',token.decode("UTF-8"))
        resp.headers.add("access-control-expose-headers",'x-token')
        return resp
    except Exception as e:
        print("ERROR ",e," ERROR")
        resp=jsonify("Duplicate Email")
        resp.status_code=400
        return resp
    finally:
        conn.close()
        cursor.close()

