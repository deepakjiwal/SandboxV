
from flask import Flask,request, jsonify
from models import *
import collections
from database import init_db, db_session

import random
from faker import Faker

init_db()

fake = Faker()


#First populate the Speciality table
spec_List = ['Dentist','Cardiologist','Neurologist','General Physician','Pediatrician','Homeopath','Ayurveda','Orthopedist','Gynecologist','Dermatologist','Oncologist','Opthalmologist','ENT Specialist','Urologist','Pathologist','Radiologist','Anestheciologist','Nephrologist','Endocrinologist','Gastrologist','Veterinary']
for i in range(0,21) :
	spec = Speciality(spec_List[i])
	db_session.add(spec)

db_session.commit() 


#Second Populate the Clinic Tables
locList = ['Gandhinagar','Jayanagar','Motinagar','Urdu Bazaar','Alambagh','HumayunNagar','JahangirNagar','ShahjahanNagar','Nehru Road', 'Indira Nagar','AnandNagar','ShaktiNagar','RK Puram','DevNagar','MAayaBazaar','GolGhar','AishBagh','Connaught Place','DurgaPur','Atta Road','TransportNagar','CharBagh','BadshahNagar','ShahNagar','Victoria Road','Elizabeth Road','Viceroy Road','ShaktiPuram','Thumkunta','Lothkunta','Bannergatta','Arakere','Bilekahalli','HSR Layout','SitaPuram','RadhaPuram','LakshmiPuram','VishnuPuram','Golconda','Andheri','Daadar','Pali Hill','Navi Mumbai']
cityList = ['Hyderabad','Bangalore','Mumbai','Delhi','Lucknow','Jaipur','Kolkata','Chennai','Guahati','Gorakhpur']

for i in range(0,1000) :
	name1 = fake.company()
	name = name1.replace('-',' ')
	name = name.replace(',',' ')
	location = random.choice(locList)
	city = random.choice(cityList)
	address = fake.address()
	clinic = Clinic(name, location, city, address)
	db_session.add(clinic)

db_session.commit()


#Think something about the Doctor Tables
clinicnum=1000
specnum=21



for i in range(0,10000) :
	name = fake.name()
	experience = fake.random_int(min=1,max=40)
	contactNumber = fake.phone_number()
	fees = (fake.random_int(min = 1, max = 20))*50
	recommendations = fake.random_int(min = 1, max = 1000)
	qualification = fake.job()
	email = fake.email()
	doc = Doctor(name, experience, contactNumber, fees, recommendations, qualification, email)

	rand1 = fake.random_int( min = 1 , max = 3 )
	for i1 in range(0,rand1) :
		clinic_id = fake.random_int(min=1,max=999)
		clinic = db_session.query(Clinic).get(clinic_id)
		if clinic not in doc.clinics :
			clinic.doctors_clinic.append(doc)



	rand2 = fake.random_int(min = 1 , max = 3)
	for i2 in range(0,rand2) :
		spec_id = fake.random_int(min = 1, max = 20)
		spec = db_session.query(Speciality).get(spec_id)
		#spec.doctors_spec.append(doc)
#		db_session.commit()
		if spec not in doc.specializations :
			spec.doctors_spec.append(doc)



	db_session.add(doc)
db_session.commit()

