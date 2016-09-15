$(function(){
	
var x = $('#openoff tr');
x.each(function(i){
	$('.badge').html(i);
    i++
$(this).find('td').eq(0).html(i);
});
    
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
