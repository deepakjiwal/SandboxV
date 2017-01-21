
from flask import Flask,request, jsonify, render_template
from models import *
import collections
from database import init_db, db_session
from app import app
from textblob import TextBlob
from textblob import Word
from textblob.wordnet import VERB

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

def isFeatureSemanticallyCorrect(featureDescription1, featureDescription2):

    listStoppingWords = ["a","about","above","after","again","against",
	"all","am","an","and","any","are","aren't","as","at","be","because",
	"been","before","being","below","between","both","but","by","can't",
	"cannot","could","couldn't","did","didn't","do","does","doesn't","doing"
	"don't","down","during","each","few","for","from","further","had","hadn't",
	"has","hasn't","have","haven't","having","he","he'd","he'll","he's","her"
	"here","here's","hers","herself","him","himself","his","how","how's",
	"i","i'd","i'll","i'm","i've","if","in","into","is","isn't","it","it's",
	"its","itself","let's","me","more","most","mustn't","my","myself","no",
	"nor","not","of","off","on","once","only","or","other","ought","our","ours",
	"ourselves","out","over","own","same","shan't","she","she'd","she'll",
	"she's","should","shouldn't","so","some","such","than","that","that's",
	"the","their","theirs","them","themselves","then","there","there's","these",
	"they","they'd","they'll","they're","they've","this","those","through","to",
	"too","under","until","up","very","was","wasn't","we","we'd","we'll","we're",
	"we've","were","weren't","what","what's","when","when's","where","where's",
	"which","while","who","who's","whom","why","why's","with","won't","would",
	"wouldn't","you","you'd","you'll","you're","you've","your","yours","yourself",
	"yourselves","needed","required"]
    featureDescription1 = TextBlob(featureDescription1)
    featureDescription2 = TextBlob(featureDescription2)
    finalfeatureDescription1 = []
    for word in featureDescription1.words:
        if not word in listStoppingWords:
            finalfeatureDescription1.append(word)
	finalfeatureDescription2 = []
    for word in featureDescription2.words:
        if not word in listStoppingWords:
            finalfeatureDescription2.append(word)
    finalFeatureDescription1Str = ' '.join(finalfeatureDescription1)
    finalFeatureDescription2Str = ' '.join(finalfeatureDescription2)
    finalFeatureDescription1Str = TextBlob(finalFeatureDescription1Str)
    finalFeatureDescription2Str = TextBlob(finalFeatureDescription2Str)
    finalFeatureDescription1Str = finalFeatureDescription1Str.correct()
    finalFeatureDescription2Str = finalFeatureDescription2Str.correct()
    featureDesc1LemList = []
    for word in finalFeatureDescription1Str.words:
        featureDesc1LemList.append(word.lemmatize())
    featureDesc2LemList = []
    for word in finalFeatureDescription2Str.words:
        featureDesc2LemList.append(word.lemmatize())
    featureDesc1LemStr = ' '.join(featureDesc1LemList)
    featureDesc2LemStr = ' '.join(featureDesc2LemList)
    featureDesc1LemStr = TextBlob(featureDesc1LemStr)
    featureDesc2LemStr = TextBlob(featureDesc2LemStr)
    featureDescription1synsets = []
    for word in featureDesc1LemStr.words:
		for synset in word.synsets:
			featureDescription1synsets.append(synset)
    featureDescription2synsets = []
    for word in featureDesc2LemStr.words:
        for synset in word.synsets:
            featureDescription2synsets.append(synset)
    commonSynsets = []
    commonSynsets = list(set(featureDescription1synsets).intersection(featureDescription2synsets))
    commonSynsetsCount = len(commonSynsets)
    if(commonSynsetsCount > 0):
        feature1SynsetCount = len(featureDescription1synsets)
        feature2SynsetCount = len(featureDescription2synsets)
        percentage = ((commonSynsetsCount * 200) / (feature1SynsetCount + feature2SynsetCount))
        if(percentage > 25):
            return True
        else:
            return False
    else:
        return False


@app.route('/addFeature', methods = ['POST'])		#checked  correct
def addFeature():
	feature = request.get_json()
	currentDescription = feature['description']
	print feature['description']
	all_Features = db_session.query(Feature).filter_by(feature_type = feature['feature_type']).all()
	matchingFeaturesList = []
	feature_Detail = {}
	for features in all_Features:
		if isFeatureSemanticallyCorrect(features.description,currentDescription):
			feature_Detail = {'id': features.id, 'name': features.name,
			'description': features.description, 'created_by':features.created_by,
			'status':features.status, 'feature_type':features.feature_type }
			matchingFeaturesList.append(feature_Detail)
	if len(matchingFeaturesList) > 0:
		print matchingFeaturesList
		response = {'returnCode': "SUCCESS", 'data':matchingFeaturesList, 'errorCode':None}
		return jsonify(response),409
	else:
		print "abcd"
		print feature['name']
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

