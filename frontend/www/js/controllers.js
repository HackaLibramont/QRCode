angular.module('starter.controllers', ['ngResource', 'ngCookies', 'leaflet-directive', 'geolocation'])
.run(function($cookies)
{
	$cookies.lang = navigator.language;
})
.factory('poiService', function ($resource,$http, $cookies) {
    var cookie = $cookies.lang; // suppose you already set $cookies.myCookie= 'xxx';
	$http.defaults.headers.post.Cookies = cookie;
	return $resource('http://172.16.115.130:8000/poi/:poiId', {poiId : '@id'});
})
.factory('trailService', function ($resource,$http, $cookies) {
    var cookie = $cookies.lang; // suppose you already set $cookies.myCookie= 'xxx';
	$http.defaults.headers.post.Cookies = cookie;
	return $resource('http://172.16.115.130:8000/trail/:trailId', {trailId : '@id'});
})

.controller('AppCtrl', function($scope, $ionicModal, $timeout, $cookies) {
  console.log($cookies.lang);
  $scope.switchLang = function(lang)
  {
	  $cookies.lang = lang;
  };
})

.controller('ParcourCtrl', function($scope, $stateParams, poiService ) {
	console.log($stateParams.parcoursId);
	$scope.centers = {};
	var parcour = poiService.get({poiId: $stateParams.parcoursId});
	
	parcour.$promise.then(function(data) {
       $scope.parcour = data;
	   console.log(JSON.stringify(data));
	   angular.extend($scope, {
			centers: {
				lat: $scope.parcour.latitude,
				lng: $scope.parcour.longitude,
				zoom: 15
			},
			markers: {
				poiMarker: {
					lat: $scope.parcour.latitude,
					lng: $scope.parcour.longitude,           
					message: $scope.parcour.name,
					focus: true,
					draggable: false
				}				
			},
			defaults: {
				scrollWheelZoom: false
			}
	});	
   });
})

.controller('TrailsCtrl', function($scope, $stateParams, trailService ) {
	var trails = trailService.query();
	
	$scope.trails = trails;   
})
.controller('TrailCtrl', function($scope, $stateParams, trailService, geolocation ) {
	 
	$scope.centers = {};
	var trail = trailService.get({trailId: $stateParams.trailId});
	
	
	trail.$promise.then(function(data) {
		$scope.trail = data;
	 
		   angular.extend($scope, {
				centers: {
					lat: $scope.trail.pois[0].latitude,
					lng: $scope.trail.pois[0].longitude,
					zoom: 15
				},
				markers : genMarkers(data),
				defaults: {
					scrollWheelZoom: false
				}
		   });
		});
  
  
   
   function genMarkers(trail)
   {
	   var arrayMarker = []; 
	   for(var i = 0; i < trail.pois.length; i++)
	   {		   
			var oPoi = trail.pois[i];
			arrayMarker[oPoi.id] = {
					lat: oPoi.latitude,
					lng: oPoi.longitude,           
					message: '<br/><a href="/#/app/parcours/'+oPoi.id+'">'+oPoi.name+'</a>',
					focus: true,
					draggable: false		   
		   };
			
	   }
	  return arrayMarker;
   }
})

.controller('ParcoursCtrl', function($scope, poiService) {
	
	$scope.parcours = poiService.query();

	$scope.onSwipeRight = function()
	{ 

	}

	$scope.onSwipeLeft = function()
	{ 

	}
  
})
.controller('ParcoursDescriptionCtrl', function($scope, poiService) {
	
	$scope.parcoursDescription = poiService.get({poiId: $stateParams.parcoursId});

});
