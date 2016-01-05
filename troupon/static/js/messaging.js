$(document).ready(function(){
    $('#compose-btn').on('click', toggleDisplay);
    $('#reply-btn').on('click', toggleDisplay);
});

var toggleDisplay = function(){
    $('#compose-form').toggleClass('hidden');
    $(this).find('i').toggleClass('fa-chevron-right', 1000, "easeOutSine");
    $(this).find('i').toggleClass('fa-chevron-down', 1000, "easeOutSine");
}