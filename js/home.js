
$(function(){
	$("#username").append("<a>"+localStorage.getItem("username")+"</a>");
	clearData();
	
    loadData(100,$.datepicker.formatDate('yy-mm-dd', new Date()));

    function loadData(limit,date,case_no,court_no){
    	date = date||null;
    	case_no = case_no||null;
    	court_no = court_no||null;
    	$("#tableData").text("");
    	data = {};
    	data["limit"] = limit;
    	
    	data["format"] = "json";
    	if (case_no != null && case_no!=""){
    		data["case__name"] = case_no;
    	}
    	if (court_no != null && court_no!=""){
    		data["court__number"] = parseInt(court_no);
    	}
    	if (date!= null){
    		data["date"] = date;
    	}    	
        var url = localStorage.getItem("baseUrl")+"/cases/api/caseday/";
        
      
        $.ajax({
  		  type: "GET",
  		  url: url, 
  		  data:data,
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
    			var date = "";
        		$.each(v,function(key,value){
        			
        			
        			switch(key){
	        			case "serial":
	        				serial = value;	        				
	        				break;
	        			case "case":	    	        				
	        				$.each(value.defendent,function(me,item){	        					
	        					defendant = defendant+" "+item.username;
	        				});	      
	        				
	        				$.each(value.respondant,function(me,item){
	        					respondant = respondant+" "+item.username;
	        				});
	        				$.each(value.respondant_lawyers,function(me,item){
	        					res_lawyers = res_lawyers+" "+item.user.username;
	        				});
	        				$.each(value.defense_lawyers,function(me,item){
	        					def_lawyers = def_lawyers+" "+item.user.username;
	        				});
	        				case_name = value.name;	        				
	        				break;
	        			case "court":
	        				
	        				court = value.number.toString();
	        				break;
	        			case "date":	        				
	        				date = value;
	        				break;
        			}  
        		
        		});
        		
        	defendant = defendant.replace("amp;","");
        	respondant = respondant.replace("amp;","");
        	def_lawyers = def_lawyers.replace("amp;","");
        	res_lawyers = res_lawyers.replace("amp;","");
            var mainData = "<tr><td><div class=card><p class=serial><b>Case NO: </b>" +  case_name +"</p><p class=serial><b>Serial NO: </b>" +  serial +"</p><p class=court_no><b>COURT NO.: </b> " + court + "</p><p class=party><b>PARTY: </b><br/> " + defendant + " Vs " + respondant + "<p class=petitioner_adv><B>PETITIONER ADV.:</b> <br/>" + def_lawyers + "</p><p class=respondent_adv><b>RESPONDENT ADV.: </b><br/>"+ res_lawyers +"</p><p class=date><b>Date:</b><br />"+date+"</p><br /></div>"
//        		var mainData = case_name+court+defendant+respondant+def_lawyers+res_lawyers;
    			$("#tableData").append(mainData);
        	});
        }
        
        function error(jqXHR,error, errorThrown){
        	 alert(jqXHR.responseText); 
        	
        }
    }
    
    
    $("#logout").click(function(){
    	localStorage.removeItem("username");
    	window.location="index.html";
    });
    $( "#datepicker" ).datepicker({
    	  dateFormat: "yy-mm-dd",
    	  onSelect: function(dateText) {
    		
    		localStorage.setItem("date",dateText);
          	loadData(100,dateText,localStorage.getItem("case_no"),localStorage.getItem("court_no"));
          }
    	});
    $("#caseno").on("change paste keyup", function() {
	    	localStorage.setItem("case_no",$(this).val());
	      	loadData(100,localStorage.getItem("date"),localStorage.getItem("case_no"),localStorage.getItem("court_no"));
    	});
    $("#courtno").on("change paste keyup", function() {
    		localStorage.setItem("court_no",$(this).val());
      		loadData(100,localStorage.getItem("date"),localStorage.getItem("case_no"),localStorage.getItem("court_no"));
	});
   
    
  function clearData(){
	  localStorage.removeItem("date");
	  localStorage.removeItem("case_no");
	  localStorage.removeItem("court_no");
	  loadData(100,$.datepicker.formatDate('yy-mm-dd', new Date()));
	  $( "#datepicker" ).val("");
	  $("#courtno").val("");
	  $("#caseno").val("");

  }
  $("#clear").click(function(){
  	clearData();
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
    $('#scheduleTable').DataTable({
    	"paging":   false,
        "ordering": false,
        "info":     false        	
    });
    
});
$("#aboutUs").hide();
