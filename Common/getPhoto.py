import os
from app import app
from flask import Flask,flash,request,redirect,url_for,session,send_from_directory,jsonify

@app.route('/api/photos/<path:path>')
def get_file(path):
    directory=request.args.get('dir',default='%',type=str)
    if directory!="review" and directory!="restaurantProfile" and directory!="userProfile":
        return jsonify("BAD REQUEST"),400
    return send_from_directory(os.path.join(app.config['UPLOAD_FOLDER'],directory),path,as_attachment=False)