@app.route('/getAllFeatures/', methods = ['GET'])
@app.route('/getAllFeatures/<substr>/', methods = ['GET'])		#checked correct
@app.route('/getAllFeatures/<int:practo_id>/', methods = ['GET'])
@app.route('/getAllFeatures/<int:practo_id>/<int:others>', methods = ['GET'])
@app.route('/getAllFeatures/<substr>/<int:practo_id>/<int:others>', methods = ['GET'])
@app.route('/getAllFeatures/<substr>/<int:practo_id>/', methods = ['GET'])
def getAllFeatures(substr = "", practo_id = 0, others = 0):

	if(practo_id == 0):
		all_Features = Feature.query.filter(Feature.feature_type.startswith(substr.lower())).all()
	else:
		if(others == 0):
			all_Features = db_session.query(Feature).filter(Feature.
			feature_type.startswith(substr.lower())).filter_by(created_by = practo_id).all()
		else :
			all_Features = db_session.query(Feature).filter(Feature.
			feature_type.startswith(substr.lower())).filter(Feature.created_by != practo_id).all()


	feature_List = []
	feature_Detail = {}
	count = 0;
	for feature in all_Features:
		up_vote_count = db_session.query(User_Feature).filter_by(feature_id =
		feature.id, liked = True).count()
		down_vote_count = db_session.query(User_Feature).filter_by(feature_id =
		feature.id, liked = False).count()
		upvote_status = False
		downvote_status = False
		if(practo_id != 0):
			status = db_session.query(User_Feature).filter_by(user_id =
			practo_id, feature_id = feature.id).first()
			if (status != None):
				if (status.liked == 1):
					upvote_status = True
				else:
					downvote_status = True
		feature_Detail = {'id': feature.id, 'name': feature.name,
		'description': feature.description, 'created_by':feature.created_by,
		'status':feature.status, 'feature_type':feature.feature_type,
		'up_vote_count': up_vote_count, 'down_vote_count': down_vote_count,
		'upvote_status': upvote_status, 'downvote_status': downvote_status}
		feature_List.append(feature_Detail);
		count = count + 1;

	return jsonify({'data':feature_List, 'total':count})
	#return jsonify({'returnCode': "SUCCESS", 'data':feature_List, 'total':count}), 400


@app.route('/getAllApproved/', methods = ['GET'])
def getAllApprovedFeatures():
	all_Features = Feature.query.filter_by(status = 'approved').all()
	feature_List = []
	feature_Detail = {}
	count = 0;
	for feature in all_Features:
		feature_Detail = {'id': feature.id, 'name': feature.name,
		'description': feature.description, 'created_by':feature.created_by,
		'status':feature.status, 'feature_type':feature.feature_type}
		feature_List.append(feature_Detail);
		count = count + 1;

	return jsonify({'data':feature_List, 'total':count})

@app.route('/vote', methods =['POST'])		#checked Correct
def vote():
	vote = request.get_json()
	upvote_status = False
	downvote_status = False
	like = vote['like']
	if like:
		up_vote_cursor = db_session.query(User_Feature).filter_by(feature_id =
		vote['feature_id'], user_id = vote['user_id'], liked = True)
		if up_vote_cursor.count() > 0:
			upvote_status = False
			row_to_delete= up_vote_cursor.first()
			db_session.delete(row_to_delete)
			db_session.commit()
		else:
			upvote_status = True
			down_vote_cursor = db_session.query(User_Feature).filter_by(feature_id =
			vote['feature_id'], user_id = vote['user_id'], liked = False)
			if down_vote_cursor.count() > 0:
				down_vote_cursor.update({'liked':True})
				db_session.commit()
			else:
				user_feature = User_Feature(vote['user_id'],vote['feature_id'],
				True,vote['comment'])
				db_session.add(user_feature)
				db_session.commit()
	else:
		down_vote_cursor = db_session.query(User_Feature).filter_by(feature_id =
		vote['feature_id'], user_id = vote['user_id'], liked = False)
		if down_vote_cursor.count() > 0:
			downvote_status = False
			row_to_delete= down_vote_cursor.first()
			db_session.delete(row_to_delete)
			db_session.commit()
		else:
			downvote_status = True
			up_vote_cursor = db_session.query(User_Feature).filter_by(feature_id
			= vote['feature_id'], user_id = vote['user_id'], liked = True)
			if up_vote_cursor.count() > 0:
				up_vote_cursor.update({'liked':False})
			else:
				user_feature = User_Feature(vote['user_id'],vote['feature_id'],
				False,vote['comment'])
				db_session.add(user_feature)
				db_session.commit()

	up_vote_count = db_session.query(User_Feature).filter_by(feature_id =
	vote['feature_id'], liked = True).count()
	down_vote_count = db_session.query(User_Feature).filter_by(feature_id =
	vote['feature_id'], liked = False).count()
	response = {'returnCode': "SUCCESS", 'up_vote_count': up_vote_count,
	'down_vote_count': down_vote_count, 'upvote_status': upvote_status,
	'downvote_status': downvote_status, 'errorCode':None}
	return jsonify(response)
