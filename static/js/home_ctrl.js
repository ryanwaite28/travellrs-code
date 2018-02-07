(function(){

  /*
    Home Controller

    Built With Knockout JS
    http://knockoutjs.com/
  */

  function MVC() {
    var self = this;
    window.logMVC = function() { console.log('mvc: ', self); }

    self.signed_in = ko.observable(false);

    self.travelsObj = {};
    self.travelsList = ko.observableArray([]);
    self.travelsMarkers = {};


    self.create_travel_caption = ko.observable('');

    $(document).ready(function() {
      self.manage = window.manage;

      setTimeout(() => {
        self.get_your_travels();
      }, 3750);

      //

      $('#zoom-icon').click(() => { manage.map.setZoom(5); });
      $('#frm-icon').click(() => {
        $("div#activity-overlay").removeClass("ghost");

        Object.keys(self.travelsMarkers).forEach(key => {
          var marker = self.travelsMarkers[key].marker;
          marker.setMap(null);
        })

        self.get_your_travels();
      });

    });

    self.unique_value = function() {
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

    //

    self.get_your_travels = function() {
      $("#glyph-contain").removeClass("ghost");

      get_your_travels()
      .then(resp => {
        console.log(resp);

        $("div#activity-overlay").addClass("ghost");
        if(resp.error) {
          alert(resp.message);
          return;
        }

        self.travelsObj         = {};
        self.travelsList        = ko.observableArray([]);
        self.travelsMarkers     = {};

        self.travelsList(resp.travels);
        resp.travels.forEach(function(){ self.travelsObj[travel.unique_value] = travel });
        self.addMarkers();
      })
      .catch(error => {
        console.log(error);
        alert(error.message)
      });
    }

    self.addMarker = function(travel) {
      var content = '<div class="row"> \
        <div class="col s12"> \
          <p class="text-wrap"><strong>' + travel.location + '</strong></p> \
          <p class="caption-1"> \
            ' + travel.caption + '<br/> \
            <span class="text-grey"> \
              <em>' + date_formatter(travel.date_created) + '</em> \
            </span> \
          </p> \
          <p class="caption-1"> \
            By: ' + travel.owner_rel.username + ' \
          </p> \
        </div> \
      </div>';

      var marker = new google.maps.Marker({
        position: new google.maps.LatLng(travel.lat, travel.lng),
        caption: travel.caption,
        location: travel.location,
        id: travel.place_id,
        animation: google.maps.Animation.DROP,
        map: manage.map
      });

      marker.addListener('click', function() {
        if (marker.getAnimation() !== null) {
          marker.setAnimation(null);
        }
        else {
          marker.setAnimation(google.maps.Animation.BOUNCE);
        }
        setTimeout(function() {
          marker.setAnimation(null)
        }, 1500);
      });

      self.travelsObj[travel.unique_value] = {
        // i know ES6 new syntax features;
        // this is so it works with Internet Explorer's Old Secure Ass!
        marker: marker,
        content: content
      };

      google.maps.event.addListener(marker, 'click', function() {
        manage.infowindow.setContent(content);
        manage.map.setZoom(13);
        manage.map.setCenter(marker.position);
        manage.infowindow.open(manage.map, marker);
        manage.map.panBy(0, -125);
      });
    }

  	self.addMarkers = function() {
      var array = self.travelsList();
  		$.each(array, function(index, travel) {
  			self.addMarker(travel);
  		});

      $(".switch-box").addClass("hide-elem");
      $("#travels-box").removeClass("hide-elem");
      $("#welcome-sidebar").removeClass("ghost");
  	}

    self.showMarker = function(travel) {
      var marker = self.travelsObj[travel.unique_value].marker;
      var content = self.travelsObj[travel.unique_value].content;

      manage.infowindow.setContent(content);
      manage.map.setZoom(13);
      manage.map.setCenter(marker.position);
      manage.infowindow.open(manage.map, marker);
      manage.map.panBy(0, -125);
  	}

    self.makeHTTPS = function(link) {
      if(!link) {
        throw new Error("no argument given...");
      }
      if(link.constructor !== String) {
        throw new Error("argument is not string...");
      }
      if(!/(http|https):\/\/(.*)/.test(link)) {
        throw new Error("argument is not a valid link...");
      }

      let splitter = link.split('://');
      let protocol = splitter[0];
      let domain_path = splitter[1];

      if(protocol == 'http') {
        return 'https' + '://' + domain_path;
      }
      else {
          return link;
      }
    }

    self.showList = function() {
      $(".switch-box").addClass("hide-elem");
      $("#travels-box").removeClass("hide-elem");
      $("#welcome-sidebar").removeClass("ghost");
  	}

    self.create_travel = function() {
      if(!manage.marker.location) {
        var string =  'You must set a location first before adding a travel. Use the search bar at the top to set a location.';
        alert(string);
        $("#welcome-sidebar").addClass("ghost");
        return;
      }

      if(!self.createtravel_title) {
        alert("Post Title is required");
        return;
      }
      if(!self.createtravel_body) {
        alert("Post Body is required");
        return;
      }
      if(self.createtravel_title.trim().length < 7) {
        alert("Post Title requires 7 characters minimum");
        return;
      }
      if(self.createtravel_title.trim().length > 175) {
        alert("Post Title requires 175 characters maximum");
        return;
      }
      if(self.createtravel_body.trim().length < 7) {
        alert("Post Body requires 7 characters minimum");
        return;
      }
      if(self.createtravel_body.trim().length > 175) {
        alert("Post Body requires 175 characters maximum");
        return;
      }

      var form_data = new FormData();
      var file = document.getElementById('create_travel_file').files[0];
      var { location, latitude, longitude, place_id } = manage.marker;

      form_data.append("create_travel_title", self.createtravel_title.trim());
      form_data.append("create_travel_body", self.createtravel_body.trim());

      form_data.append("create_travel_location", location);
      form_data.append("create_travel_place_id", place_id);
      form_data.append("create_travel_latitude", latitude);
      form_data.append("create_travel_longitude", longitude);

      if(file) {
        var accepted_file_types = ['jpg', 'jpeg', 'png', 'gif'];
        var type = file.type.split("/");
        if(type[0] !== "image" || accepted_file_types.indexOf(type[1]) === -1) {
          alert("File must be an image: jpg, png, or gif");
          return;
        }
        else {
          form_data.append("create_travel_file", file);
        }
      }

      var ask = confirm("Create a travel for the location: " + manage.marker.location + "?");
      if(ask === false) { return; }

      // $vault.create_travel(form_data)
      // .then(resp => {
      //   // console.log(resp);
      //   if(!resp.error) {
      //     alert(resp.message);
      //
      //     self.createtravel_title = "";
      //     self.createtravel_body = "";
      //     self.createtravel_link = "";
      //     document.getElementById('createtravel_file').value = "";
      //     document.getElementById('createtravel_filetext').value = "";
      //     self.travelsList.push(resp.travel);
      //     self.travels[resp.travel.unique_value] = resp.travel;
      //     self.addMarker(resp.travel);
      //     self.$apply();
      //
      //     manage.marker.setVisible(false);
      //     manage.marker.clearLocation();
      //     manage.infowindow.close()
      //   }
      // })
      // .catch(error => { alert(error.message) })
  	}

  }

  // initialize controller
  ko.applyBindings(new MVC());
  console.log('welcome controller initialized!');

})()
