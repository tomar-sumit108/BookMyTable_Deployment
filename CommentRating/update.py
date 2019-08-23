import pymysql
from app import app
from db_config import mysql
from flask import jsonify
from flask import flash, request
from util.lastId import get_last_id
from LoginSignUp.util.required import token_required

@app.route('/api/reviews',methods=['PUT'])
@token_required
def update_review(current_user):
    id=request.args.get('id',default='%',type=int)
    if(id=='%'):
        return jsonify("BAD REQUEST"),400
    try:
        data=request.json[0]
        _comment=data['comment']
        _rating=data['rating']
        _rating_text=data['rating_text']
        _user_id=current_user['id']
        _date=data['date']
        _time=data['time']

        conn=mysql.connect()
        cursor=conn.cursor()
        cursor.execute("SELECT user_id from Review where id=%s",id)
        try:
            u_id=cursor.fetchall()[0][0]
            if(u_id!=_user_id):
                raise Exception
        except:
            return jsonify("Unauthorized"),401

        cursor.execute("SELECT restaurant_id,rating from Review where id=%s",id)
        (_res_id,rating1)=cursor.fetchall()[0]
        cursor.execute("SELECT rating,votes FROM Restaurant where id=%s",_res_id)
        (rating,votes)=cursor.fetchall()[0]
        cursor.execute("UPDATE Restaurant SET rating=%s where id=%s",
                    ((rating*(votes)-rating1+_rating)/(votes),_res_id))

        sql="UPDATE Review SET comment=%s,rating=%s,rating_text=%s,date=%s,time=%s WHERE id=%s"
        values=(_comment,_rating,_rating_text,_date,_time,id)
        cursor.execute(sql,values)
        cursor.execute("DELETE FROM Photo where review_id=%s",id)
        for url in data['photos']:
            sql="INSERT INTO Photo(review_id,url) values(%s,%s)"
            values=(id,url)
            cursor.execute(sql,values)
            print("sssssssss")
        conn.commit()
        return jsonify("Comment Updation Successfull")
    except Exception as e:
        print("commmment ",e," comment")
        return jsonify("Error"),500
    finally:
        conn.close()
        cursor.close()



