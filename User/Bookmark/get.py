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

@app.route('/api/bookmarks',methods=['GET'])
@token_required
def get_bookmark(current_user,row=None):
    try:
        if(row != None):
            current_user=row
        conn=mysql.connect()
        cursor=conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT date,time,restaurant_id from Bookmark where user_id=%s",current_user['id'])
        bookmarks=cursor.fetchall()
        for bookmark in bookmarks:
            sql="""SELECT Restaurant.id, Restaurant.name,Restaurant.thumb, Location.address,Location.city
                    FROM Restaurant 
                    JOIN Location ON Restaurant.location_id=Location.id 
                    WHERE Restaurant.id=%s"""
            cursor.execute(sql,(bookmark['restaurant_id']))
            rrs=cursor.fetchall()[0]
            bookmark['restaurant']=rrs
            del bookmark['restaurant_id']
        current_user['bookmarks']=bookmarks
        if row==None:
            return jsonify(current_user['bookmarks'])
        return current_user
    except Exception as e:
        print("ERRrrOR ",e," ERROR")
        resp=jsonify("ERROR")
        resp.status_code=500
        return resp