(function(){

  /*
    Sign Up Controller

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

    self.sign_up = function() {
      var sign_up_username           = $('#sign_up_username').val();
      var sign_up_email              = $('#sign_up_email').val();
      var sign_up_email_verify       = $('#sign_up_email_verify').val();
      var sign_up_password           = $('#sign_up_password').val();
      var sign_up_password_verify    = $('#sign_up_password_verify').val();

      if(!validateUsername(sign_up_username)) {
        alert('usernames must be: \n\n \
        letters and/or numbers (dashes, periods, underscores are allowed)\n \
        minimum of 3 characters.');
        return;
      }
      if(!validateEmail(sign_up_email)) {
        alert('email is in bad format.');
        return;
      }
      if(sign_up_email !== sign_up_email_verify) {
        alert('emails do not match');
        return;
      }
      if(!validatePassword(sign_up_password)) {
        alert('passwords must be: \n\n \
        letters and/or numbers (dashes, periods, underscores, special characters are allowed)\n \
        minimum of 7 characters.');
        return;
      }
      if(sign_up_password !== sign_up_password_verify) {
        alert('passwords do not match');
        return;
      }

      disable_buttons();

      var params = {
        method: "POST",
        credentials: "include",
        body: JSON.stringify({
          username: sign_up_username,
          email: sign_up_email,
          password: sign_up_password
        }),
        headers: headers_json()
      }

      fetch('/signup', params)
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
  console.log('sign up controller initialized!');

})()
