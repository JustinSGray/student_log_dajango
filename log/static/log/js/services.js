'use strict';

/* Services */


// Demonstrate how to register services
// In this case it is a simple value service.
angular.module('studentLog.services', ['ngResource']).
    factory('Klass',function($resource){
        return $resource('tmp_data/classes/:classId.json', {}, 
                         {query: {method:'GET', params:{classId:'classes'}, isArray:true}}
                        );

})
.value('version', '0.1');
