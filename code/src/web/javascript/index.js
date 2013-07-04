/*	 
	storage of authentication code for this session only !!
 */

/**
 * REST call to get an Authentication for Twitter returns access token
 */
function httpRequest(url, callback) // How can I use this callback?
{
	var request = new XMLHttpRequest();
	request.onreadystatechange = function() {
		if (request.readyState != 4) {
			return; // Another callback here

		}
		if (request.status != 200) {
			return;
		}
		callback(request.responseText)

	}
	request.open("GET", url);
	request.send();
}
/**
 * Used to store access token in the web storage only stores twitter access
 * token
 * 
 * @param twitter_access_token:
 *            twitters access token to be stored in the browser for the session
 * @param override:
 *            if true, will forcible store the access token overriding any
 *            previous tokens
 */
function store_codes(twitter_access_token, override) {
	document.getElementById("result").innerHTML = "Sorry.";
	alert(twitter_access_token);
	if (typeof (Storage) !== "undefined") {
		if (override) {
			sessionStorage.twitter_authentication_code = twitter_access_token;

		} else if (!sessionStorage.twitter_authentication_code) {
			// sessionStorage.twitter_authentication_code=authenticate();
			sessionStorage.twitter_authentication_code = twitter_access_token;
			document.getElementById("result").innerHTML = "New Auth code stored" + twitter_access_token;
		} else {
			document.getElementById("result").innerHTML = sessionStorage.twitter_authentication_code
					+ " is the previous code";
		}
	} else {
		document.getElementById("result").innerHTML = "Cant store things";
	}
}
/**
 * First thing to run on the index page to check its authentication for the
 * search engine
 */
function OnRun() {


	var check = check_authentication();
	alert("Checked");
	if (check == false) {
		return "Unsupported Browser";
	}

}
/**
 * 
 * @returns False: if the browser can't support web storage
 */
function check_authentication() {
	if (typeof (Storage) !== "undefined") {
		if (!sessionStorage.twitter_authentication_code) {
			alert("REQUESTING1 done");
			httpRequest('http://superfluous.imqs.co.za/omicron/authorise', store_codes,true);

			return true;
		} else {
			var access = sessionStorage.twitter_authentication_code;
			if (validate_access_token() == false) {
				alert("REQUESTING2");
				httpRequest('http://superfluous.imqs.co.za/omicron/authorise', store_codes,true);
				return true;
			} else {
				document.getElementById("result").innerHTML = sessionStorage.twitter_authentication_code + " is the previous code";
				return true;
			}
		}
	} else {
		alert("Can't store Access_tokens due to browser support");
		return false;
	}
}
/**
 * Validates access token TODO validate the access_token somehow, no method with
 * the twitter api to tell if access token is expired without doing a manuel
 * request and get rejected
 * 
 * @returns false: If the token is expired.
 */
function validate_access_token() {
	return true;
}