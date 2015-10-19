
$(document).ready(function() {

    //----------------------------------------
    //  Flickity galleries:
    //----------------------------------------

    //initialize Flickity on the galleries:
    var $gallery = $('.flickity-gallery').flickity({
    
        cellSelector: '.gallery-cell',
        setGallerySize: false,
        freeScroll: true,
        wrapAround: true,
        autoPlay: true,
        imagesLoaded: true,

        arrowShape: { 
            x0: 10,
            x1: 60, y1: 50,
            x2: 60, y2: 40,
            x3: 20
        }

    });

    //----------------------------------------
    //  Packery grids:
    //----------------------------------------
    
    //initialize Packery on the grids:
    var $grid = $('.packery-grid').packery({

        "itemSelector": '.grid-item',
        "columnWidth": ".grid-sizer",
        "gutter": ".gutter-sizer",
        "percentPosition": true

    });

});