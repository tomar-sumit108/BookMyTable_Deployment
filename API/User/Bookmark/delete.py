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
@app.route('/api/bookmarks',methods=['DELETE'])
@token_required
def DeleteBookmark(current_user):
    id=request.args.get('id',default='%',type=int)
    if(id=='%'):
        return jsonify("BAD REQUEST"),400
    try:
        conn=mysql.connect()
        cursor=conn.cursor()
        cursor.execute("SELECT user_id from Bookmark where id=%s",id)
        u_id=cursor.fetchall()[0]
        if(u_id!=_user_id):
            return jsonify("Unauthorized"),401
        cursor.execute("DELETE FROM Bookmark WHERE id=%s",id)
        conn.commit()
        resp=jsonify("")
        resp.status_code=204
        return resp
    except Exception as e:
        print("ERROR ",e," ERROR")
        resp=jsonify("ERROR")
        resp.status_code=400
        return resp
    finally:
        conn.close()
        cursor.close()

