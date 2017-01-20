
from flask import Flask,request, jsonify, render_template
from models import *
import collections
from database import init_db, db_session
from app import app

#@app.route('/')			#correct
#def serveStatic():
#	return app.send_static_file('index.html')

@app.route('/')
def index():
	return render_template("index.html")

@app.route('/<path:path>')
def static_proxy(path):
  # send_static_file will guess the correct MIME type
  return app.send_static_file(path)

@app.route('/addUser', methods = ['POST'])		#checked  correct
def addUser():
	user = request.get_json()
	row = db_session.query(User).filter_by(email=user['email']).count()
	if row == 0:
		new_user = User(user['practo_id'], user['name'],user['contact_number'],user['email'])
		db_session.add(new_user)
		db_session.commit()
		response = {'returnCode': "SUCCESS", 'data':{}, 'errorCode':None}
		return jsonify(response)
	else:
		response = {'returnCode': "CONFLICT", 'data':{}, 'errorCode':None}
		return jsonify(response), 409

@app.route('/addFeature', methods = ['POST'])		#checked  correct
def addFeature():
	feature = request.get_json()
	new_feature = Feature(feature['name'],feature['description'],
	feature['created_by'],feature['status'],feature['feature_type'])
	db_session.add(new_feature)
	db_session.commit()
	response = {'returnCode': "SUCCESS", 'data':{}, 'errorCode':None}
	return jsonify(response)

@app.route('/deleteFeature',methods = ['DELETE'])		#checked Correct
def deleteClinic():
	feature = request.get_json()
	feature_to_delete= db_session.query(Feature).get(feature['id'])
	db_session.delete(clinic_to_delete)
	db_session.commit()
	response = {'returnCode': "SUCCESS", 'data':{}, 'errorCode':None}
	return jsonify(response)

@app.route('/editFeature', methods =['PATCH'])		#checked Correct
def editClinic():
	feature = request.get_json()
	db_session.query(feature).filter_by(id = feature['id']).update(
	{'name':post['name'],'description':feature['description'],
	'created_by':feature['created_by'],'status':feature['status'],
	'feature_type':feature['feature_type']})
	db_session.commit()
	response = {'returnCode': "SUCCESS", 'data':{}, 'errorCode':None}
	return jsonify(response)

@app.route('/getAllFeatures', methods = ['GET'])		#checked correct
def getAllFeatures():
	all_Features = Feature.query.all()
	feature_List = []
	feature_Detail = {}
	count = 0;
	for feature in all_Features:
		up_vote = db_session.query(User_Feature).filter_by(feature_id =
		feature.id, like_count = 1).count()
		down_vote = db_session.query(User_Feature).filter_by(feature_id =
		feature.id, like_count = 0).count()
		feature_Detail = {'id': feature.id, 'name': feature.name,
		'description': feature.description, 'created_by':feature.created_by,
		'status':feature.status, 'feature_type':feature.feature_type,
		'up_vote': up_vote, 'down_vote': down_vote}
		feature_List.append(feature_Detail);
		count = count + 1;

	return jsonify({'data':feature_List, 'total':count})
	#return jsonify({'returnCode': "SUCCESS", 'data':feature_List, 'total':count}), 400
