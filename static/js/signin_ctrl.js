(function(){

  /*
    Sign In Controller

    Built With Knockout JS
    http://knockoutjs.com/
  */

  function MVC() {
    var self = this;
    window.logMVC = function() { console.log('mvc: ', self); }

    self.uniqueValue = function() {
      return String(Date.now()) + Math.random().toString(36).substr(2, 34);
    }

    self.reveal_guest_nav_links = function() {
      $('nav#navigation-bar').find('ul#nav-mobile').append('<li><a title="Sign In" href="/signin">Sign In</a></li>');
      $('nav#navigation-bar').find('ul#nav-mobile').append('<li><a title="Sign Up" href="/signup">Sign Up</a></li>');
    }
    self.reveal_user_nav_links = function() {
      $('nav#navigation-bar').find('ul#nav-mobile').append('<li><a title="Home" href="/home">Home</a></li>');
      $('nav#navigation-bar').find('ul#nav-mobile').append('<li><a title="Sign Out" href="/signout">Sign Out</a></li>');
    }

    //

    self.sign_in = function() {
      var sign_in_email              = $('#sign_in_email').val();
      var sign_in_password           = $('#sign_in_password').val();

      if(!validateEmail(sign_in_email)) {
        alert('email is in bad format.');
        return;
      }
      if(!validatePassword(sign_in_password)) {
        alert('passwords must be: \n\n \
        letters and/or numbers (dashes, periods, underscores, special characters are allowed)\n \
        minimum of 7 characters.');
        return;
      }

      disable_buttons();

      var params = {
        method: "PUT",
        credentials: "include",
        body: JSON.stringify({
          email: sign_in_email,
          password: sign_in_password
        }),
        headers: headers_json()
      }

      fetch('/signin', params)
      .then(function(resp){ enable_buttons(); return resp.json() })
      .then(function(json){
        console.log(json);
        alert(json.message);
        if(!json.error) {
          window.location.href = '/';
        }
      })
    }

  }

  // initialize controller
  ko.applyBindings(new MVC());
  console.log('sign in controller initialized!');

})()
