$(function(){
    
    $('#send_question').live('click', function(){
        var name = $('.faq_form #id_name').val();
        var email = $('.faq_form #id_email').val();
        var question = $('.faq_form #id_question').val();

        $.ajax({
            type:'post',
            url:'/send_question/',
            data:{
                'name':name,
                'email':email,
                'question':question
            },
            success:function(data){
                if (data=='success'){
                    $('.faq_form .sended').text('Ваш вопрос отправлен.');
                    $('.faq_form #id_name').val('');
                    $('.faq_form #id_email').val('');
                    $('.faq_form #id_question').val('');
                    $('.faq_form .errorlist').remove();
                }
                else{
                    $('.faq_form').html(data);
                }
            },
            error:function(){
                $('.faq_form .sended').text('Произошла ошибка, попробуйте задать вопрос позже.');
            }
        });
    });

    
});