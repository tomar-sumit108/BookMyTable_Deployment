import pymysql
from app import app
from db_config import mysql
from flask import jsonify
from flask import flash, request
from util.sendGetResponse import send_get_response

def append_photos(cursor,review):
    cursor.execute("SELECT * from Photo where review_id=%s",review['id'])
    review['photos']=[]
    for photo in cursor.fetchall():
        review['photos'].append(photo['url'])
    

def append_restaurant_details(cursor,review):
    sql="""SELECT Restaurant.id,Restaurant.name,Restaurant.thumb,Location.locality,Location.city 
                    from Restaurant JOIN Location 
                    ON  Restaurant.location_id=Location.id where Restaurant.id=%s"""
    cursor.execute(sql,review['restaurant_id'])
    review['restaurant']=cursor.fetchall()[0]
    del review['restaurant_id']

def append_user_details(cursor,review):
    cursor.execute("SELECT id,name,city from User where id=%s",review['user_id'])
    review['user']=cursor.fetchall()[0]
    del review['user_id']


@app.route('/api/reviews')
def get_reviews(resId=None,userId=None):
    _restaurant_id=request.args.get('restaurantId',default="%",type=int)
    _user_id=request.args.get('userId',default="%",type=int)
    if resId != None:
        _restaurant_id=resId
    if userId!=None:
        _user_id=userId
    try:
        conn=mysql.connect()
        cursor=conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * from Review where restaurant_id LIKE %s AND user_id LIKE %s",(_restaurant_id,_user_id))

        reviews=cursor.fetchall()
        print(reviews)
        for review in reviews:
            append_photos(cursor,review)
            append_restaurant_details(cursor,review)
            append_user_details(cursor,review)
        return send_get_response(reviews,"No Review Found ")
  
    except Exception as e:
        print(e)
        resp=jsonify("ERROR")
        resp.status_code=500
        return resp
    finally:
        conn.close()
        cursor.close()
    

