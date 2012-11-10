'use strict';

/* Controllers */

function klasses($scope,Klass) {
    var klasses = $scope.klasses = Klass.query();

    $scope.addClass = function(class_name) {
        klasses.push({'name':class_name, 
                      'date':"today!",
                      'active':true});
        $scope.next_id++;
    }

    $scope.delClass = function(klass) {
        var r = confirm("Are you sure you want to delete this class? This will permanently remove all the data about it!!!")
        if(r){
            klasses.splice(klasses.indexOf(klass),1);
        };
    }

    $scope.toggle = function(klass) {
        var i = klasses.indexOf(klass)
        var current = klasses[i].active
        klasses[i].active = !current

    }
}
klasses.$inject = ['$scope','Klass'];

function klass($scope,$filter,Klass,$routeParams,$location) {
    var klass = $scope.klass = Klass.get({'classId':$routeParams.classId},function(klass){
        angular.forEach(klass.students,function(value,key){ 
            klass.students[key].send_msg = false;
        })
    })
    //Msg#SepIDLast NameFirst NameDECP1 P2TeacherStatusParent's NameGrPhone #R inW inR outW out
    $scope.header_map = [{"key":"sep_id","value":"SepID"},
                         {"key":"last_name","value":"Last Name"},
                         {"key":"first_name","value":'First Name'},
                         {"key":"dec","value":'DEC'},
                         {"key":"p1","value":"P1"},
                         {"key":"p2","value":"P2"},
                         {"key":"teacher","value":"Teacher"},
                         {"key":"status","value":"Status"},
                         {"key":"parents_name","value":"Parent's Name"},
                         {"key":"grade","value":"Gr"},
                         {"key":"phone","value":"Phone #"},
                         {"key":"r_in","value":"R in"},
                         {"key":"w_in","value":"W in"},
                         {"key":"r_out","value":"R out"},
                         {"key":"w_out","value":"W out"}];

    $scope.status_map = [
        {'key':"enr","long_name":"Enrolled","short_name":"Enr"},
        {'key':"wd","long_name":"Withdrawn","short_name":"WD"},
        {'key':"adm","long_name":"Admitted","short_name":"Adm"}
    ]  

    $scope.score_columns = ['r_in','r_out','w_in','w_out'];                    

    $scope.teacher_types = ['GenEd','DEC','Lift','AC/MH','Indep']
    $scope.teacher_classes = {'GenEd':'','DEC':'DEC','Lift':'Lift','AC/MH':'ACMH','Indep':'Indep'};
    
    $scope.goStudent = function(studentId) {
        $location.path("/classes/"+klass.id+"/students/"+studentId);
    }
    
}
klass.$inject = ['$scope','$filter','Klass','$routeParams','$location'];


function klass_student($scope) {

    $scope.header_map = [{"key":"sep_id","value":"SepID"},
                         {"key":"last_name","value":"Last Name"},
                         {"key":"first_name","value":'First Name'},
                         {"key":"dec","value":'DEC'},
                         {"key":"parents_name","value":"Parent's Name"},
                         {"key":"grade","value":"Gr"},
                         {"key":"phone","value":"Phone #"},
                         {"key":"r_in","value":"R in"},
                         {"key":"w_in","value":"W in"},
                         {"key":"r_out","value":"R out"},
                         {"key":"w_out","value":"W out"}];

    $scope.status_map = [
        {'key':"enr","long_name":"Enrolled","short_name":"Enr"},
        {'key':"wd","long_name":"Withdrawn","short_name":"WD"},
        {'key':"adm","long_name":"Admitted","short_name":"Adm"}
    ] 

    $scope.score_columns = ['r_in','r_out','w_in','w_out'];
    $scope.teacher_types = ['GenEd','DEC','Lift','AC/MH','Indep']
    $scope.teacher_classes = {'GenEd':'','DEC':'DEC','Lift':'Lift','AC/MH':'ACMH','Indep':'Indep'};

    $scope.klass = {
        "id":1,
        "name":"Class 1",
        "date":"01/11/2012"};

    $scope.student = {"id":1,"first_name":"Justin","last_name":"Gray","sep_id":10001,"dec":true,
         "parents_name":"Scott Gray","grade":11,"phone":"216-773-0000",
         "r_in":400,"w_in":0,"r_out":"FE200","w_out":0,"notes":"xxxx"};

        

    $scope.klass_data = {"status":"enr","p1":true,"p2":false,
        "teacher":"GenEd",
        "notes":[{"class":{"id":1,
                           "name":"Class 1",
                           "date":"01/11/2012"},
                  "id":1,"date_time":"XXXX","note":"XXXXXXXXXXXXXXX"},
                 {"class":{"id":1,
                           "name":"Class 1",
                           "date":"01/11/2012"},
                  "id":2,"date_time":"XXXX","note":"XXXXXXXXXXXXXXX"},
                 {"class":{"id":2,
                  "name":"Class 2",
                  "date":"01/11/2011"},
                  "id":3,"date_time":"XXXX","note":"XXXXXXXXXXXXXXX"}
                 ]};

    $scope.add_note = function(text) {
        var note = {
            "class":$scope.klass,
            "date_time": new Date(),
            "note":text
        }
        $scope.klass_data.notes.push(note);
    }             


}
klass_student.$inject = ['$scope'];


