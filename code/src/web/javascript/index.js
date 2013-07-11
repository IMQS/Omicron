/*	 
	storage of authentication code for this session only !!
 */
/**
 * This checks the fields have been filled in before filling in the hidden fields with the data to format it correctly for the REST call
 * @returns true: if all the correct fields have been submitted
 * @returns false: any one of the required fields have not been entered
 */
function OnSubmit() {
	//parameters to submit
	var tags = document.getElementsByName("tags")[0];
	var platforms = document.getElementsByName("platforms")[0];
	var location = document.getElementsByName("location")[0];
	var location_type = document.getElementsByName("location_type")[0];
	var func = document.getElementsByName("function")[0];
	
	//local parameters
	var locationtype = document.getElementById("location_type_details");
	var search = document.getElementById("tags");
	var long = document.getElementById("longitude");
	var lat = document.getElementById("latitude");
	var area_radius = document.getElementById("radius_area");
	

	//temp storage
	var parameters = "";
	
	console.log("OnSubmit");
	
	console.log("search element");
	console.log(search.value);
	//separates the search string by underscores for each component
	if (search.value == "" || search.value == null){
		return false;
	} else {
		var array = search.value.split(" ");
		console.log(array.length);
		parameters=parameters+array[0];
		for(var i = 1;i< array.length;i++){
			parameters = parameters +"_"+array[i];
			
		}
		tags.value = parameters;			//set it back into the hidden input
	}
	
	
	parameters = "";
	//sets the location type and area or GPS coordinates
	console.log("locationtype element");
	console.log(locationtype.value);
	if(locationtype.value =="Region"){
		location_type.value = "area"
		if (area_radius.value == "" || area_radius.value == null){
			console.log("area not specified also not implemented");
			return false;
		}else {
			location.value = area_radius.value
		}
		
	} else if(locationtype.value == "Circle") {
		
		location_type.value = "radius"; 


		console.log("long element");
		console.log(long.value);
		if (long.value == "" || long.value == null)
			return false;

		console.log("lat element");
		console.log(lat.value);
		if (lat.value == "" || lat.value == null)
			return false;
		

		console.log("radius element");
		console.log(area_radius.value);
		if (area_radius.value == "" || area_radius.value == null)
			return false;
		location.value = long.value+"_"+lat.value+"_"+area_radius.value
	}
	
	parameters = "";
	//Sets the function heat map or point map to the hidden func variable (from visible Function variable)
	var Function = document.getElementById("function");
	console.log("Function element");
	console.log(Function.value);
	if (Function.value == "" || Function.value == null)
		return false;
	if(Function.value == "Heat Map"){
		func.value = "heat_map";
	} else if(Function.value == "Point Map") {
		func.value="point_map";
	}
	
	//concatinates the strings separated by underscores of the platform names
	var platform = document.getElementsByName("platform");
	console.log("platform element");
	console.log(platform);
	var checkedplatform = null;
	var boolean = false;
	for ( var i = 0; i < platform.length; i++) {
		if (platform[i].checked) {
			if (checkedplatform == null) {
				if (platform[i].value == "instagram") {
					checkedplatform = platform[i].value;
					boolean = true;
					platform[i].disabled = true;
					console.log("disabled instagram");
				} else if (platform[i].value == "twitter") {
					checkedplatform = platform[i].value;
					boolean = true;
					console.log("disabled twitter");
					platform[i].disabled = true;
				}
			} else {
				if (platform[i].value == "instagram") {
					checkedplatform = platform[i].value + "_" + checkedplatform;
					platform[i].disabled = true;
				} else if (platform[i].value == "twitter") {
					checkedplatform = platform[i].value + "_" + checkedplatform;
					platform[i].disabled = true;
				}
			}
		}
	}
	if(boolean == false){
		console.log("No platform selected")
		return false;
	}
	if (checkedplatform == null) {
		console.log("No platform checked");
		return false;
	}

	platforms.value = checkedplatform;
/*	var form = document.getElementById("form");
	form.action = "http://superfluous.imqs.co.za/omicron/main.html"+parameters;
	console.log(form);
*/
	return true;
}
/**
 * REST call to get an Authentication for Twitter returns access token
 * @param url: URL for the REST call, String
 * @param callback: Function pointer to execute after the REST call has completed
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
	document.getElementById("result").innerHTML = "Attempting to Authorise";
	if (typeof (Storage) !== "undefined") {
		if (override) {
			sessionStorage.twitter_authentication_code = twitter_access_token;
		} else if (!sessionStorage.twitter_authentication_code) {
			// sessionStorage.twitter_authentication_code=authenticate();
			sessionStorage.twitter_authentication_code = twitter_access_token;
			document.getElementById("result").innerHTML = "Successfully Authorised";
		} else {
			document.getElementById("result").innerHTML = sessionStorage.twitter_authentication_code
					+ " is the previous code";
		}
	} else {
		document.getElementById("result").innerHTML = "Authentication failed";
		sessionStorage.twitter_authentication_code = "Disabled"
	}
}
/**
 * First thing to run on the index page to check its authentication for the
 * search engine
 */
function OnRun() {
	var check = check_authentication();
	console.log("Checked Authentication");
	/* alert("Checked"); */
	if (check == false) {
		return "Unsupported Browser";
	} else {
		console.log("Authenticated and Ready to request");
		EnableButtons();
	}

}
function EnableButtons(){
	var forms = document.getElementsByTagName("form");
	for(var i = 0;i<forms.length;i++){
		for(var j = 0 ; j < forms[i].length;j++){
			if(forms[i][j].type=="submit"){
				console.log(forms[i][j].value)
				forms[i][j].disabled = true;
			}
		}
	}
}
/**
 * Checks authentication, if there is a valid access token available
 * @returns true: If it attempts to get a new code, or find an old valid code
 * @returns false: if the browser can't support web storage
 */
function check_authentication() {
	if (typeof (Storage) !== "undefined") {
		if (!sessionStorage.twitter_authentication_code) {
			console
					.log("Requesting Omicron access code, New auth codes needed");
			httpRequest('http://superfluous.imqs.co.za/omicron/authorise',
					store_codes, true);

			return true;
		} else {
			var access = sessionStorage.twitter_authentication_code;
			if (validate_access_token() == false) {
				console
						.log("Requesting Omicron access code, found invalid token");
				httpRequest('http://superfluous.imqs.co.za/omicron/authorise',
						store_codes, true);
				return true;
			} else {
				document.getElementById("result").innerHTML =  "Authenticated, previous code";
				return true;
			}
		}
	} else {
		alert("Can't store Access_tokens due to browser support");
		sessionStorage.twitter_authentication_code = "Disabled"
		return false;
	}
}
/**
 * Validates access token TODO validate the access_token somehow, no method with
 * the twitter api to tell if access token is expired without doing a manuel
 * request and get rejected
 * @returns true: If its a valid token.
 * @returns false: If the token is expired.
 */
function validate_access_token() {
	return true;
}