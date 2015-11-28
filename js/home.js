
$(function(){
	$("#username").append("<a>"+localStorage.getItem("username")+"</a>");
	
    loadData($.datepicker.formatDate('yy-mm-dd', new Date()),10);

    function loadData(date,limit){
    	$("#tableData").text("");
        var url = localStorage.getItem("baseUrl")+"/cases/api/caseday/?format=json&date="+date+"&limit="+limit.toString();   
        $.ajax({
  		  type: "GET",
  		  url: url,  		 
  		  success: success,
  		  error: error,
  		 dataType: 'json', 
  		});  
        
        function success(data, textStatus, jqXHR){        	
        	$.each(data.objects,function(k,v){      
        		var defendant = "";
    			var respondant = "";
    			var res_lawyers = "";
    			var def_lawyers = "";
    			var serial = "";
    			var case_name = "";
    			var court = 0;
        		$.each(v,function(key,value){
        			
        			
        			switch(key){
	        			case "serial":
	        				serial = value;	        				
	        				break;
	        			case "case":	        					        				
	        				$.each(value.defendent,function(me,item){	        					
	        					defendant = defendant+" "+item.first_name+"."+item.last_name;
	        				});	        				
	        				$.each(value.respondant,function(me,item){
	        					respondant = respondant+" "+item.first_name+"."+item.last_name;
	        				});
	        				$.each(value.respondant_lawyers,function(me,item){
	        					res_lawyers = res_lawyers+" "+item.user.first_name+"."+item.user.last_name;
	        				});
	        				$.each(value.defense_lawyers,function(me,item){
	        					def_lawyers = def_lawyers+" "+item.user.first_name+"."+item.user.last_name;
	        				});
	        				case_name = value.name;	        				
	        				break;
	        			case "court":
	        				
	        				court = value.number.toString();
	        				break;
        			}  
        		
        		});
            var mainData = "<tr><td><div class=card><p class=serial><b>CASE NO: </b>" +  serial +"</p><p class=court_no><b>COURT NO.: </b> " + court + "</p><p class=party><b>PARTY: </b><br/> " + defendant + " Vs " + respondant + "<p class=petitioner_adv><B>PETITIONER ADV.:</b> <br/>" + def_lawyers + "</p><p class=respondent_adv><b>RESPONDENT ADV.: </b><br/>"+ res_lawyers +"</p><p class=details><b>DETAILS:</b><br/><br/></p></div>"
//        		var mainData = case_name+court+defendant+respondant+def_lawyers+res_lawyers;
    			$("#tableData").append(mainData);
        	});
        }
        
        function error(data){
        	alert("error while loading data");
        }
    }
    
    
    $("#logout").click(function(){
    	localStorage.removeItem("username");
    	window.location="index.html";
    });
    $( "#datepicker" ).datepicker({
    	  dateFormat: "yy-mm-dd",
    	  onSelect: function(dateText) {
          	loadData(dateText,10);
          }
    	});
    
  

    
});


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
    $( "#tabs" ).tabs();
});
$(function() {
    $('nav#menu-left').mmenu();
});
$(document).ready(function() {
    $('#scheduleTable').DataTable();
});
$("#aboutUs").hide();
