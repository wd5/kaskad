window.onload = function(){	jQuery('input[placeholder], textarea[placeholder]').placeholder();}

$(function(){

    $('.fancybox, a.do_comment').fancybox();


    $(".shutter_text").hide();

    $('.shutter_ring').click(function(){
        if ($('.shutter').css('padding') == '9px')
            {SlideShutterDown();}
        if ($('.shutter').css('padding') == '18px')
            {SlideShutterUp();}
    });


});

function SlideShutterDown()
    {
        duration = 500;

        $('.shutter_ring').hide('slow');
        $('.shutter_b').hide('slow');
        $('.shutter').animate({
            padding: '18px',
            height: '100%'
        },duration);

        $('.shutter_text').css(
            {height: '100%',
            opacity: '0.0'}
        ).show('slow').delay(duration).animate({opacity: '1.0'},duration);
        $('.shutter_ring').delay(duration/4).fadeIn('slow');
        $('.shutter_b').delay(duration/4).fadeIn('slow');

    }

function SlideShutterUp()
    {
        duration = 500;

        $('.shutter_ring').hide('slow').delay(duration/2);
        $('.shutter_b').hide('slow').delay(duration/2);

        $('.shutter_text').animate({opacity: '0.0'},duration).css(
            {height: '1px'}
        ).hide('slow').delay(duration);

        $('.shutter').animate({
            padding: '9px',
            height: '0%'
        },duration);

        $('.shutter_ring').fadeIn('fast');
        $('.shutter_b').fadeIn('fast');

    }