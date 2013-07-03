/*	don't actually need js for index
	storage of authentication code for this session only !!
*/
function store_codes(){
	if(typeof(Storage)!=="undefined")
	  {
	  if (!sessionStorage.twitter_authentication_code)
	    {
	    sessionStorage.twitter_authentication_code="This is an authentication code"
	    }
	  else
	    {
		  
	    }
	  document.getElementById("result").innerHTML="You have clicked the button " + sessionStorage.clickcount + " time(s) in this session.";
	  }
	else
	  {
	  document.getElementById("result").innerHTML="Sorry, your browser does not support web storage...";
	  }
	}
}