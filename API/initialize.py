import pymysql
import json
from app import app
from db_config import mysql
from flask import jsonify
from flask import flash, request
from werkzeug import generate_password_hash, check_password_hash
import random
from decimal import Decimal
from util.lastId import get_last_id

with open('all_data.json') as json_file:
    data = json.load(json_file)
with open('Cities.json') as json_file:
    cities_data=json.load(json_file)

def update_availablity(id,cursor):
    try:
        index1=random.randrange(0,6)
        arr=[1,1,1,1,1,1,1]
        arr[index1]=0
        sql="INSERT INTO Day(restaurant_id,Monday,Tuesday,Wednesday,Thursday,Friday,Saturday,Sunday) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)"
        values=(id,arr[0],arr[1],arr[2],arr[3],arr[4],arr[5],arr[6])
        cursor.execute(sql,values)
    except Exception as e:
        print("Error",e,"Error")


def update_location(tt, loc_id, cursor):
    _city = tt['location']['city']
    _locality = tt['location']['locality']
    _zipcode = tt['location']['zipcode']
    _address = tt['location']['address']
    _verbose = tt['location']['locality_verbose']
    _latitude = Decimal(tt['location']['latitude'])
    _longitude = Decimal(tt['location']['longitude'])
    if _zipcode == "":
        _zipcode = None
    else:
        _zipcode = int(_zipcode)

    sql = "INSERT INTO Location(id,city,zipcode,locality,address,locality_verbose,latitude,longitude) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)"
    value = (loc_id, _city, _zipcode, _locality,
             _address, _verbose, _latitude, _longitude)
    cursor.execute(sql, value)


def update_restaurant(tt, loc_id, cursor):
    _id = tt['id']
    _name = tt['name']
    _average_cost = tt['average_cost_for_two']
    _cuisines = tt['cuisines']
    _timings = tt['timings']
    _establishment = ", ".join(tt['establishment'])
    _highlights = ", ".join(tt['highlights'])
    _rating=Decimal(tt['user_rating']['aggregate_rating'])
    _votes=tt['user_rating']['votes']
    _email="example"+str(loc_id)+"@gmail.com"
    _password=generate_password_hash("asdfjkl",method='sha256')    

    _thumb = tt['thumb']
    _phone_numbers = tt['phone_numbers']
    _capacity=random.randrange(20,50)
    sql = "INSERT INTO Restaurant(id,email,password,location_id,name,average_cost_for_two,cuisines,timings,establishment,highlights,thumb,phone_numbers,capacity,rating,votes) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    value = (_id,_email,_password,loc_id, _name, _average_cost, _cuisines, _timings, _establishment, _highlights,
             _thumb, _phone_numbers,_capacity,_rating,_votes)
    cursor.execute(sql, value)

def update_slots(res_id,cursor):
    sql="INSERT INTO Slot(restaurant_id,start_time,end_time) VALUES(%s,%s,%s)"
    values1=[(res_id,"09:00","15:00"),(res_id,"10:00","16:00"),(res_id,"12:00","16:00")]
    values2=[(res_id,"17:00","23:00"),(res_id,"18:00","23:00"),(res_id,"19:00","23:30")]

    cursor.execute(sql,values1[random.randrange(0,2)])
    cursor.execute(sql,values2[random.randrange(0,2)])

def fill_establishments(tt,establishments):
    for est in tt['establishment']:
        establishments.append(est)
def fill_highlights(tt,highlights):
    for hlt in tt['highlights']:
        highlights.append(hlt)
def fill_cuisines(tt,cuisines):
    ccs=tt['cuisines'].split(", ")
    for cc in ccs:
        cuisines.append(cc)
def fill_common_tables(cursor,cuisines,establishments,highlights):
    for cc in cuisines:
        cursor.execute("INSERT INTO Cuisines(name) values(%s)",cc)
    for est in establishments:
        cursor.execute("INSERT INTO Establishments(name) values(%s)",est)
    for hlt in highlights:
        cursor.execute("INSERT INTO Highlights(name) values(%s)",hlt)

@app.route('/')
def just():
    return "SERVER IS RUNNING"

@app.route('/init')
def get_restaurant():
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Photo")
        cursor.execute("DELETE FROM Review")
        cursor.execute("DELETE FROM Slot")
        cursor.execute("DELETE FROM Booking")
        cursor.execute("DELETE FROM Day")
        cursor.execute("DELETE FROM Restaurant")
        cursor.execute("DELETE FROM Location")
        # cursor.execute("DELETE FROM Cities")
        cursor.execute("DELETE FROM Cuisines")
        cursor.execute("DELETE FROM Establishments")
        cursor.execute("DELETE FROM Highlights")

        conn.commit()
        loc_id = 1
        # for tt in cities_data:
        #     sql="INSERT INTO Cities(id,name,state) VALUES(%s,%s,%s)"
        #     values=(int(tt['id]),tt['name'],tt['state'])
        #     cursor.execute(sql,values)
        #     conn.commit()
        establishments=[]
        cuisines=[]
        highlights=[]
        
        for tt in data:
            tt['establishment']=["Cafe" if x=="Caf\u00e9" else x for x in tt['establishment']]
            estb=fill_establishments(tt,establishments)
            fill_highlights(tt,highlights)
            fill_cuisines(tt,cuisines)
            update_location(tt, loc_id,cursor)
            update_restaurant(tt, loc_id, cursor)
            update_slots(tt['id'],cursor)
            update_availablity(tt['id'],cursor)
            loc_id = loc_id+1
            print("YESS")
        fill_common_tables(cursor,set(cuisines),set(establishments),set(highlights))
        conn.commit()
            

    except Exception as e:
        print(e)
        return "except"
    finally:
        cursor.close()
        conn.close()
        print("DFSDF")
        return "finla"


if __name__ == "__main__":
    app.run(debug=True)
