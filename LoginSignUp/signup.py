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

# {
    # "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJwdWJsaWNfaWQiOjMsImV4cCI6MTU2NTM0Mzk3OX0.ELli-A9z9mFW-wz56ZRuQgKF2goG5alotQAAGB6YIVI"
# }


@app.route('/api/signup',methods=['POST'])
def addsUser():
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
            'exp':datetime.datetime.utcnow()+datetime.timedelta(minutes=2)
            }, app.config['SECRET_KEY'])
        
        resp=jsonify([{"name":data[0]['name']}])
        # resp=jsonify("success")
        resp.headers.add('token',token.decode("UTF-8"))
        return resp
    except Exception as e:
        print("ERROR ",e," ERROR")
        return "error"
    finally:
        conn.close()
        cursor.close()

