$(document).ready(function() {

    // disable save button on page load
    var button  = $('#save');
    button.attr('disabled', 'disabled');

    var telInput = $('#mobile-number');
    telInput.intlTelInput({
        initialCountry: 'auto',
        geoIpLookup: function(callback) {
            $.get('http://ipinfo.io', function() {},
                 'jsonp').always(function(resp) {
            var countryCode = (resp && resp.country) ? resp.country : '';
            callback(countryCode);
        });
    },
        utilsScript: '/static/bower_components/jackocnr/lib/libphonenumber/build/utils.js',
        nationalMode: 'true'
    });

    var errorMsg = $('#error-msg');
    var validMsg = $('#valid-msg');

    var reset = function() {
        telInput.removeClass('error');
        errorMsg.addClass('hide');
        validMsg.addClass('hide');
    };

    // on blur: validate
    telInput.blur(function() {
        reset();
            if ($.trim(telInput.val())) {
            if (telInput.intlTelInput('isValidNumber')) {
              validMsg.removeClass('hide');
            } else {
              telInput.addClass('error');
              errorMsg.removeClass('hide');
            }
        }
    });

    // on keyup / change flag: reset
    telInput.on('keyup change', reset);

        $('form').submit(function() {
        $('#hidden').val(telInput.intlTelInput('getNumber'));
    });
        // enable save button on changes in form data
        $('form :input').change(function() {
            $(this).closest('form').data('changed', true);
            button.removeAttr('disabled');
    });

    $('#user-country').on('change', function(event){
        var country = $(this).val();

        if(country == 0) {
            $('#nigerian-locations').addClass('hidden');
            $('#kenyan-locations').addClass('hidden');
        } else if(country == 1) {
            $('#nigerian-locations').removeClass('hidden');
            $('#kenyan-locations').addClass('hidden');
        } else if(country == 2) {
            $('#kenyan-locations').removeClass('hidden');
            $('#nigerian-locations').addClass('hidden');
        }
    });

});
