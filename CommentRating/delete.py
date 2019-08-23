import pymysql
from app import app
from db_config import mysql
from flask import jsonify
from flask import flash, request
from util.lastId import get_last_id
from LoginSignUp.util.required import token_required
from CommentRating.util.delete import delete_review_query

@app.route('/api/reviews',methods=['DELETE'])
@token_required
def delete_review(current_user):
    id=request.args.get('id',default='%',type=int)
    if(id=='%'):
        return jsonify("BAD REQUEST"),400
    try:
        conn=mysql.connect()
        cursor=conn.cursor()
        cursor.execute("SELECT user_id from Review where id=%s",id)
        try:
            u_id=cursor.fetchall()[0][0]
            if(u_id!=_user_id):
                raise Exception
        except:
            return jsonify("Unauthorized"),401

        delete_review_query(id,cursor)
        conn.commit()
        resp=jsonify("Success")
        resp.status_code=204
        return resp
    except Exception as e:
        print("comment ",e," comment")
        return jsonify("ERROR"),500
    finally:
        conn.close()
        cursor.close()



