'use strict';


// Declare app level module which depends on filters, and services
var app = angular.module('studentLog', ['studentLog.filters', 'studentLog.services', 'studentLog.directives']).
  config(['$routeProvider', function($routeProvider) {
    $routeProvider.when('/classes', {templateUrl: 'partials/classes.html', controller: klasses});
    $routeProvider.when('/classes/:classId', {templateUrl: 'partials/class.html', controller:klass});
    $routeProvider.when('/classes/:classId/students/:studentId',{templateUrl: 'Partials/class_student.html',controller:klass_student})
    $routeProvider.otherwise({redirectTo: '/classes'});
  }]);

  app.run(function($rootScope) {
    $rootScope.alert = function(text) {
      alert(text);
    };

    $rootScope.app_root = "/student_log";

    $rootScope.header_map = [{"key":"sep_id","value":"SepID"},
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

    $rootScope.status_map = [
        {'key':"enr","long_name":"Enrolled","short_name":"Enr"},
        {'key':"wd","long_name":"Withdrawn","short_name":"WD"},
        {'key':"adm","long_name":"Admitted","short_name":"Adm"}
    ]                       
  });