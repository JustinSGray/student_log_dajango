'use strict';

/* Filters */

angular.module('studentLog.filters', []).
  filter('interpolate', ['version', function(version) {
    return function(text) {
      return String(text).replace(/\%VERSION\%/mg, version);
    }
  }]).
  filter('checkbox', function(){
    return function(input){
        return input ? "YES" : "NO";
    }
  });
