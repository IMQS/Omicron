
function initmap() {
	// set up the map
	var map = L.map('mapHolder').setView([ 51.505, -0.09 ], 0);
	L.tileLayer('http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
		/* 'http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png' */
		maxZoom : 18
	}).addTo(map);
	var heatmap = L
			.tileLayer(
					'http://superfluous.imqs.co.za/omicron/request_handler?function=heat_map&platforms=twitter&tags=%23IMQS&location_type=radius&location=-33.964818_18.8372568_50000&directory=/{z}/{x}/{y}.png',
					{
						maxZoom : 18
					});
	L.control.layers(null, {
		"Heat map" : heatmap
	}).addTo(map);

}
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
	
}
function OnRun() {
	var input = get_input();
	process_input(input);
	initmap();
}
