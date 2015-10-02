

$(document).ready(function() {


	//----------------------------------------
	//	Modals:
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
		  	}

	  	for(t in transitions){
			if( el.style[t] !== undefined ){
			  return transitions[t];
			}
	  	}
	}


	var transitionEndEvent = whichTransitionEndEvent();
		modalsWrapper = $('.modals-wrapper'),
		modalsParent = $('.modals-parent'),
		modalsCloseBtn = $('#modals-close'),
		openedModal = null;

	const ESC = '27';

	
	function openModal(modalSelector){
		// get the modal:
		modal = $(modalSelector);
		if(!modal.length) return;

		// check for any already opened modal:
		if(openedModal != null) {

			//first close the openedModal:
			openedModal.removeClass('open').addClass('close');
			openedModal.one(transitionEndEvent, function(event) {
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
				modalsCloseBtn.one('click', function(event){
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
		if(!openedModal) return;

		// reset modal wrapper and target:
		modalsWrapper.removeClass('open');
		modalsParent.removeClass('open');

		// reset the opened modal:
		openedModal.removeClass('open').addClass('close');
		openedModal.one(transitionEndEvent, function(event) {
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



	//-------------------------------------
	// navigation:
	//-------------------------------------

	

});