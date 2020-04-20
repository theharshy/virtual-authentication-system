function validate() {
  var x, text, r;

  x = otp.value;

  var apigClient = apigClientFactory.newClient();

  // if OTP is valid
  console.log(body);

  apigClient.rootPost({}, body, {})
    .then(function(result){
      console.log(result);
      display(true);

    }).catch( function(result){
      console.log(result);
      r=false;
      text = "OTP is not valid";
      errorElement.innerText = text;
      display(false);
      });
}
