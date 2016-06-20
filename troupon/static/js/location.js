    $(document).ready(function() {
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(showPosition, showError);
        } else {
            console.log("Geolocation is not supported by this browser.");
        }

        function showError(error) {
            switch (error.code) {
                case error.PERMISSION_DENIED:
                    console.log("User denied the request for Geolocation.")
                    break;
                case error.POSITION_UNAVAILABLE:
                    console.log("Location information is unavailable.")
                    break;
                case error.TIMEOUT:
                    console.log("The request to get user location timed out.")
                    break;
                case error.UNKNOWN_ERROR:
                    console.log("An unknown error occurred.")
                    break;
            }
        }

        function showPosition(position) {
            $.ajax({
                type: "POST",
                /*method type*/
                contentType: "application/json; charset=utf-8",
                url: "https://maps.googleapis.com/maps/api/geocode/json?latlng=" + position.coords.latitude + ',' + position.coords.longitude + '&key=AIzaSyCVSRwHlla02n6Y_sYT9L6CMmbMY3f6QN0',
                /*parameter pass data is parameter name param is value */
                dataType: "json",
                success: function(data) {
                    loc = data['results'][4]['formatted_address']
                    var city = loc.split(',')[0];
                    localStorage.setItem('loc', city);
                },
                error: function(result) {
                    alert("Error");
                }
            });
        }
    });
