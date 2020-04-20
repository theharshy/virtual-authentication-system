function getUrlVars() {
    var vars = {};
    var parts = window.location.href.replace(/[?&]+([^=&]+)=([^&]*)/gi, function(m,key,value) {
        vars[key] = value;
    });
    return vars;
}
var userid = getUrlVars()["userid"];

var image_url = "https://b1photos.s3.amazonaws.com/" + userid + ".jpg"

window.onload = function() {
  var userid = getUrlVars()["userid"];
  document.getElementById('image').src = image_url;

  button.addEventListener("click", (e) =>  {
  var x, text;

  n = name.value;
  p = phone.value;

  var apigClient = apigClientFactory.newClient();

  body = {
      'name' : name.value,
      'phone' : phone.value,
      'file_name': userid
    };


  console.log(body);
  // if Input is valid
  apigClient.owneractionPost({}, body, {})
      .then(function(result){
        console.log(result);
        errorElement.innerText = "New User Created!"
        
      }).catch( function(result){
        console.log(result);
        r=false;
        text = "Input is not valid";
        errorElement.innerText = text;
        return false;
        });

});

};
const name = document.getElementById('name')
const phone = document.getElementById('phone')
const errorElement = document.getElementById('error')
const button = document.getElementById("submit")

if(button){
  button.addEventListener("click", (e) =>  {
  // var x, text;

  // n = name.value;
  // p = phone.value;

  // var apigClient = apigClientFactory.newClient();

  // body = {
  //     'name' : name.value,
  //     'phone' : phone.value
  //   };


  // console.log(body);
  // // if Input is valid
  // apigClient.owneractionPost({}, body, {})
  //     .then(function(result){
  //       console.log(result);
  //       errorElement.innerText = "Access Granted!"
        
  //     }).catch( function(result){
  //       console.log(result);
  //       r=false;
  //       text = "Input is not valid";
  //       errorElement.innerText = text;
  //       return false;
  //       });

});
}