
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
	post = request.get_json()
	new_user = User(post['name'],post['contact_number'],post['email'])
	db_session.add(new_user)
	db_session.commit()
	response = {'returnCode': "SUCCESS", 'data':{}, 'errorCode':None}
	return jsonify(response)

@app.route('/getAllClinics', methods = ['GET'])
def getAllClinics():								#checked Correct
	# start = (int(page)-1)*10
	# end = int(page)*10
	all_Clinics = Clinic.query.all()
	clinics_List = []
	clinic_Detail={}
	for clinic in all_Clinics:
		clinic_Detail = {'id': clinic.id, 'name': clinic.name, 'location': clinic.location, 'city':clinic.city, 'address':clinic.address}
		clinics_List.append(clinic_Detail);
	return jsonify({'returnCode': "SUCCESS", 'data':clinics_List, 'errorCode':None})

@app.route('/deleteClinic',methods = ['POST'])		#checked Correct
def deleteClinic():
	post = request.get_json()
	clinic_To_Delete= db_session.query(Clinic).get(post['id'])
	db_session.delete(clinic_To_Delete)
	db_session.commit()
	response = {'returnCode': "SUCCESS", 'data':{}, 'errorCode':None}
	return jsonify(response)

@app.route('/editClinic', methods =['POST'])		#checked Correct
def editClinic():
	post = request.get_json()
	db_session.query(Clinic).filter_by(id = post['id']).update({'name':post['name'],'location':post['location'],'city':post['city'],'address':post['address']})
	db_session.commit()
	response = {'returnCode': "SUCCESS", 'data':{}, 'errorCode':None}
	return jsonify(response)

@app.route('/addDoctor', methods = ['POST'])		#checked correct
def addDoctor():
	post = request.get_json()
	doc_To_Add = Doctor(post['name'],post['experience'],post['contactNumber'],post['fees'],post['recommendations'],post['qualification'],post['email'])

	for clinic in post['clinics']:
		clinic_For_Doc = Clinic.query.filter_by(name=clinic['text']).first()
		clinic_For_Doc.doctors_clinic.append(doc_To_Add)
		db_session.commit()

	for speciality in post['specializations'] :
		speciality_For_Doc = Speciality.query.filter_by(name=speciality['text']).first()
		#the clinic id should already be added otherwise it will not add the doctor and will give an error.... how to handle the error??
		speciality_For_Doc.doctors_spec.append(doc_To_Add)
		db_session.commit()

	db_session.add(doc_To_Add)
	db_session.commit()
	response = {'returnCode': "SUCCESS", 'data':{}, 'errorCode':None}
	return jsonify(response)

@app.route('/getAllDoctors/<page>', methods = ['GET'])		#checked correct
def getAllDoctors(page):
	start = (int(page) - 1)*10
	end = int(page)*10
	all_Doctors = Doctor.query.slice(start,end)
	docs_List = []
	doctor_Details={}
	clinic_List_For_A_Doctor = []
	#clinic_Details_For_A_Clinic = {}
	spec_List_For_A_Doctor = []
	#spec_Details_For_A_Clinic = {}
	for doc in all_Doctors:
		clinic_List_For_A_Doctor=[]
		spec_List_For_A_Doctor=[]
		for clinic in doc.clinics:
			clinic_List_For_A_Doctor.append({'clinic_id':clinic.id, 'clinic_name':clinic.name,'clinic_location':clinic.location,'clinic_city':clinic.city,'clinic_address':clinic.address})
		for specialization in doc.specializations:
			spec_List_For_A_Doctor.append({'spec_id':specialization.id, 'spec_name':specialization.name})
		doctor_Details = {'doc_id' : doc.id, 'doc_name': doc.name, 'doc_experience': doc.experience, 'doc_contactNumber': doc.contactNumber, 'doc_fees':doc.fees, 'doc_recommendations':doc.recommendations, 'doc_qualification':doc.qualification,'doc_email':doc.email, 'clinic_List_For_A_Doc':clinic_List_For_A_Doctor,'spec_List_For_A_Doc':spec_List_For_A_Doctor};
		docs_List.append(doctor_Details);
	return jsonify({'returnCode': "SUCCESS", 'data':docs_List, 'errorCode':None})

@app.route('/deleteDoctor',methods = ['POST'])		#checked correct
def deleteDoctor():
	post = request.get_json()
	doctor_To_Delete=db_session.query(Doctor).get(post['doctorId'])
	db_session.delete(doctor_To_Delete)
	db_session.commit()
	response = {'returnCode': "SUCCESS", 'data':{}, 'errorCode':None}
	return jsonify(response)

