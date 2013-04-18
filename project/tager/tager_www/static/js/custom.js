
$(document).ready(function(){
	$('#rateSeller').change(function(){
	window.location.replace("hello?ch_id="+$(this).val())
	});
});

$('#rateSeller').on('click', function(){
		// $(".todo").remove();
		alert("Handler rateSeller called.");
	})

$("#rateSeller").click(function() {
  alert("Handler for rateSeller called.");
});

$(document).ready(function(){
  $("#hide").click(function(){
    $("p").hide();
  });
  $("#show").click(function(){
    $("p").show();
  });
});


$(document).ready(function(){

	$("#post").click(function(){
		window.location.replace("/post?post_id="+$(this).val());
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
if($("#id_location").val().length == 0){
  $('#descriptionoutput').text("Can not be blank");
}
});




 $(function() {
    var availableTags = [
      "Cairo","Alexandria","Sharkia","Assiut","Beni-Suif","Aswan","Luxor","Minya","Dakhlia","Gharbia","Monofia","Sohag","Matrouh","Beheira","Al Wadi al gdeed","Kafr el heikh","North Sinai","South Sinai","Red Sea","Portsaied","Suez","Qina", "Ismailia", "Giza", "Damietta"
    ]

    $( "#id_location" ).autocomplete({
      source: availableTags
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

