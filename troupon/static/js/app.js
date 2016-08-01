
$(document).ready(function() {


    //----------------------------------------
    //  Modals:
    //----------------------------------------

    function whichTransitionEndEvent(){
        // utility function for determining TransitionEndEvent browser prefixes:
        var t,
            el = document.createElement('fakeelement'),
            transitions = {
                'transition':'transitionend',
                'otransition': 'otransitionend',
                'OTransition':'oTransitionEnd',
                'MozTransition':'transitionend',
                'WebkitTransition':'webkitTransitionEnd'
            };

        for(t in transitions){
            if( el.style[t] !== undefined ){
              return transitions[t];
            }
        }
    }

    var transitionEndEvent = whichTransitionEndEvent(),
        modalsWrapper = $('.modals-wrapper'),
        modalsParent = $('.modals-parent'),
        modalsCloseBtn = $('#modals-close'),
        openedModal = null;

    var ESC = '27';

    
    function openModal(modalSelector){
        // get the modal:
        var modal = $(modalSelector);
        if(!modal.length) {
            return;
        }

        // check for any already opened modal:
        if(openedModal !== null) {

            //first close the openedModal:
            openedModal.removeClass('open').addClass('close');
            openedModal.one(transitionEndEvent, function() {
                // reset openedModal:
                openedModal.removeClass('close');
                openedModal = null;
                // can now show the new modal:
                showNewModal();
            });
        } else {
            // in the absence of an opened modal:
            showNewModal();
        }

        function showNewModal(){
            // open the modal:
            modalsWrapper.addClass('open');
            modalsParent.addClass('open');
            modal.addClass('open');

            // set close listeners:
            if(modal.attr('data-dismissable') =='false') {
                // hide the modalsCloseBtn
                modalsCloseBtn.addClass('hidden');
            } else {
                // show modalsCloseBtn:
                modalsCloseBtn.removeClass('hidden');

                // set modalsCloseBtn click listener:
                modalsCloseBtn.one('click', function(){
                    closeModal();
                });
                // set ESC keypress listener:
                $(document).one('keyup', function(event){
                    if(event.which == ESC){
                        closeModal();
                    }
                });
            }

            // assign the modal as the current openedModal:
            openedModal = modal;
        }
    }

    function closeModal(){
        // check for openedModal:
        if(!openedModal) {
            return;
        }

        // reset modal wrapper and target:
        modalsWrapper.removeClass('open');
        modalsParent.removeClass('open');

        // reset the opened modal:
        openedModal.removeClass('open').addClass('close');
        openedModal.one(transitionEndEvent, function() {
            openedModal.removeClass('close');
            // reset the openedModal pointer:
            openedModal = null;
        });
    }

    // set listeners for modal-toggle elements:
    $('.modal-toggle').each(function(){
        $(this).click(function(event){
            event.preventDefault();
            openModal($(this).attr('data-modal-target'));
        });
    });



    //----------------------------------------
    //  Flickity galleries:
    //----------------------------------------

    //initialize Flickity on the galleries:
    $('.flickity-gallery').flickity({
    
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
    
    // initialize Packery on the grids:
    
    function initDealItemsLayout() {
        var $grid = $('.packery-grid');
        $grid.packery({

            'itemSelector': '.grid-item',
            'columnWidth': '.grid-sizer',
            'gutter': '.gutter-sizer',
            'percentPosition': true,
            'isResizeBound': true

        });
    }
    initDealItemsLayout();
    
    // call packery layout everytime an item's image loads:
    $('.packery-grid').find('.item-image-wrapper img').load(function() {
        initDealItemsLayout();
    });

    // call packery layout whenever window is resized:
    $(window).resize(function() {
        initDealItemsLayout();
    });

    //----------------------------------------
    //  Date filters:
    //----------------------------------------

    // send an ajax call to server when date filter selector changes:

    var $dateFilterSelect = $('.section-heading .date-filter-select');
    $dateFilterSelect.change(function(event){
        var $queryString = '?dtf=' + event.currentTarget.selectedIndex +
            '&pg=1';
        var $path = $(location).attr('pathname');
        $.ajax({url: $path + $queryString, success: 
            function(result) {
                $('.description').detach();
                $('.section-heading').nextAll().detach();
                var $index = result.html.search('<p class="description">');
                var $html = result.html.slice($index, -1);
                $($html).insertAfter('.section-heading');
                initDealItemsLayout();
        }});
    });
});
