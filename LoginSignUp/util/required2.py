import pymysql
from app import app
from db_config import mysql
from flask import flash, request,jsonify,make_response
import jwt
from functools import wraps

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return jsonify({'message' : 'Token is missing!'}), 401

        try:
            data=jwt.decode(token,app.config['SECRET_KEY'])
            conn=mysql.connect()
            cursor=conn.cursor(pymysql.cursors.DictCursor)
            cursor.execute("SELECT id,email from Restaurant where id=%s",data['public_id'])
            current_user=cursor.fetchall()[0]
            conn.commit()
        except Exception as e :
            print(e)
            return jsonify({'message':'Token is invalid'}),401
        return f(current_user,*args,**kwargs)
    return decorated
