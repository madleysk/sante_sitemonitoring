//My personalized scripts

var url= window.location.href
document.addEventListener('DOMContentLoaded', function(){
	//keeping search value in the searchbox
	var search = document.querySelector('#search');
	if ( url.split("=").length > 1 ){
		search.value = url.split("=")[1];
	}
	});
