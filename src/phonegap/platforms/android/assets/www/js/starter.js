$(function(){
	var username = localStorage.getItem('username');
	if (username == null)
	{
		loadIndexPage();
	}
});

function loadIndexPage(){ 
   window.location="index.html";
   
}