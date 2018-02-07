(function(){

  /*
    Welcome Controller

    Built With Knockout JS
    http://knockoutjs.com/
  */

  function MVC() {
    var self = this;
    window.logMVC = function() { console.log('mvc: ', self); }

    self.signed_in = ko.observable(false);

    self.reveal_guest_nav_links = function() {
      $('nav#navigation-bar').find('ul#nav-mobile').append('<li><a title="Sign In" href="/signin">Sign In</a></li>');
      $('nav#navigation-bar').find('ul#nav-mobile').append('<li><a title="Sign Up" href="/signup">Sign Up</a></li>');
    }
    self.reveal_user_nav_links = function() {
      $('nav#navigation-bar').find('ul#nav-mobile').append('<li><a title="Home" href="/home">Home</a></li>');
      $('nav#navigation-bar').find('ul#nav-mobile').append('<li><a title="Sign Out" href="/signout">Sign Out</a></li>');
    }

    self.check_session = function() {
      check_session()
      .then(function(resp){
        console.log(resp);
        self.signed_in(resp.online);

        if(resp.online === true) {
          self.user = resp.user;
          Object.keys(resp.user).forEach(function(key){
            self[key] = ko.observable(resp.user[key]);
          });

          self.reveal_user_nav_links();
        }
        else {
          self.reveal_guest_nav_links();
        }
      })
    }; self.check_session();

  }

  // initialize controller
  ko.applyBindings(new MVC());
  console.log('welcome controller initialized!');

})()
