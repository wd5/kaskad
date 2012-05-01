window.onload = function(){	jQuery('input[placeholder], textarea[placeholder]').placeholder();}

$(function(){

    $('.fancybox, a.do_comment').fancybox();

    $('.shutter').toggle(
        function () {
            $('.shutter_text').hide('slow');
        },
        function () {
            $('.shutter_text').show('slow');
        }
    );

});