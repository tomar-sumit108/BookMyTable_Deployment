import pymysql
from app import app
from db_config import mysql
from flask import jsonify,flash,request
from util.sendGetResponse import send_get_response
from LoginSignUp.util.required import token_required
from User.BeenThere.get import get_beenthere
from User.Bookmark.get import get_bookmark
from CommentRating.get import get_reviews

def convert_user(cursor,rows):
    for row in rows:
        get_beenthere(row=row)
        get_bookmark(row=row)
        row['reviews']=get_reviews(userId=row['id']).json