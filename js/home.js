
$(function(){
    loadData();
function loadData(){
    var url = localStorage.getItem("baseUrl")+"/home/api/case/";        
    var data  = {"username":username,"password":password};
    $.ajax({
          type: "GET",
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

    }


 $("#li1").click(function(){
                $("#tabs").show();
                $("#tabs-2").hide();
                $("#tabs-3").hide();
                $("#aboutUs").hide();
                $("#tabs-1").show();
            });
            $("#li2").click(function(){
                $("#tabs").show();
                $("#tabs-1").hide();
                $("#tabs-3").hide();
                $("#aboutUs").hide();
                $("#tabs-2").show();
            });
            $("#li3").click(function(){
                $("#tabs").show();
                $("#tabs-2").hide();
                $("#tabs-1").hide();
                $("#aboutUs").hide();
                $("#tabs-3").show();
            });
            $("#li4").click(function(){
                $("#tabs").hide();
                $("#aboutUs").show();
                
            });
            $(function() {
                $( "#datepicker" ).datepicker();
            });
            $(function() {
                $( "#tabs" ).tabs();
            });
            $(function() {
                $('nav#menu-left').mmenu();
            });
            $(document).ready(function() {
                $('#scheduleTable').DataTable();
            });
        $("#aboutUs").hide();

};