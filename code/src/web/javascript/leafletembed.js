


function initmap() {
	// set up the map
	var map = L.map('mapHolder').setView([51.505, -0.09], 0);
	
	L.tileLayer('http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
		/*'http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png'*/
	    maxZoom: 18
	}).addTo(map);
	var heatmap = L.tileLayer('http://superfluous.imqs.co.za/omicron/request_handler?function=heat_map&platforms=twitter&tags=%23food&location_type=radius&location=33_50_50000&directory=/{z}/{x}/{y}', {
		
	    maxZoom: 18
	});
	L.control.layers(null,{"Heat map":heatmap}).addTo(map);	

}