function runningFunction(){
	r = $.post({
		url:'/web/3',
		aync: false
	});
	setTimeout("javascript:location.href='/web/4'", 3000);
	console.log(r.responseText);
}