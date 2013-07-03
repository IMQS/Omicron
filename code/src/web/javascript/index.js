/*	don't actually need js for index
	storage of authentication code for this session only !!
 */
function httprequest() {
	var url = "http://host/path/to/resource";
	var representationOfDesiredState = "The cheese is old and moldy, where is the bathroom?";
	
	var client = new XMLHttpRequest();

	client.open("POST", url, false);

	client.setRequestHeader("Content-Type", "text/plain");

	client.send(representationOfDesiredState);

	if (client.status == 200)
		alert("The request succeeded!\n\nThe response representation was:\n\n"
				+ client.responseText)
	else
		alert("The request did not succeed!\n\nThe response status was: "
				+ client.status + " " + client.statusText + ".");
}

function authenticate() {

	return "Access_Token"
}
function store_codes() {
	document.getElementById("result").innerHTML = "Sorry.";
	if (typeof (Storage) !== "undefined") {
		if (!sessionStorage.twitter_authentication_code) {
			// sessionStorage.twitter_authentication_code=authenticate();
			sessionStorage.twitter_authentication_code = "Authentication code present in storage";
			document.getElementById("result").innerHTML = "New Auth code stored";
		} else {
			document.getElementById("result").innerHTML = sessionStorage.twitter_authentication_code;
		}
	} else {
		document.getElementById("result").innerHTML = "Cant store things";
	}
}