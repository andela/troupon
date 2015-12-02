'use strict';
$(document).ready(function(){
    $( "#profile" ).hide( "fast" );
    $( ".settings-page" ).find('.show-profile').click(function() {
        var parent = $(this).parentsUntil('.settings-page').parent();
        parent.find('.profile-detail').slideToggle('fast');
    });

    $( "#change-password-section" ).hide( "fast" ); 
    $('.change-password').click(function() {
        var parent = $(this).parentsUntil('.settings-page').parent();
        parent.find('.password').slideToggle('fast');
    });

    var hash = location.hash;
    if(hash == "#changepassword") $('.change-password').trigger('click');

    
        $('#merchantform').on('submit', function(event) {
            var $form = $(this);
            console.log($form)

            $.ajax({
                type: $form.attr('method'),
                url: $form.attr('action'),
                data: $form.serialize(),

                success: function(data) {
                if (data == "success") {

                    location.href= "/userprofile/verify/";
                }
            },
                error: function(error) {
                    console.log(error.responseText)
                },

                headers: {
                    "X-CSRFToken": $("input[name='csrfmiddlewaretoken']").val()
                    },

            });

        });

});