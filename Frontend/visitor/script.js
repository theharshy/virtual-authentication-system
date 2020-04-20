const otp = document.getElementById('otp')
const form = document.getElementById('form')
const errorElement = document.getElementById('error')
const page2 = document.getElementById('access')
var apigClient = apigClientFactory.newClient();

form.addEventListener('submit', (e) => {
  let messages = []
  if (otp.value === '' || otp.value == null) {
    messages.push('OTP is required')
  }
  if (messages.length > 0) {
    e.preventDefault()
    errorElement.innerText = messages.join(', ')
  }

  else
  {
  	e.preventDefault()
	  body = {
	    "otp" : (otp.value)
	  };
	  console.log(body);
	  apigClient.rootPost({}, body, {})
	    .then(function(result){
	      console.log(result);
	      if (result.data.statusCode == "404"){
	      	text = "OTP is invalid";
	      	errorElement.innerText = text;
	      }
	      else{
	      	errorElement.innerText = result.data.body
	      }
	      
	    }).catch( function(result){
	      console.log(result);
	      text = "Request Failure. Please try again!";
	      errorElement.innerText = text;
	      });

	}

})