
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


// $(document).ready(function(){
// $('#Channel_dropdown').change(function(){
//   window.location.replace("../subchannel?ch_id="+$(this).val())
// });
// });


// $(document).ready(function(){
// $('#subChannel_dropdown').change(function(){
//   window.location.replace("../att?sub_ch_id="+$(this).val())
// });
// });



