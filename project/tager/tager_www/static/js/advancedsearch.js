
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

$(document).ready(function(){
$('#advanced_render_subchannels').hide();
$('#attributes_show').hide();
});


$(document).ready(function(){
  $('#advancedsearch_channels').change(function(){
    var channel = $('#ad_Channel_dropdown').val()

   $.ajax({
       url: "/advanced_subchannel/",
       type: "POST",
       data: {
       'ad_ch_id' : channel,
       },
           success:function(req){

            $('#advancedsearch_subchannels').html(req)

      }
    });
  });
});


$(document).ready(function(){
$('#advancedsearch_subchannels').change(function(){
    var subchannel = $('#ad_subChannel_dropdown').val()
   $.ajax({
       url: "/advanced_att/",
       type: "POST",
       data: {
       'ad_sub_ch_id' : subchannel,
       },
           success:function(req){
            $('#advanced_render_channels').hide();
            $('#advanced_render_subchannels').show();
            $('#attributes_show').show();
           	 $('#attributes_id').html(req)
             $('#attributes_id').hide();

     }
    });
  });
});
$(document).ready(function(){
$('#attributes_show').click(function(){
  $('#advanced_render_subchannels').hide();
  $('#attributes_id').show();
  $('#attributes_show').hide();
  });
});
$(document).ready(function(){
$('#advanced_render_channels').click(function(){
  window.location.replace("/advanced_search_channel_show?ad_ch_id="+$('#ad_Channel_dropdown').val())
// $('#advanced_render_subchannels').hide();
});
});
$(document).ready(function(){
$('#advanced_render_subchannels').click(function(){
  window.location.replace("/advanced_subchannel_show?ad_sub_ch_id="+$('#ad_subChannel_dropdown').val())
});
});
 $(function() {
    $( "#dialog" ).dialog();
    $('#dialog').click(function(){
  window.location.replace("/advanced_search_channel")
// $('#advanced_render_subchannels').hide();
});
  });