
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
	row = db_session.query(User).filter_by(practo_id=user['practo_id']).count()
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
	db_session.delete(feature_to_delete)
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
		feature_Detail = {'id': feature.id, 'name': feature.name, 'description': feature.description, 'created_by':feature.created_by, 'status':feature.status, 'feature_type':feature.feature_type}
		feature_List.append(feature_Detail);
		count = count + 1;
		likeCount = db_session.query(User_Feature).filter_by(feature_id = feature.id, like = True)
		#feature_Detail.up_vote = likeCount
		print likeCount
	return jsonify({'data':feature_List, 'total':count})
	#return jsonify({'returnCode': "SUCCESS", 'data':feature_List, 'total':count}), 400


@app.route('/vote', methods =['POST'])		#checked Correct
def vote():
	vote = request.get_json()
	like = vote['like']
	if like:
		up_vote_cursor = db_session.query(User_Feature).filter_by(feature_id =
		vote['feature_id'], user_id = vote['user_id'], like = True)
		if up_vote_cursor.count() > 0:
			row_to_delete= up_vote_cursor.first()
			db_session.delete(row_to_delete)
			db_session.commit()
		else:
			down_vote_cursor = db_session.query(User_Feature).filter_by(feature_id =
			vote['feature_id'], user_id = vote['user_id'], like = False)
			if down_vote_cursor.count() > 0:
				down_vote_cursor.update({'like':True})
			else:
				user_feature = User_Feature(vote['user_id'],vote['feature_id'],
				True,vote['comment'])
				db_session.add(user_feature)
				db_session.commit()
	else:
		down_vote_cursor = db_session.query(User_Feature).filter_by(feature_id =
		vote['feature_id'], user_id = vote['user_id'], like = False)
		if down_vote_cursor.count() > 0:
			row_to_delete= down_vote_cursor.first()
			db_session.delete(row_to_delete)
			db_session.commit()
		else:
			up_vote_cursor = db_session.query(User_Feature).filter_by(feature_id
			= vote['feature_id'], user_id = vote['user_id'], like = True)
			if up_vote_cursor.count() > 0:
				up_vote_cursor.update({'like':False})
			else:
				user_feature = User_Feature(vote['user_id'],vote['feature_id'],
				False,vote['comment'])
				db_session.add(user_feature)
				db_session.commit()

	up_vote_count = db_session.query(User_Feature).filter_by(feature_id =
	vote['feature_id'], like = True).count()
	down_vote_count = db_session.query(User_Feature).filter_by(feature_id =
	vote['feature_id'], like = False).count()
	response = {'returnCode': "SUCCESS", 'up_vote_count': up_vote_count,
	'down_vote_count': down_vote_count, 'errorCode':None}
	return jsonify(response)
