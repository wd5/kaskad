window.onload = function(){	jQuery('input[placeholder], textarea[placeholder]').placeholder();}

$(function(){

    $('.fancybox').fancybox();

    $('.shutter_ring').click(function(){

        $('.shutter_text').animate({
            height:'100%'
        },2000);

        $('.shutter').animate({
            padding: 18,
            height:'100%'
        },2000);

    });


});

