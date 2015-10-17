
$(document).ready(function() {

    //----------------------------------------
    //  Featured deals gallery:
    //----------------------------------------


    //initialize flickity on the featured deals gallery:

    var $gallery = $('#banner-section .gallery').flickity({
        
        setGallerySize: false,
        freeScroll: true,
        wrapAround: true,
        autoPlay: true,
        lazyLoad: 1,
        imagesLoaded: true,

        arrowShape: { 
            x0: 10,
            x1: 60, y1: 50,
            x2: 60, y2: 40,
            x3: 20
        }
    });

    /*
    //set the background color of a loaded gallery cell to the image's dominant color:
    $gallery.on( 'lazyLoad', function( event, cellElement ){
        try {

            // get the loaded image:
            var loadedImage = event.originalEvent.target;
            loadedImage.crossOrigin = "Anonymous";

            //get it's domninant color:
            var colorThief = new ColorThief();
            var dominantColor = colorThief.getColor(loadedImage);

            //modifiy the cell's background color, sizing and positioning:
            $( cellElement ).css({
                "background-color": "rgba(" + dominantColor[0] + "," + dominantColor[1] + "," + dominantColor[2] + ", 1)"
            });

            //modifiy the cell image's sizing and positioning:
            $( loadedImage ).css({
                "width": "100%",
                "height": "auto",
                "left": "0px",
                "top": "50%",
                "transform": "translateY(-50%)"
            });

        } catch (e) {
            console.log(e);
        }
    })
    */

});