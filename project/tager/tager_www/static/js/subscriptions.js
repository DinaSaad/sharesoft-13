$(document).ajaxSend(function(event, xhr, settings) {
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    function sameOrigin(url) {
        // url could be relative or scheme relative or absolute
        var host = document.location.host; // host + port
        var protocol = document.location.protocol;
        var sr_origin = '//' + host;
        var origin = protocol + sr_origin;
        // Allow absolute or scheme relative URLs to same origin
        return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
            (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
            // or any other URL that isn't scheme relative or absolute i.e relative.
            !(/^(\/\/|http:|https:).*/.test(url));
    }
    function safeMethod(method) {
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    if (!safeMethod(settings.type) && sameOrigin(settings.url)) {
        xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
    }
});    

function subscribe(){
	var channel = $("#channel_id").val()
	var subchannel = $("#subchannel_id").val()
	var parameter = $("#parameter_id").val()
	var choice = $("#choice_id").val()
	if(channel != '--------'){
		if(subchannel != '--------'){
			if(parameter != '--------'){
				if(choice != '--------'){
					var channel = $("#channel_id").val()
					var subchannel = $("#subchannel_id").val()
					var parameter = $("#parameter_id").val()
					var choice = $("#choice_id").val()
					$.ajax({
    					url: "/subscription_by_param/",
    					type: "GET",
    					data: {
    						"ch_id" : channel,
    						"sch_id" : subchannel,
    						"p_id" : parameter,
    						"cho_id" : choice,
    					}, 
        				success: function(req) {
  							alert("You are now subscribed");
						}
					});
				}
			}
			else{
				var channel = $("#channel_id").val()
				var subchannel = $("#subchannel_id").val()
				$.ajax({
    				url: "/subscription_by_subchann/",
    				type: "GET",
    				data: {
    					"ch_id" : channel,
    					"sch_id" : subchannel,
    				}, 
        			success: function(req) {
     					alert("You are now subscribed");
					}
				});
			}
		}
		else{
			var channel = $("#channel_id").val()
			$.ajax({
    			url: "/subscription_by_chann/",
    			type: "GET",
    			data: {
    				"ch_id" : channel,
    			}, 
        		success: function(req) {
  					alert("You are now subscribed");
				}
			});
		}
	}
}
$(document).ready(function(){
	$("#choose").change(function() {
		document.getElementById('channel_id').selectedIndex = 0;
		document.getElementById('subchannel_id').selectedIndex = 0;
		document.getElementById('parameter_id').selectedIndex = 0;
		document.getElementById('choice_id').selectedIndex = 0;
		var item = $("#choose").val()
		if(item == 'Channel subscription') {
			$('#subchannel').css('display', 'none');
			$('#parameter').css('display', 'none');
			$('#choice').css('display', 'none');
			$('#channel').css('display', 'block');
		}
		else {
			if(item == 'Subchannel subscription') {
				$('#parameter').css('display', 'none');
				$('#choice').css('display', 'none');
				$('#channel').css('display', 'block');
				$('#subchannel').css('display', 'block');
				$("#channel_id").change(function(){
					var channel = $("#channel_id").val()
					if(channel != '--------'){
						$.ajax({
    						url: "/subchannels_sub/",
    						type: "GET",
    						data: {
    							"ch_id" : channel,
    						},
        					success: function(req) {
  								$('#subchannel_id').remove();
    							$(req).find('#subchannel').each(function(i){
     								$('#subchannel').append($(req).find('#subchannel_id'));
    							});
							}
						});
					}				
				});
			}
			else {
				if(item == 'Attribute subscription'){
					$('#channel').css('display', 'block');
					$('#subchannel').css('display', 'block');
					$('#parameter').css('display', 'block');
					$('#choice').css('display', 'block');
					$('#channel_id').change(function(){
					var channel = $("#channel_id").val()
					if(channel != '--------'){
    					$.ajax({
    						url: "/subchannels_sub/",
    						type: "GET",
    						data: {
    							"ch_id" : channel,
    						}, 
        					success: function(req) {
  								$('#subchannel_id').remove();
    							$(req).find('#subchannel').each(function(i){
     								$('#subchannel').append($(req).find('#subchannel_id'));
    							});
    							$('#subchannel_id').change(function(){
    								var subchannel = $('#subchannel_id').val()
    								if(subchannel != '--------'){
    									$.ajax({
    										url: "/parameters_sub/",
    										type: "GET",
    										data: {
    											"sch_id" : subchannel,
    										}, 
        									success: function(req) {  								
  												$('#parameter_id').remove();
    											$(req).find('#parameter').each(function(i){
     												$('#parameter').append($(req).find('#parameter_id'));
    											});
    											$('#parameter_id').change(function(){
    												var parameter = $("#parameter_id").val()
    												if(parameter != '--------'){
    													$.ajax({
    														url: "/choices_sub/",
    														type: "GET",
    														data: {
    															"p_id" : parameter,
    														}, 
        													success: function(req) {
        														$('#choice_id').remove();
    															$(req).find('#choice').each(function(i){
     																$('#choice').append($(req).find('#choice_id'));
    															});
															}
														});
    												}
    											});
											}
										});
    								}
    							})
							}
						});
    				}
				});
				}
				else{
					$('#channel').css('display', 'none');
					$('#subchannel').css('display', 'none');
					$('#parameter').css('display', 'none');
					$('#choice').css('display', 'none');
				}
			}
		}
	});
});