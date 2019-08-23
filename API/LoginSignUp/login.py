import pymysql
from app import app
from db_config import mysql
from flask import flash, request,jsonify,make_response
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import uuid
import datetime
from functools import wraps
from util.lastId import get_last_id
from LoginSignUp.util.required import token_required

@app.route('/api/login',methods=['POST'])
def login():
    try:
        data=request.json[0]
        if not data or not "email" in data or not "password" in data:
            return make_response('Bad Request', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})

        conn=mysql.connect()
        cursor=conn.cursor(pymysql.cursors.DictCursor)
        if int(data['restaurant'])==0:
            cursor.execute("SELECT * FROM User WHERE email_id=%s",data['email'])
        else:
            cursor.execute("SELECT * FROM Restaurant WHERE email=%s",data['email'])
        conn.commit()
        
        Users=cursor.fetchall()
        if not Users:
            return make_response('Check Email', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})
        email=""
        if int(data['restaurant'])==0:
            email=Users[0]['email_id']
        else:
            email=Users[0]['email']
        
        User=Users[0]
        conn.close()
        cursor.close()
        

        if check_password_hash(User['password'],data['password']):
            token = jwt.encode({'public_id' : User['id'], 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=app.config['token_expire_time']),'name':User['name'],'email':email,'restaurant':data['restaurant']}, app.config['SECRET_KEY'])
            resp=jsonify("Successful")
            resp.headers.add("x-token",token.decode('UTF-8'))
            resp.headers.add("access-control-expose-headers","x-token")
            resp.status_code=201
            return resp

        return make_response('Check Password', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})
    except Exception as e:
        print (e)
        return jsonify("BAD request"),400







