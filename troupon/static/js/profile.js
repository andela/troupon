$(document).ready(function(){

    $( "#profile" ).hide( "fast" )
    $( ".settings-page" ).find('.show-profile').click(function() {
        var parent = $(this).parentsUntil('.settings-page').parent();
        parent.find('.profile-detail').slideToggle('fast');
    });

    $( "#change-password-section" ).hide( "fast" ) 
    $('.change-password').click(function() {
        var parent = $(this).parentsUntil('.settings-page').parent();
        parent.find('.password').slideToggle('fast');
    });

    var hash = location.hash;
    if(hash == "#changepassword") $('.change-password').trigger('click');

});