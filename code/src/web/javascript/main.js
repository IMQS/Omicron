/**
 * 
 */
function initmap(input) {
//	alert(input)
//	input = '?function=heat_map&platforms=twitter&tags=%23IMQS&location_type=radius&location=-33.964818_18.8372568_50000'
	// set up the map
	var map = L.map('mapHolder').setView([ 51.505, -0.09 ], 0);
	L.tileLayer('http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
		/* 'http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png' */
		maxZoom : 18
	}).addTo(map);
	var heatmap = L
			.tileLayer(
					'http://superfluous.imqs.co.za/omicron/request_handler'+input+'&directory=/{z}/{x}/{y}.png',
					{
						maxZoom : 18
					});
	L.control.layers(null, {
		"Heat map" : heatmap
	}).addTo(map);

}
/*
function get_input() {
	var str = decodeURIComponent(window.location.search);
	var objURL = {};
	str.replace(new RegExp("([^?=&]+)(=([^&]*))?", "g"), function($0, $1, $2,
			$3) {
		objURL[$1] = $3;
	});
	return objURL;
}

function process_input(input) {
	input["location_type"]
}
*/

function database_request(callback,request_params,callback_params) // How can I use this callback?
{
	var request = new XMLHttpRequest();
	request.onreadystatechange = function() {
		if (request.readyState != 4) {
			return; // Another callback here

		}
		if (request.status != 200) {
			return;
		}
		console.log("Pushing call back");
		var search_id = request.responseText
		console.log(search_id);
		callback(callback_params);

	}
	console.log("Opening port");
//	request.setRequestHeader("Content-length", 1);
	request_params = "?query="+encodeURIComponent(request_params.substring(1,request_params.lenght));
	request.open("GET", "http://superfluous.imqs.co.za/omicron/request_search_id"+request_params);
	request.send();
}

function OnRun() {
	var input = window.location.search;
//	alert("Starting");
//	var input = "?function=heat_map&platforms=twitter&tags=%23IMQS&location_type=radius&location=-33.964818_18.8372568_50000" 
	//database_request(initmap,input,input);
	console.log("Completed ");
}
