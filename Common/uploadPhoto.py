import os
from app import app
from flask import Flask,flash,request,redirect,url_for,session,jsonify
from werkzeug.utils import secure_filename
from flask_cors import CORS, cross_origin
from LoginSignUp.util.required import token_required
import uuid


@app.route('/api/photos', methods=['POST'])
@token_required
def fileUpload(current_user):
    directory=request.args.get('dir',default='%',type=str)
    if directory!="review" and directory!="restaurantProfile" and directory!="userProfile":
        return jsonify("BAD REQUEST"),400

    target=os.path.join(app.config['UPLOAD_FOLDER'],directory)
    if not os.path.isdir(target):
        os.mkdir(target)
    
    required_extension=["png","jpeg","jpg"]
    if 'file' not in request.files:
        return jsonify("NO FILE"),400
    file = request.files['file'] 
    extension=file.filename.split(".")[-1]
    if not extension in required_extension:
        return jsonify("Check file type"),400
    filename=str(uuid.uuid4())
    destination="/".join([target, filename+"."+extension])
    file.save(destination)
    response=jsonify(filename+"."+extension)
    print(filename+"."+extension)
    response.headers.add('Access-Control-Allow-Origin','*')
    return response,201

