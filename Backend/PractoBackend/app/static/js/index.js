var practo = angular.module("PractoBackend", ["ngRoute","ngTagsInput"]);

practo.config(function($routeProvider){
	$routeProvider
	.when('/doctors',{
		templateUrl: 'doctors.html',
		controller: 'doctorsController'
	})
	.when('/clinics',{
		templateUrl: "clinics.html",
		controller: "clinicsController"
	})
	.when('/specializations',{
		templateUrl: "specializations.html",
		controller: "specializationsController"
	})
	.when('/insertClinic',{
		templateUrl: "insertClinic.html",
		controller: "insertClinicController"
	})
	.when('/insertDoctor',{
		templateUrl: "insertDoctor.html",
		controller: "insertDoctorController"
	})
	.when('/insertSpecialization',{
		templateUrl: "insertSpecialization.html",
		controller: "insertSpecializationController"
	})
	.when('/editDoctor',{
		templateUrl: "editDoctor.html",
		controller: "editDoctorController"
	})
	.when('/editClinic',{
		templateUrl: "editClinic.html",
		controller: "editClinicController"
	})
	.when('/editSpecialization',{
		templateUrl: "editSpecialization.html",
		controller: "editSpecializationController"
	})
	.otherwise({redirectTo:'/doctors'})
});


practo.controller("tabsController",function($scope,$rootScope,$location){
	$rootScope.activeTab = 1;
	$scope.tabClicked = function(tab){
			if(tab == 1){
				$rootScope.activeTab = 1;
				$location.path('/doctors');
			}
			else if(tab == 2){
				$rootScope.activeTab = 2;
				$location.path('/clinics');
			}
			else {
				$rootScope.activeTab = 3;
				$location.path('/specializations');
			}
	}
});

practo.controller("doctorsController", function($scope,$rootScope,$http,$location) {
	$rootScope.activeTab = 1;
	var req = {
    method: 'GET',
    url: 'http://localhost:3000/getAllDoctors/1',
    headers: {'Content-Type': 'application/json'}
  };
  $http(req)
  .success(function(data){
    if(data.returnCode == "SUCCESS")
    {
    	$scope.doctors = data.data;
    	console.log($scope.doctors);
  	}
  	else
  	{
  		console.log("There is an error")
  	}
  })
  .error(function(){
  	console.log("Error connecting to the server");
  });


  $scope.addDoctor = function() {
    $location.path('/insertDoctor');
  }

  $scope.editDoctor = function(doctor){
  	$rootScope.doctorToEdit = doctor;
  	$location.path('/editDoctor');
  }

  $scope.removeDoctor = function(doctor,index){
    console.log(doctor);
    var req = {
      method: 'POST',
      url: 'http://localhost:3000/deleteDoctor',
      headers: {'Content-Type': 'application/json'},
      data : {doctorId: doctor.doc_id}
    };
    $http(req)
    .success(function(data){
      if(data.returnCode == "SUCCESS")
      {
        $scope.doctors.splice(index,index+1)
        console.log("doctor deleted");
      }
      else
      {
        console.log("There is an error")
      }
    })
    .error(function(){
      console.log("Error connecting to the server");
    });
  }


});


practo.controller("clinicsController", function($scope,$http,$rootScope,$location){
	$rootScope.activeTab = 2;
	$scope.clinics = [];

	var req = {
    method: 'GET',
    url: 'http://localhost:3000/getAllClinics',
    headers: {'Content-Type': 'application/json'}
  };
  $http(req)
  .success(function(data){
    if(data.returnCode == "SUCCESS")
    {
    	$scope.clinics = data.data;
    }
    else
    {
    	console.log("There is an error")
    }
  })
  .error(function(){
  	console.log("Error connecting to the server");
  });

  $scope.addClinic = function() {
    $location.path('/insertClinic');
  }

  $scope.editClinic = function(clinic){
  	$rootScope.clinicToEdit = clinic;
		$location.path('/editClinic');
  };

  $scope.removeClinic = function(clinic,index){
    console.log(clinic);
    var req = {
      method: 'POST',
      url: 'http://localhost:3000/deleteClinic',
      headers: {'Content-Type': 'application/json'},
      data : {id: clinic.id}
    };
    $http(req)
    .success(function(data){
      if(data.returnCode == "SUCCESS")
      {
        $scope.clinics.splice(index,index+1)
        console.log("clinic deleted");
      }
      else
      {
        console.log("There is an error")
      }
    })
    .error(function(){
      console.log("Error connecting to the server");
    });
  }

});

