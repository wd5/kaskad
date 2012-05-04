window.onload = function(){	jQuery('input[placeholder], textarea[placeholder]').placeholder();}

$(function(){
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            function getCookie(name) {
                var cookieValue = null;
                if (document.cookie && document.cookie != '') {
                    var cookies = document.cookie.split(';');
                    for (var i = 0; i < cookies.length; i++) {
                        var cookie = jQuery.trim(cookies[i]);
                        // Does this cookie string begin with the name we want?
                        if (cookie.substring(0, name.length + 1) == (name + '=')) {
                            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                            break;
                        }
                    }
                }
                return cookieValue;
            }
            if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
                // Only send the token to relative URLs i.e. locally.
                xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
            }
        }
    });

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
        $.ajax({
            url: "/ajax/",
            data: {name:"bot"},
            type: "POST",
            complete: function() {
                $('.textarea').html();
            }
        });

    });

});

function hideForm()
    {$('.mod_form').hide();
    }

function showForm()
    {$('.mod_form').show();
    }