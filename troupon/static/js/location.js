    $(document).ready(function() {
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(showPosition, showError);
        } else {
            toastr.error("Geolocation is not supported by this browser.");
        }

        function showError(error) {
            switch (error.code) {
                case error.PERMISSION_DENIED:
                    toastr.error("User denied the request for Geolocation.")
                    break;
                case error.POSITION_UNAVAILABLE:
                    toastr.error("Location information is unavailable.")
                    break;
                case error.TIMEOUT:
                    toastr.error("The request to get user location timed out.")
                    break;
                case error.UNKNOWN_ERROR:
                    toastr.error("An unknown error occurred.")
                    break;
            }
        }

        function showPosition(position) {
            $.ajax({
                type: "POST",
                contentType: "application/json; charset=utf-8",
                url: "https://maps.googleapis.com/maps/api/geocode/json?latlng=" + position.coords.latitude + ',' + position.coords.longitude + '&key=AIzaSyCVSRwHlla02n6Y_sYT9L6CMmbMY3f6QN0',
                dataType: "json",
                success: function(data) {
                    loc = data['results'][4]['formatted_address']
                    var city = loc.split(',')[0];
                    document.cookie = "city='" + city + "'";
                },
                error: function(result) {
                    toastr.error(result);
                }
            });
        }
    });
