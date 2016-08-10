$(function(){
	var i = 0;
	$('#openoff tr').each(function(){
    	i++
    });
    $('.badge').html(i);
    
    $('#clickOn').click(function(){
    	$(this).hide();
        $('#clickOff').show();
        $('table').removeClass('off');
    });
    $('#clickOff').click(function(){
    	$(this).hide();
        $('#clickOn').show();
        $('table').addClass('off');
    });
});