practo.controller("specializationsController", function($scope,$http,$rootScope,$location){
	$rootScope.activeTab = 3;
	$scope.specializations = [];
	var req = {
        	method: 'GET',
            url: 'http://localhost:3000/getAllSpecializations',
            headers: {'Content-Type': 'application/json'}
        };

  $http(req).
  success(function(data){
    if(data.returnCode == "SUCCESS")
    {
    	$scope.specializations = data.data;
    }
    else
    {
    	console.log("Error in retrieving specializations");
    }
  })
  .error(function(){
		console.log("Error Connecting to the backend");
  });


  $scope.addSpecialization = function() {
    $location.path('/insertSpecialization');
  }

  $scope.editSpecialization= function(spec){
      $rootScope.specializationToEdit = spec;
      console.log(spec);
      $location.path('/editSpecialization');
  }

  $scope.removeSpecialization = function(spec,index){

    var req = {
      method: 'POST',
      url: 'http://localhost:3000/deleteSpecialization',
      headers: {'Content-Type': 'application/json'},
      data : {specId: spec.id}
    };
    $http(req)
    .success(function(data){
      if(data.returnCode == "SUCCESS")
      {
        $scope.specializations.splice(index,index+1)
        console.log("spec deleted");
      }
      else
      {
        console.log("There is an error")
      }
    })
    .error(function(){
      console.log("Error connecting to the server");
    });
  }


});

practo.controller("insertClinicController",function($scope,$http,$location){
	$scope.addClinic = function(){
		var req = {
        	method: 'POST',
            url: 'http://localhost:3000/addClinic',
            headers: {'Content-Type': 'application/json'},
            data: {name: $scope.name, location:$scope.location, city:$scope.city, address: $scope.address}
        };
       	$http(req).
       	success(function(data){

          $location.path('/clinics');
       		console.log(data);
       	})
       	.error(function(){
       		console.log("Error Connecting to the backend");
       	})
	}
});


practo.controller("insertDoctorController",function($scope,$http,$location,$q){
	
  $scope.specializations = [];
  $scope.loadSpecializations = function(subString){
    console.log(subString);
    var d = $q.defer();
    $http.get('http://localhost:3000/getSelectedSpecializations/'+subString).success(function(data){
      d.resolve(data.data);
    });
    return d.promise;
  };
  $scope.clinics = [];
  $scope.loadClinics = function(subString){
    console.log(subString);
    var d = $q.defer();
    $http.get('http://localhost:3000/getSelectedClinics/'+subString).success(function(data){
      d.resolve(data.data);
    });
    return d.promise;
  };

	$scope.addDoctor = function(){
		console.log($scope.specializations);
		console.log($scope.clinics);
    for(clinic in $scope.clinics)
    {
      $scope.clinics[clinic].text = $scope.clinics[clinic].text.replace("-"," ");
    }

    console.log($scope.clinics);
		var req = {
      method: 'POST',
      url: 'http://localhost:3000/addDoctor',
        headers: {'Content-Type': 'application/json'},
        data: {name: $scope.name, qualification:$scope.qual, experience: $scope.exp, fees : $scope.fees, recommendations:$scope.recommendations, clinics:$scope.clinics, specializations:$scope.specializations, contactNumber:$scope.mobileNumber, email: $scope.email}
    };
    $http(req).
    success(function(data){
      $location.path('/doctors');
      console.log(data);
    })
    .error(function(){
      console.log("Error Connecting to the backend");
   	})
	}
});

practo.controller("insertSpecializationController",function($scope,$http,$location){
	$scope.addSpecialization = function(){
		var req = {
        	method: 'POST',
            url: 'http://localhost:3000/addSpecialization',
            headers: {'Content-Type': 'application/json'},
            data: {name: $scope.specialization}
        };
       	$http(req).
       	success(function(data){

          $location.path('/specializations');
       		console.log(data);
       	})
       	.error(function(){
       		console.log("Error Connecting to the backend");
       	})
	}
});

