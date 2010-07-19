/***************************/
//@Author: Albert "deeper4k" Gazizov
//@email: deeper4k@gmail.com
//@license: Feel free to use it, but keep this credits please!					
/***************************/

//SETTING UP OUR POPUP
//0 means disabled; 1 means enabled;
var popupStatus = new Array();
popupStatus["#popupLogin"] = 0;
popupStatus["#popupRegister"] = 0;

//loading popup with jQuery magic!
function loadPopup(popup){
	//loads popup only if it is disabled
	if(popupStatus[popup]==0){
		$("#backgroundPopup").css({
			"opacity": "0.7"
		});
		$("#backgroundPopup").fadeIn("slow");
		$(popup).fadeIn("slow");
		popupStatus[popup] = 1;
	}
}

//disabling popup with jQuery magic!
function disablePopup(popup){
	//disables popup only if it is enabled
	if(popupStatus[popup]==1){
		$("#backgroundPopup").fadeOut("slow");
		$(popup).fadeOut("slow");
		popupStatus[popup] = 0;
	}
}

//centering popup
function centerPopup(popup){
	//request data for centering
	var windowWidth = document.documentElement.clientWidth;
	var windowHeight = document.documentElement.clientHeight;
	var popupHeight = $(popup).height();
	var popupWidth = $(popup).width();
	//centering
	$(popup).css({
		"position": "absolute",
		"top": windowHeight/2-popupHeight/2,
		"left": windowWidth/2-popupWidth/2
	});
	//only need force for IE6
	
	$("#backgroundPopup").css({
		"height": windowHeight
	});
	
}


//CONTROLLING EVENTS IN jQuery
$(document).ready(function(){
	$("#login").attr('href', '#');
	$("#register").attr('href', '#');
	//LOADING POPUP
	//Click the button event!
	$("#login").click(function(){
		//centering with css
		centerPopup("#popupLogin");
		//load popup
		loadPopup("#popupLogin");
	});
	$("#register").click(function(){
		$( '#popupRegister' ).load('/ajax_register_form' );
		//alert($('#register_form').form.action);
		//centering with css
		centerPopup("#popupRegister");
		//load popup
		loadPopup("#popupRegister");
	});
				
	//CLOSING POPUP
	//Click the x event!
	$("#popupLoginClose").click(function(){
		disablePopup("#popupLogin");
	});
	//Click out event!
	$("#backgroundPopup").click(function(){
		disablePopup("#popupLogin");
		disablePopup("#popupRegister");
	});
	//Press Escape event!
	$(document).keypress(function(e){
		if(e.keyCode==27 &&  (popupStatus["#popupLogin"]==1 || popupStatus["#popupRegister"]==1)){
			disablePopup("#popupLogin");
			disablePopup("#popupRegister");
		}
	});

});
/*
$( document ).ajaxStart( function() {
	$( '#spinner' ).show();
}).ajaxStop( function() {
	$( '#spinner' ).hide();
});
*/
$(document).ready(function(){
	$('.header_right .cat').click(function() {
				var id = $(this).attr('id');
				id = id.replace('cat_', '');
				$(":input[name*='category']").val(id);
				$('.header_right .active').attr('class', $('.header_right .active').attr('class').replace('active', ''));
				$(this).addClass('active');
			});
});
$(document).keypress(function(e) { 
	if (e.keyCode == 39 && e.ctrlKey && $('.b-pager__next').length) {
		window.location.href = $('.b-pager__next').attr('href');
    }
	if (e.keyCode == 37 && e.ctrlKey && $('.b-pager__prev').length) {
		window.location.href = $('.b-pager__prev').attr('href');
    } 
}); 