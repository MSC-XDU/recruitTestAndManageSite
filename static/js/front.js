function runningFunction(){
	r = $.post('/web/3');
	setTimeout("javascript:location.href='/web/4'", 3000);
	console.log(r.resoponseText);
	return r.resoponseText;
}