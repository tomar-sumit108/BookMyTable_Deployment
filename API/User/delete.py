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
from CommentRating.util.delete import delete_review_query
from LoginSignUp.util.required2 import token_required

@app.route('/api/delete',methods=['DELETE'])
@token_required
def delete(current_user):
    conn=mysql.connect()
    cursor=conn.cursor()
    
    cursor.execute("SELECT id FROM Review where user_id=%s",current_user['id'])
    rows=cursor.fetchall()
    for row in rows:
        delete_review_query(row,cursor)
    cursor.execute("DELETE FROM BeenThere where user_id=%s",current_user['id'])
    cursor.execute("DELETE FROM Bookmark where user_id=%s",current_user['id'])
    cursor.execute("DELETE FROM User where id=%s",current_user['id'])
    conn.commit()
    conn.close()
    cursor.close()
    return "Done"
