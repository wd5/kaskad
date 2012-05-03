window.onload = function(){	jQuery('input[placeholder], textarea[placeholder]').placeholder();}

$(function(){

    $('.fancybox').fancybox();

    $('.shutter').toggle(
        function () {
            $('.shutter_text').hide('slow');
        },
        function () {
            $('.shutter_text').show('slow');
        }
    );

    $('.do_comment').toggle(
        function(){
            $('.mod_form').slideDown();
        },
        function(){
            $('.mod_form').slideUp();
        }
    );

    $('input[value="Отправить"]').click(function(){

        //alert($('input[name="sender_name"]').val());

    });

});

function hideForm()
    {$('.mod_form').hide();
    }

function showForm()
    {$('.mod_form').show();
    }