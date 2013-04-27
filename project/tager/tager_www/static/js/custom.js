
$(document).ready(function(){

	$("#post").click(function(){
		window.location.replace("/post?post="+$(this).val());
	})
})

$(document).ready(function(){
$('#Channel_dropdown').change(function(){
	window.location.replace("viewsubchannels?ch_id="+$(this).val())
});




});

 // $(document).ready(function(){
 // $('#location_dropdown').change(function(){
 //   window.location.replace("att?location_id="+$(this).val())
 // });
 // });


$(document).ready(function(){
$('#subChannel_dropdown').change(function(){
	window.location.replace("addpost?sub_ch_id="+$(this).val())
});
});


$(document).ready(function(){
      $('#picture1').hide();
      $('#picture2').hide();
      $('#picture3').hide();
      $('#picture4').hide();
      $('#picture5').hide();
  });
$(document).ready(function(){
  $('#add1').click(function(){
    $('#picture1').show();
    $('#add1').hide();
  });
});

$(document).ready(function(){
  $('#add2').click(function(){
    $('#picture2').show();
    $('#add2').hide();
  });
});


$(document).ready(function(){
  $('#add3').click(function(){
    $('#picture3').show();
    $('#add3').hide();
  });
});
$(document).ready(function(){
  $('#add4').click(function(){
    $('#picture4').show();
    $('#add4').hide();
  });
});
$(document).ready(function(){
  $('#add5').click(function(){
    $('#picture5').show();
    $('#add5').hide();
  });
});
$(document).ready(function(){
  $('#add6').click(function(){
    alert("Sorry you reached the maximum number of allowed pictures");
    $('#add6').hide();
  });
});
$(document).ready(function() {
$('#SubmitAction').attr("disabled", true);
});


$(document).ready(function() {
$(function(){
  $('#titleoutput').text("Can not be blank");
  $('#descriptionoutput').text("Can not be blank");
  $('#priceoutput').text("Can not be blank");
  $('#id_title').keyup(function(){
    data = $(this).val();
    var x = false;    
    if( data == "     "){
    $('#SubmitAction').attr("disabled", true);    
    $('#titleoutput').text("The title can not be spacs");
    }
    else{
    if( data.length < 5){
    $('#SubmitAction').attr("disabled", true);    
    $('#titleoutput').text("The title can not be shorter than 5 characters");
    }
    else{
    if( data.length > 30){
    $('#SubmitAction').attr("disabled", true);    
    $('#titleoutput').text("The title can not be more than 30 characters");
    }
    else{
    $('#SubmitAction').removeAttr("disabled");    
    $('#titleoutput').text("");
    }
    }
    $('#SubmitAction').attr("disabled", true);
    }

$('#SubmitAction').attr("disabled", true);

});
  });
});



$(document).ready(function() {

$(function(){
  $('#id_price').keyup(function(){
    alert("text");
    var data = $(this).val();
    var pattern = /^[0-9]+$/;
    if (data.length > 1 && data.match(pattern)) {
              $('#SubmitAction').removeAttr("disabled");    
              $('#priceoutput').text("");
               
                return true;
            }
          else {
              $('#SubmitAction').attr("disabled", true);    
              $('#priceoutput').text("Price must be 2 digits number");  
              return false;
            }   
});
  });

});




$(document).ready(function() {
$(function(){
  $('#id_description').keyup(function(){
    var data = $(this).val();
    var pattern = /[a-z]|[A-Z]|\d+/;
    if (data.length > 25 && data.match(pattern)) {
              $('#SubmitAction').removeAttr("disabled");    
              $('#descriptionoutput').text("");
               
                return true;
            }

          else {
              $('#SubmitAction').attr("disabled", true);    
              $('#descriptionoutput').text("Invalid description");  
              return false;
            }   
});
  });
});


$(document).ready(function(){

	$("#addBuyer").click(function(){
		window.location.replace("/addBuyer?post_id="+$(this).val());
	})
	
})


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

function reportPost(ids){
    reason = 'optionsRadios' + ids;
  $.ajax({
    url: "/report/",
    type: "POST",
    data: {
      "post_id" : ids,
      "report_reason" : $("input[name=" + reason + "]:checked").val(),
    }, 
    success: function(result) {
        alert("Report Submitted... Thank you ! :D");  
    }
});
}
function update_status_tosave(){
  $("#update_status").hide();
  $("#status").hide();
  var status1 = $("#status").text();
  $("#statusvalue").val(status1);
  $('#statusvalue').css('display', 'block');
  $('#savestatus').css('display', 'block');
}
function updates(){
  var title = "test"
  $.ajax({
    url: "/updatestatus/",
    type:"POST",
    data:{
      "status" : title,
    },
    success: function(result){
      alert("test");
    },

  })
}
 $(function() {
    var availableTags = [
      "Cairo","Alexandria","Sharkia","Assiut","Beni-Suif","Aswan","Luxor","Minya","Dakhlia","Gharbia","Monofia","Sohag","Matrouh","Beheira","Al Wadi al gdeed","Kafr el heikh","North Sinai","South Sinai","Red Sea","Portsaied","Suez","Qina", "Ismailia", "Giza", "Damietta"
    ]
    $("#id_location").autocomplete({
      source: availableTags
    });
  });
 
function get_interested(ids) {
    $.ajax({
    url: "/getInterestedIn/",
    type: "POST",
    data: {
        "post_id" : ids,
    }, 
    success: function(result) {
        $('#listOfBuyers' + id).css('display', 'block');
    }
});
}
function report(id) {
  $('.reportDIV' + id).css('display', 'block');
  $('#report_button' + id).css('display', 'none');

}
function cancelReport(id) {
  $('.reportDIV' + id).css('display', 'none');  
  $('#report_button' + id).css('display', 'block');

}
