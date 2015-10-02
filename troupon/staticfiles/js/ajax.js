$(function(){

    $('#search').keyup(function() {

        $.ajax({
            type: "POST",
            url: "deals/search/entry",
            data: { 
                'q' : $('#search').val(),
                'csrfmiddlewaretoken' : $("input[name=csrfmiddlewaretoken]").val()
            },
            success: searchSuccess,
            dataType: 'html'
        });

    });

});

function searchSuccess(data, textStatus, jqXHR)
{
    $('#search-results').html(data);

    $('#search-results').mouseleave(function(){
        $(this).fadeOut('slow');
        });
}

