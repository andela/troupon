    $('document').ready(function(){
        MapMaker = {
            geocoder: '',
            latlng: '',
            map: '',
            $mapCanvas: document.getElementById('map'),
            $address: {'address': document.getElementsByTagName('address')[0].innerHTML},
            mapOptions: {zoom: 18},
            initialize: function() {
                this.geocoder = new google.maps.Geocoder();
                this.latlng = new google.maps.LatLng(-34.397, 150.644);
                this.mapOptions.center = this.latlng;
                this.setMap();
                this.codeAddress();
                console.log(this.$mapCanvas);
            },
            setMap: function(){
                this.map = new google.maps.Map(this.$mapCanvas, this.mapOptions);
            },
            codeAddress: function() {
                this.geocoder.geocode(this.$address, this.render);
            },
            render: function(results, status){
                if(status == google.maps.GeocoderStatus.OK){
                    MapMaker.map.setCenter(results[0].geometry.location);
                    console.log(MapMaker.map);
                    var marker = new google.maps.Marker({
                        map: MapMaker.map,
                        position: results[0].geometry.location
                    });
                } else {
                    console.log("Geocode was not successful for the following reason: " + status);
                }
            }

        };

        MapMaker.initialize();
    });
