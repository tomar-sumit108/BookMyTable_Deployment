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

@app.route('/api/beentheres',methods=['GET'])
@token_required
def get_beenthere(current_user,row=None):
    try:
        if(row != None):
            current_user=row
        conn=mysql.connect()
        cursor=conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT date,time,restaurant_id from BeenThere where user_id=%s",current_user['id'])
        beentheres=cursor.fetchall()
        for beenthere in beentheres:
            sql="""SELECT Restaurant.id, Restaurant.name,Restaurant.thumb, Location.address,Location.city
                    FROM Restaurant 
                    JOIN Location ON Restaurant.location_id=Location.id 
                    WHERE Restaurant.id=%s"""
            cursor.execute(sql,(beenthere['restaurant_id']))
            rrs=cursor.fetchall()[0]
            beenthere['restaurant']=rrs
            del beenthere['restaurant_id']
        current_user['beentheres']=beentheres
        if row==None:
            return jsonify(current_user['beenthere'])
        return current_user
    except Exception as e:
        print("ERRrrOR ",e," ERROR")
        resp=jsonify("ERROR")
        resp.status_code=500
        return resp