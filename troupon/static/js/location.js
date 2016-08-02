    $(document).ready(function() {
      if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(showPosition, showError);
      } else {
        toastr.error("Geolocation is not supported by this browser.");
      }

      function showError(error) {
        errorMsg = "";
        switch (error.code) {
          case error.PERMISSION_DENIED:
            errorMsg = "You have denied Troupon access to your location";
            break;
          case error.POSITION_UNAVAILABLE:
            errorMsg = "Location information is unavailable.";
            break;
          case error.TIMEOUT:
            errorMsg = "The request to get user location timed out.";
            break;
          case error.UNKNOWN_ERROR:
            errorMsg = "An unknown error occurred.";
            break;
        }
        toastr.error(errorMsg);
        deleteCookie();
      }

      function deleteCookie() {
        document.cookie = 'city=; expires=Thu, 01 Jan 1970 00:00:01 GMT;';
        localStorage.removeItem("reload");
      }

      function getKey(callback) {
        var key = "";
        $.ajax({
          type: "GET",
          contentType: "application/json",
          url: "/api/serverkey",
          dataType: "json",
          success: function(data) {
            callback(data);
          },
          error: function(result) {
            toastr.error(result);
          }
        });
        return key;
      }

      function showPosition(position) {
        var key = "";
        getKey(function(result) {
          key = result;
        });
        $.ajax({
          type: "POST",
          contentType: "application/x-www-form-urlencoded; charset=UTF-8",
          url: "https://maps.googleapis.com/maps/api/geocode/json?latlng=" + position.coords.latitude + ',' + position.coords.longitude + '&key=' + key,
          dataType: "json",
          success: function(data) {
            var loc = data['results'][4]['formatted_address'];
            var city = loc.split(',')[0];
            document.cookie = "city='" + city + "'";
            if (!localStorage.reload) {
              localStorage.setItem("reload", "true");
              // window.location.reload();
            }
          },
          error: function(result) {
            toastr.error(result);
          }
        });
      }
    });