

window.onload = function() {
  var userid = getUrlVars()["userid"];
var image_url = "https://b1photos.s3.amazonaws.com/" + userid + ".jpg"

  document.getElementById('image2').src = image_url;

};

form.addEventListener('submit', (e) =>  {
  var x, text;

  n = name.value;
  p = phone.value;

  var apigClient = apigClientFactory.newClient();

  body = {
      'name' : name,
      'phone' : phone
    };



  // if Input is valid
  apigClient.owneractionPost({}, body, {})
      .then(function(result){
        console.log(result);
        errorElement.innerText = "Access Granted!"
        
      }).catch( function(result){
        console.log(result);
        r=false;
        text = "Input is not valid";
        errorElement.innerText = text;
        return false;
        });

});