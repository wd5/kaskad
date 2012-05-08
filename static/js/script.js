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
    //Анимация корзины при изменении

    function animate_cart(){

        $('.cart').animate({
                opacity: 0.25
            }, 200, function() {
                $(this).animate({
                    opacity: 1
                },200);
            }
        );

    }

    function create_img_fly(el)
    {
        var img = el.find('.item_img_zl');
        var offset = el.find('img').offset();
        element = "<div class='img_fly'>"+img.html()+"</div>";
        $('body').append(element);
        $('.img_fly').css({
            'position': "absolute",
            'z-index': "1000",
            'left': offset.left,
            'top': offset.top
        });

    }

    //Добавление товара в корзину

    $('.to_cart').live('click', function(){
        var product_id = $('.product_id').val()

        if (product_id){
            $.ajax({
                type:'post',
                url:'/add_product_to_cart/',
                data:{
                    'product_id':product_id
                },
                success:function(data){
                    $('.img_fly').remove();
                    create_img_fly($('.product_img'));

                    $('.cart').replaceWith(data);

                    var fly = $('.img_fly');
                    var left_end = $('.cart').offset().left;
                    var top_end = $('.cart').offset().top;

                    fly.animate(
                        {
                            left: left_end,
                            top: top_end
                        },
                        {
                            queue: false,
                            duration: 600,
                            easing: "swing"
                        }
                    ).fadeOut(600);

                    setTimeout(function(){
                        animate_cart();
                    } ,600);

                },
                error:function(jqXHR,textStatus,errorThrown){

                }
            });
        }

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
