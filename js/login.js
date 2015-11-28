$(function(){
	var username = localStorage.getItem("username");
	if (username!=null){
		window.location="home.html";
		
	}
	
	$("#loginForm").submit(function(event){
		event.preventDefault();
		var username = $("#username").val();
		var password = $("#password").val();
		var url = localStorage.getItem("baseUrl")+"/home/login/";		
		var data  = {"username":username,"password":password};
		$.ajax({
		  type: "POST",
		  url: url,
		  data: data,
		  success: success,
		  error: error,
		});
		function success(data){
			alert("Login successfull");
			localStorage.setItem("username",username);
			 window.location="home.html";
		}
		function error(){
			alert("Login failed");			
		}
	});


});