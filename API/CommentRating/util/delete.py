import pymysql
from app import app
from db_config import mysql
from flask import jsonify
from flask import flash, request
from util.lastId import get_last_id

def delete_review_query(id,cursor):
        cursor.execute("SELECT restaurant_id,rating from Review where id=%s",id)
        (res_id,rating)=cursor.fetchall()[0]
        cursor.execute("SELECT rating,votes from Restaurant where id=%s",res_id)
        (rating2,votes)=cursor.fetchall()[0]
        print("res ",votes)
        new_rating=rating2*votes-rating
        votes=votes-1
        if votes>0:
            new_rating=new_rating/(votes)
        cursor.execute("UPDATE Restaurant SET rating=%s,votes=%s",(new_rating,votes))
        cursor.execute("DELETE FROM Photo where review_id=%s",id)
        cursor.execute("DELETE FROM Review where id=%s",id)

def all_review_delete_query(cursor):
        rows=cursor.execute("SELECT id from Review")
        for row in rows:
            delete_review_query(row,cursor)