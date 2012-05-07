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


    $('.to_cart').live('click', function(){
        $.ajax({
            url: "/",
            data: {

            },
            type: "POST",
            success: function(data) {

            }
        });

        return false;
    });

    $('#sendcomment').live('click', function(){
        $.ajax({
            url: "/do_comment/",
            data: {
                sender_name:$('#id_sender_name').val(),
                text:$('#id_text').val(),
                email:$('#id_email').val(),
                product:$('#id_product').val(),
                parent:$('#id_parent').val()
            },
            type: "POST",
            success: function(data) {
                if (data=='success')
                    {$('.mod_form').replaceWith("Спасибо. Ваш комментарий будет опубликован после модерации.");}
                else{
                    $('.mod_form').replaceWith(data);
                }
            }
            /*,
            error:function(jqXHR,textStatus,errorThrown){
                $('.mod_form').html(jqXHR.responseText);
            }*/
        });

        return false;
    });

});
