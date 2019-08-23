import pymysql
from app import app
from db_config import mysql
from flask import jsonify
from flask import flash, request
from util.lastId import get_last_id
from LoginSignUp.util.required import token_required

@app.route('/api/reviews',methods=['POST'])
@token_required
def insert_review(current_user):
    try:
        data=request.json[0]
        _comment=data['comment']
        _rating=float("0"+str(data['rating']))
        _rating_text=data['rating_text']
        _res_id=data['restaurant_id']
        _user_id=current_user['id']
        _date=data['date']
        _time=data['time']

        conn=mysql.connect()
        cursor=conn.cursor()
        cursor.execute("SELECT rating,votes FROM Restaurant where id=%s",_res_id)
        
        (rating,votes)=cursor.fetchall()[0]
        
        cursor.execute("UPDATE Restaurant SET rating=%s,votes=%s where id=%s",
                    ((rating*votes+_rating)/(votes+1),votes+1,_res_id))
        print("working")
        sql="INSERT INTO Review(restaurant_id,user_id,comment,rating,rating_text,date,time) values(%s,%s,%s,%s,%s,%s,%s)"
        values=(_res_id,_user_id,_comment,_rating,_rating_text,_date,_time)
        cursor.execute(sql,values)
        review_id=get_last_id(cursor)
        for url in data['photos']:
            sql="INSERT INTO Photo(review_id,url) values(%s,%s)"
            values=(review_id,url)
            cursor.execute(sql,values)
        conn.commit()
        print("sucess")
        resp=jsonify("Comment Insertion Successfull")
        resp.status_code=201
        return resp
    except Exception as e:
        print("review ",e," review")
        resp=jsonify("Error")
        resp.status_code=500
        return resp
    finally:
        conn.close()
        cursor.close()



