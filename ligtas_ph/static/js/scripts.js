$(window).scroll(function(e){
	$('#leftDiv').stop().animate({'margin-top': $(this).scrollTop()}, 5);
});