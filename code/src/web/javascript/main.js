/**
 * Sets up leaflet and removes the loading gif from the <div>
 * then adds the base maps from open street maps and adds heatmap layer from superfluous.imqs.co.za
 */
function initmap(bool, search_id, geo_point_data) {
	if(bool == true){
		console.log("Returning already setup");
		return;
	}
	var mapholder = document.getElementById('mapHolder')
	mapholder.innerHTML=""
	mapholder.style.borderStyle = 'solid'
	mapholder.style.borderColor = 'rgba(0,0,0,0.1)'
	var map = L.map('mapHolder').setView([ -33, 18 ], 6);
	L.tileLayer('http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
		/* 'http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png' */
		maxZoom : 18
	}).addTo(map);
	var heatmap = L
			.tileLayer(
					'http://superfluous.imqs.co.za/omicron/request_handler?user_id='+search_id+'&directory=/{z}/{x}/{y}.png',
					{
						maxZoom : 18
					});
	
	var geo_points = L.geoJson(JSON.parse(geo_point_data));
	
	L.control.layers(null, {
		"Heat map" : heatmap,
		"Points":geo_points
	}).addTo(map);	
}
/**
 * Makes a request to the superfluous.imqs.co.za database that stores the query and gets a user id back which is use to uniquly identify the query
 * @param callback : function pointer to the function that must be called after the http request has completed
 * @param request_params : the http request parameters
 * @param callback_params : the parameters for the call back function
 */
function database_request(callback, request_params) // How can I use this callback?
{
	var request = new XMLHttpRequest();
	var boolean = false;
	request.onreadystatechange = function() {
		if (request.readyState != 4) {
			return; // Another callback here

		}
		if (request.status != 200) {
			return;
		}

		var search_id = request.responseText
		console.log(search_id);

//		boolean = true;
		console.log("checking");
		if(request.readyState == 4 && request.status==200){
			console.log("Pushing call back");
			callback(initmap,boolean,search_id);
			boolean = true;
		}

	}
	console.log("Opening port");
	request.open("GET", "http://superfluous.imqs.co.za/omicron/request_search_id"+request_params);
	request.send();
}
/**
 * First and only function thats called from the html document, checks if there is an twitter access token for this session 
 * and makes the first REST call to the database on superfluous to request a user id (search id) that will be used to uniquely identify the 
 * query
 */
function OnRun() {
	var input = window.location.search; 
	var twitter = "Disabled";
	if (typeof (Storage) !== "undefined") {
		if (sessionStorage.twitter_authentication_code) {
			twitter = "{'twitter':'" +sessionStorage.twitter_authentication_code+"'}";
		}
	} else {
		document.getElementById("result").innerHTML = "Storage Failed";
	}

	if(twitter=="Disabled"){
		alert("Please go to the main page to get authenticated ")
	}
	twitter = encodeURIComponent(twitter)
	database_request(geo_point_request,input+"&auth_codes="+twitter);
	console.log(input+"&authcodes="+twitter);
	console.log("Completed ");
}

/**
 * 
 */
function geo_point_request(callback, bool, search_id) // How can I use this callback?
{
	var request = new XMLHttpRequest();
	var boolean = false;
	if (bool == true) { 
		return;
	}
	request.onreadystatechange = function() {
		if (request.readyState != 4) {
			return; // Another callback here

		}
		if (request.status != 200) {
			return;
		}

		var geo_data = request.responseText
		console.log(geo_data);

//		boolean = true;
		console.log("checking");
		if(request.readyState == 4 && request.status==200){
			console.log("Pushing call back");
			callback(boolean, search_id, geo_data);
			boolean = true;
		}

	}
	console.log("Opening port");
	request.open("GET", "http://superfluous.imqs.co.za/omicron/request_handler?user_id="+search_id+"&function=geo_coords");
	request.send();
}