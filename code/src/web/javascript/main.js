/**
 * 
 */
function initmap(input,bool,search_id) {
//	alert(input)
//	input = '?function=heat_map&platforms=twitter&tags=%23IMQS&location_type=radius&location=-33.964818_18.8372568_50000'
	// set up the map
	if(bool == true){
		console.log("Returning already setup");
		return;
	}
	var loader = document.getElementsByTagName("img");
	loader[0].style = "display:none";
	var map = L.map('mapHolder').setView([ 51.505, -0.09 ], 0);
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
			callback(callback_params,boolean,search_id);
			boolean = true;
		}

	}
	console.log("Opening port");
//	request.setRequestHeader("Content-length", 1);
	request.open("GET", "http://superfluous.imqs.co.za/omicron/request_search_id"+request_params);
	request.send();
}
/**
 * 
 */
function OnRun() {
	var input = window.location.search;
//	alert("Starting");
//	var input = "?function=heat_map&platforms=twitter&tags=%23IMQS&location_type=radius&location=-33.964818_18.8372568_50000" 
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
	database_request(initmap,input+"&auth_codes="+twitter,input);
	console.log(input+"&authcodes="+twitter);
	console.log("Completed ");
}
