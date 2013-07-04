


function initmap() {
	// set up the map
	var map = L.map('mapHolder').setView([51.505, -0.09], 0);
	L.tileLayer('http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
		/*'http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png'*/
	    maxZoom: 18
	}).addTo(map);
}