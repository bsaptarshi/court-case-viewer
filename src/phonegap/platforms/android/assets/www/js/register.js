$(function(){
	$("#registerForm").submit(function(event){
		event.preventDefault();
		var username = $("#username").val();
		var password = $("#password").val();
		var first_name = $("#firstName").val();
		var last_name = $("#lastName").val();
		var email = $("#email").val();
		var url = localStorage.getItem("baseUrl")+"/home/api/user/";		
		var data  = {"username":username,"password":password,"first_name":first_name,
				"last_name":last_name,"email":email};
		$.ajax({
		  type: "POST",
		  url: url,
		  data: data,
		  success: success,
		  error: error,
		});
		function success(data){
			alert("User creation successfull");
			
			 window.location="home.html";
		}
		function error(){
			alert("USer not registered");			
		}
	});
	
});