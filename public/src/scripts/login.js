// initialize Account Kit with CSRF protection
AccountKit_OnInteractive = function(){
AccountKit.init(
  {
    appId:1058850810852691,
    state:"{{xsrf}}",
    version:"v1.0"
  }
);
};

// login callback
function loginCallback(response) {
console.log(response);
if (response.status === "PARTIALLY_AUTHENTICATED") {
  document.getElementById("code").value = response.code;
  document.getElementById("xsrf").value = response.state;
  document.getElementById("fb_accountkit_login").submit();
}
else if (response.status === "NOT_AUTHENTICATED") {
    document.getElementsByClassName('alert').innerHtml = 'Authentication Issue';
    document.getElementsByClassName('alert').style.display = 'block';
    document.getElementsByClassName('alert').className += 'alert-danger';
}
else if (response.status === "BAD_PARAMS") {
    document.getElementsByClassName('alert').innerHtml = 'Bad Params';
    document.getElementsByClassName('alert').style.display = 'block';
    document.getElementsByClassName('alert').className += 'alert-warning';
}
}

// phone form submission handler
function phone_btn_onclick() {
AccountKit.login('PHONE',
    {},
    loginCallback);
}

function email_btn_click() {
    document.getElementById("email_login").submit();
}
