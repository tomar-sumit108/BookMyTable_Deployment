import pymysql
from app import app
from db_config import mysql
from werkzeug.security import generate_password_hash, check_password_hash
from flask import jsonify
import jwt
import datetime
from functools import wraps
from flask import flash, request
from util.lastId import get_last_id
from util.sendGetResponse import send_get_response
from Restaurant.util.convertRestaurant import convert_restaurant
from LoginSignUp.util.required2 import token_required

def insert_days(cursor,data,res_id):
        sql="INSERT INTO Day(restaurant_id,Monday,Tuesday,Wednesday,Thursday,Friday,Saturday,Sunday) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)"
        values=(res_id,data['Monday'],data['Tuesday'],data['Wednesday'],data['Thursday'],data['Friday'],data['Saturday'],data['Sunday'])
        cursor.execute(sql,values)

def insert_location(cursor,data):
    # try:
        _address=data['address']['line_1']+" "+data['address']['line_2']+", "+data['locality_verbose']+", "+data['city']
        _city=data['city']
        _zipcode=None
        if data['zipcode'].isdigit():
            _zipcode=int(data['zipcode'])
        _locality=data['locality']
        _loc_verb=data['locality_verbose']
        cursor.execute("SELECT * from Cities where name=%s",_city)
        if cursor.rowcount==0:
            cursor.execute("INSERT into Cities(name) values(%s)",_city)
        
        sql="INSERT INTO Location(city,zipcode,locality,address,locality_verbose) values(%s,%s,%s,%s,%s)"
        values=(_city,_zipcode,_locality,_address,_loc_verb)
        cursor.execute(sql,values)
    # except Exception as e:
        # print("lo "+e+" lo")

def insert_highlights(data,cursor):
    # try:
        cursor.execute("SELECT name FROM Highlights")
        l1=cursor.fetchall()
        l1=[i for sub in l1 for i in sub]
        new_list=list(set(data)-set(l1))
        for dd in new_list:
            cursor.execute("INSERT INTO Highlights(name) values(%s)",dd)

        return ", ".join(data)
    # except Exception as e:
        # print("high "+e+" high")

def insert_establishments(data,cursor):
    # try:
        cursor.execute("SELECT name FROM Establishments")
        l1=cursor.fetchall()
        l1=[i for sub in l1 for i in sub]
        new_list=list(set(data)-set(l1))
        for dd in new_list:
            cursor.execute("INSERT INTO Establishments(name) values(%s)",dd)

        return ", ".join(data)
    # except Exception as e:
        # print("est "+e+" est")

def insert_cuisines(data,cursor):
    cursor.execute("SELECT name FROM Cuisines")
    l1=cursor.fetchall()
    l1=[i for sub in l1 for i in sub]
    new_list=list(set(data)-set(l1))
    for dd in new_list:
        cursor.execute("INSERT INTO Cuisines(name) values(%s)",dd)

    return ", ".join(data)

    

def insert_restaurant(cursor,data,_loc_id):
    # try:
        _ave_cost=int("0"+str(data['average_cost_for_two']))
        _cuisines=insert_cuisines(data['cuisines'],cursor)
        _establishment=insert_establishments(data['establishment'],cursor)
        _highlights=insert_highlights(data['highlights'],cursor)

        _name=data['name']
        _phone=data['phone']['std']+"-"+data['phone']['number']
        _thumb=data['thumb']
        _opening_status=int("0"+str(data['opening_status']))
        _email=data['email']
        _website=data['website']
        _capacity=int("0"+str(data['capacity']))
        hashed_password=generate_password_hash(data['password'],method='sha256')
        sql="""INSERT INTO 
            Restaurant(location_id,name,email,average_cost_for_two,cuisines,establishment,highlights,thumb,phone_numbers,capacity,opening_status,website,password)
            VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
        values=(_loc_id,_name,_email,_ave_cost,_cuisines,_establishment,_highlights,_thumb,_phone,_capacity,_opening_status,_website,hashed_password)
        cursor.execute(sql,values)
    # except Exception as e:
        # print("res "+e+" res")

def insert_slot(cursor,data,res_id):
    print(data)
    try:
        for slot in data:
            sql="INSERT INTO Slot(restaurant_id,start_time,end_time) VALUES(%s,%s,%s)"
            values=(res_id,slot['start_time'],slot['end_time'])
            cursor.execute(sql,values)   

    except Exception as e:
        print("slot "+e+" slot")

@app.route('/api/restaurants',methods=['POST'])
# @token_required
def add_restaurant():
    try:
        data=request.json 
        conn=mysql.connect()
        cursor=conn.cursor()
        cursor2=conn.cursor(pymysql.cursors.DictCursor)
        insert_location(cursor,data[0]['location'])
        loc_id=get_last_id(cursor)

        try:
            insert_restaurant(cursor,data[0],loc_id)  
        except Exception as e:
            return jsonify("Duplicate email"),400
        res_id=get_last_id(cursor)
        
        insert_days(cursor,data[0]['days'],res_id)
        
        insert_slot(cursor,data[0]['slots'],res_id)
        print("sss")
        conn.commit()
        cursor2.execute("SELECT * FROM Restaurant where id=%s",res_id)
        rows=cursor2.fetchall()
        convert_restaurant(cursor2, rows)
        token=jwt.encode({
            'public_id':res_id,
            'exp':datetime.datetime.utcnow()+datetime.timedelta(minutes=app.config['token_expire_time']),
            'name':data[0]['name'],
            'email':data[0]['email'],
            'restaurant':1
            }, app.config['SECRET_KEY'])
        resp=jsonify(rows)
        resp.status_code=201
        resp.headers.add('x-token',token.decode("UTF-8"))
        resp.headers.add("access-control-expose-headers",'x-token')
        return resp


    except Exception as e:
        print(e)
        resp=jsonify("ERROR")
        resp.status_code=500
        return resp
    finally:
        conn.close()
        cursor.close()
        cursor2.close()
        
