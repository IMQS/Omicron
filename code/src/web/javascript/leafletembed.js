var map;
var ajaxRequest;
var plotlist;
var plotlayers=[];

function initmap() {
	// set up the map
	var map = L.map('mapHolder').setView([51.505, -0.09], 13);
	L.tileLayer('http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
	    maxZoom: 18
	}).addTo(map);
}