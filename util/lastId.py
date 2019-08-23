import pymysql
from app import app
from db_config import mysql
from flask import jsonify
from flask import flash, request



def get_last_id(cursor):
    try:
        cursor.execute("SELECT LAST_INSERT_ID()")
        rows=cursor.fetchall()
        
        return rows[0][0]
    except Exception as e:
        print("ID",e,"ID")