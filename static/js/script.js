window.onload = function(){	jQuery('input[placeholder], textarea[placeholder]').placeholder();}

$(function(){

    $('.cart_qty_modal').hide();

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

    // Удаление из корзины

    $('.cart_qty_modal_text').keypress(function(e){
        if(e.which == 13)
            $('.cart_qty_modal_ok').trigger("click");
        else
        if( e.which!=8 && e.which!=0 && (e.which<48 || e.which>57))
        {
            alert("Только цифры");
            return false;
        }
    });

    $('.cart_qty_modal_text').keyup(function(){
        if($(this).val() == '')
            $(this).val(0);
        else if($(this).val() > 1000000)
            $(this).val(1000000);
        var cnt = $(this).val();
        var price = $('.cart_qty_price').html();
        var sum = price * cnt;
        //sum = Math.round(sum * 100)/100;
        $('.cart_qty_total_price').html(sum);
    });

    $('.cart_del').live('click', function(){
        if ($('.cart_qty_modal').css('display')=='none'){
            var el = $(this);
            var cart_product_id = el.find('.product_id').val();

            if (cart_product_id){
                $.ajax({
                    type:'post',
                    url:'/delete_product_from_cart/',
                    data:{
                        'cart_product_id':cart_product_id
                    },
                    success:function(data){
                        data = eval('(' + data + ')');
                        //$('.header_cart').html(data.cart_html);

                        if (data.cart_total == ''){
                            $('.cart_items').find('h1').html('Ваша корзина пока пуста');
                            $('.cart_items').find('.cart_sum').fadeOut('fast', function(){
                                $('.cart_sum').remove();
                            });
                        }
                        else{
                            $('.itog').text(data.cart_total);
                        }

                        el.parent().fadeOut('fast', function(){
                            $(this).remove();
                        });
                    },
                    error:function(data){
                    }
                });
            }
        }
    });

    $('.cart_qty_modal_cancel').live('click', function(){
        $('.cart_qty_modal').hide();
        $('.cart_qty_modal_ok').attr('disabled', true);
        $('.submit input').attr('disabled', false);
        $('.cart_del_disabled').attr('class','cart_del');
    });

    $('.cart_item_qty_btn input').live('click', function(){
        var price = $(this).parent().parent().find('.cart_item_price').html();
        var count = $(this).attr('name');
        var summ = $(this).parent().parent().find('.cart_item_sum').html();
        $('.cart_qty_price').html(price);
        $('.cart_qty_modal_text').val(count);
        $('.cart_qty_total_price').html(summ);
        $('.cart_qty_modal').show();
        $('.cart_qty_modal_text').focus();
        var pos = $(this).parent().parent().position();
        var left = $(this).parent().position().left;
        var top = $(this).parent().position().top;
        var pos2 = $('.cart_qty_modal_text').position();
        var itemid = $(this).parent().parent().find('.product_id').val();
        var cart = $(this).parent().parent().find('.id_cart').val();
        //alert('l: '+pos.left+' t: '+pos.top)
        $('.cart_qty_item_id').val(itemid);
        $('.cart_qty_cart_id').val(cart);
        $('.cart_qty_modal_ok').attr('disabled', false);
        $('.cart_qty_modal').css('left', (left-pos2.left) + 'px');
        $('.cart_qty_modal').css('top', (pos.top-top) +'px');
        $('.submit input').attr('disabled', true);
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
