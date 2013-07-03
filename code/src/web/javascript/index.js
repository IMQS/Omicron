/*	don't actually need js for index
	storage of authentication code for this session only !!
 */

/**
 * REST call to get an Authentication for Twitter returns access token
 */
function request_Authentication() {
	var url = "http://host/path/to/resource";
	var representationOfDesiredState = "The cheese is old and moldy, where is the bathroom?";
	var client = new XMLHttpRequest();
	client.open("POST", url, false);
	client.setRequestHeader("Content-Type", "text/plain");
	client.send(representationOfDesiredState);
	if (client.status == 200)
		alert("The request succeeded!\n\nThe response representation was:\n\n"+ client.responseText)
	else
		alert("The request did not succeed!\n\nThe response status was: "+ client.status + " " + client.statusText + ".");
	store_codes(access_token)
}
/**
 * Used to store access token in the web storage only stores twitter access token 
 * @param twitter_access_token: twitters access token to be stored in the browser for the session
 * @param override: if true, will forcible store the access token overriding any previous tokens
 */
function store_codes(twitter_access_token,override) {
	document.getElementById("result").innerHTML = "Sorry.";
	if (typeof (Storage) !== "undefined") {
		if(override){
			sessionStorage.twitter_authentication_code = twitter_access_token;
			
		} else if (!sessionStorage.twitter_authentication_code) {
			// sessionStorage.twitter_authentication_code=authenticate();
			sessionStorage.twitter_authentication_code = twitter_access_token;
			document.getElementById("result").innerHTML = "New Auth code stored";
		} else {
			document.getElementById("result").innerHTML = sessionStorage.twitter_authentication_code +" is the previous code";
		}
	} else {
		document.getElementById("result").innerHTML = "Cant store things";
	}
}
/**
 * First thing to run on the index page to check its authentication for the search engine
 */
function OnRun(){
	var check = check_authentication()
	if(check == false) {
		return "Unsupported Browser"
	} else if(check == true) {
		//Authenticated and ready
	}
	
}
/**
 * 
 * @returns False: if the browser can't support web storage 
 */
function check_authentication(){
	if (typeof (Storage) !== "undefined") {
		if (!sessionStorage.twitter_authentication_code) {
			request_authentication();
			return true;
		} else {
			var access = sessionStorage.twitter_authentication_code;
			if(validate_access_token() == false) {
				request_authentication();
				return true;
			} else {
				return true;
			}
		}
	} else {
		alert("Can't store Access_tokens due to browser support");
		return false
	}
}
/**
 * Validates access token
 * TODO validate the access_token somehow, no method with the twitter api to tell if access token is expired without doing a manuel request and get rejected
 * @returns false: If the token is expired. 
 */
function validate_access_token(){
	return false
}