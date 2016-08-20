function runningFunction(){
	r = $.post('/web/3');
	setTimeout("javascript:location.href='/web/4'", 3000); 
	return r.resoponseText;
}