practo.controller("editDoctorController",function($scope,$http,$rootScope,$location,$q){
	var doctor = $rootScope.doctorToEdit;
	$scope.name = doctor.doc_name;
	$scope.qual = doctor.doc_qualification;
	$scope.exp = doctor.doc_experience;
  console.log(doctor.doc_contactNumber);
	$scope.mobileNumber = doctor.doc_contactNumber;
  $scope.recommendations = Number(doctor.doc_recommendations);
  $scope.fees = Number(doctor.doc_fees)

	$scope.email = doctor.doc_email;

	$scope.specializations = [];
  for(i in doctor.spec_List_For_A_Doc)
  {
    $scope.specializations.push({text : doctor.spec_List_For_A_Doc[i].spec_name});
  }

  $scope.loadSpecializations = function(subString){
    console.log(subString);
    var d = $q.defer();
    $http.get('http://localhost:3000/getSelectedSpecializations/'+subString).success(function(data){
      d.resolve(data.data);
    });
    return d.promise;
  };
  $scope.clinics = [];
  for(i in doctor.clinic_List_For_A_Doc)
  {
    console.log(doctor.clinic_List_For_A_Doc[i].clinic_name);
    $scope.clinics.push({text : doctor.clinic_List_For_A_Doc[i].clinic_name});
  }

  $scope.loadClinics = function(subString){
    console.log(subString);
    var d = $q.defer();
    $http.get('http://localhost:3000/getSelectedClinics/'+subString).success(function(data){
      d.resolve(data.data);
    });
    return d.promise;
  };

	$scope.editDoctor = function(){
    console.log("Entered into editDoctor");
    for(spec in $scope.specializations)
    {
      $scope.specializations[spec].text = $scope.specializations[spec].text.replace("-"," ");
    }
    for(clinic in $scope.clinics)
    {
      $scope.clinics[clinic].text = $scope.clinics[clinic].text.replace("-"," ");
    }
    console.log($scope.clinics);
		var req = {
        	method: 'POST',
            url: 'http://localhost:3000/editDoctor',
            headers: {'Content-Type': 'application/json'},
            data: {id:doctor.doc_id, name: $scope.name, qualification:$scope.qual , experience: $scope.exp, clinics:$scope.clinics, specializations:$scope.specializations, recommendations:$scope.recommendations, fees:$scope.fees, contactNumber:$scope.mobileNumber, email: $scope.email}
        };
       	$http(req).
       	success(function(data){
       		if(data.returnCode == "SUCCESS")
       		{
       			console.log(data);
            $location.path('/doctors');
       		}
       		else
       		{
       			console.log("Error Updating the doctor");
       		}
       	})
       	.error(function(){
       		console.log("Error Connecting to the backend");
       	});
	}
});


practo.controller("editClinicController",function($scope,$http,$rootScope,$location){
	var clinic = $rootScope.clinicToEdit;
	console.log(clinic);
	$scope.name = clinic.name;
	$scope.location = clinic.location;
	$scope.city = clinic.city;
	$scope.address = clinic.address;

	$scope.editClinic = function(){
		var req = {
        	method: 'POST',
            url: 'http://localhost:3000/editClinic',
            headers: {'Content-Type': 'application/json'},
            data: {id:clinic.id, name: $scope.name, location:$scope.location, city:$scope.city, address: $scope.address}
        };
       	$http(req).
       	success(function(data){
       		console.log(data);
          $location.path('/clinics');
       	})
       	.error(function(){
       		console.log("Error Connecting to the Server");
       	})
	}
});


practo.controller("editSpecializationController",function($scope,$http,$rootScope,$location){
  var specialization = $rootScope.specializationToEdit; 
  $scope.specialization = specialization.name;
  $scope.addSpecialization = function(){
    var req = {
      method: 'POST',
      url: 'http://localhost:3000/editSpecialization',
      headers: {'Content-Type': 'application/json'},
      data: {id:specialization.id,name: $scope.specialization}
    };
    $http(req).
    success(function(data){
      console.log(data);
      $location.path('/specializations');
    })
    .error(function(){
      console.log("Error Connecting to the backend");
    })
  }
});