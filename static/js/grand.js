function check_session() {
  return new Promise(function(resolve, reject){
    fetch('/check_session', {method: "GET", credentials: "include"})
    .then(function(resp){ return resp.json() })
    .then(function(json){ return resolve(json); })
    .catch(function(err){ return reject(error) })
  });
}

function validateUsername(username) {
  var re = /^[a-z0-9\-\_\.]{3,}$/;
  return re.test(username.toLowerCase());
}

function validateEmail(email) {
  var re = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
  return re.test(email.toLowerCase());
}

function validatePassword(password) {
  var re = /^[a-zA-Z0-9\-\_\.\!\@\#\$\%\&\?]{7,}$/;
  return re.test(password);
}

function headers_json() {
  let myHeaders = new Headers();
  myHeaders.append("Content-Type", "application/json; charset=UTF-8");
  myHeaders.append("Accept", "application/json");
  return myHeaders;
}

function disable_buttons() {
  $('button.btn').addClass("disabled");
}
function enable_buttons() {
  $('button.btn').removeClass("disabled");
}

function get_random_travels() {
  return new Promise(function(resolve, reject){
    fetch('/get/travels/random', {method: "GET", credentials: "include"})
    .then(function(resp){ return resp.json() })
    .then(function(json){ return resolve(json); })
    .catch(function(err){ return reject(error) })
  });
}

function get_user_travels(travel_ids = []) {
  return new Promise(function(resolve, reject){
    var params = {
      method: "PUT",
      credentials: "include",
      header: headers_json(),
      body: JSON.stringify({travel_ids: travel_ids})
    }

    fetch('/get/travels/random', params)
    .then(function(resp){ return resp.json() })
    .then(function(json){ return resolve(json); })
    .catch(function(err){ return reject(error) })
  });
}