@app.route('/editDoctor',methods =['POST'])		#checked correct
def editDoctor():
	post = request.get_json()
	doc = Doctor.query.filter(Doctor.id==post['id']).first()
	#clinicsOfDoctor = doc.clinics.query.all()
	clinic_To_Be_Removed = None;
	for aClinic in doc.clinics:
		clinic_To_Be_Removed = Clinic.query.filter(Clinic.id==aClinic.id).first()
		clinic_To_Be_Removed.doctors_clinic.remove(doc)
		db_session.commit()

	specialization_To_Be_Removed = None
	for aSpecialization in doc.specializations:
		specialization_To_Be_Removed = Speciality.query.filter(Speciality.id==aSpecialization.id).first()
		specialization_To_Be_Removed.doctors_spec.remove(doc)
		db_session.commit()


	doc.name = post['name']
	doc.experience = post['experience']
	doc.contactNumber = post['contactNumber']
	doc.fees = post['fees']
	doc.recommendations = post['recommendations']
	doc.qualification = post['qualification']
	doc.email = post['email']
	clinic_To_Be_Updated = None;
	for clinic in post['clinics']:
		clinic_To_Be_Updated = Clinic.query.filter_by(name=clinic['text']).first()
		clinic_To_Be_Updated.doctors_clinic.append(doc)
		db_session.commit()

	specialization_To_Be_Updated = None
	for spec in post['specializations']:
		specialization_To_Be_Updated = Speciality.query.filter_by(name=spec['text']).first()
		specialization_To_Be_Updated.doctors_spec.append(doc)
		db_session.commit()
	db_session.commit()
	response = {'returnCode': "SUCCESS", 'data':{}, 'errorCode':None}
	return jsonify(response)

@app.route('/addSpecialization', methods = ['POST'])		#checked correct
def addSpecialization():
	post = request.get_json()
	spec_To_Add = Speciality(post['name'])
	db_session.add(spec_To_Add)
	db_session.commit()
	response = {'returnCode': "SUCCESS", 'data':{}, 'errorCode':None}
	return jsonify(response)

@app.route('/getAllSpecializations', methods = ['GET'])		#checked correct
def getAllSpecializations():
	all_Specialities = Speciality.query.all()
	specs_List = []
	spec_Details={}
	for spec in all_Specialities:
		spec_Details = {'id':spec.id,'name':spec.name};
		specs_List.append(spec_Details);
	return jsonify({'returnCode': "SUCCESS", 'data':specs_List, 'errorCode':None})
		#doctorObject = {'id': clinic.id, 'name': clinic.name, 'location': clinic.location, 'city':clinic.city, 'address':clinic.address};
		#clinics.append(clinicObject);

@app.route('/deleteSpecialization',methods = ['POST'])		#checked correct
def deleteSpecialization():
	post = request.get_json()
	speciality_To_Delete=db_session.query(Speciality).get(post['specId'])
	db_session.delete(speciality_To_Delete)
	db_session.commit()
	response = {'returnCode': "SUCCESS", 'data':{}, 'errorCode':None}
	return jsonify(response)

@app.route('/editSpecialization',methods =['POST'])			#checked corrrect
def editSpecialization():
	post = request.get_json()
	db_session.query(Speciality).filter_by(id=post['id']).update({'name':post['name']})
	db_session.commit()
	response = {'returnCode': "SUCCESS", 'data':{}, 'errorCode':None}
	return jsonify(response)


@app.route('/getSelectedClinics/<substr>', methods = ['GET'])
def getSelectedClinics(substr):
	all_Clinics = Clinic.query.filter(Clinic.name.startswith(substr.lower())).all()
	clinics_List = []
	clinic_Detail={}
	for clinic in all_Clinics:
		clinic_Detail = {'text': clinic.name}
		clinics_List.append(clinic_Detail)
	return jsonify({'returnCode': "SUCCESS", 'data':clinics_List, 'errorCode':None})

@app.route('/getSelectedSpecializations/<substr>', methods = ['GET'])
def getSelectedSpecializations(substr):
	specializations_Result = Speciality.query.filter(Speciality.name.startswith(substr)).all()
	specialization_List = []
	specialization_Detail={}
	for spec in specializations_Result:
		specialization_Detail = {'text': spec.name}
		specialization_List.append(specialization_Detail)
	return jsonify({'returnCode': "SUCCESS", 'data':specialization_List, 'errorCode':None})
