
<<<<<<< HEAD
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
=======



$(document).ready(function(){

	$("#post").click(function(){
		window.location.replace("/post?post_id="+$(this).val());
	})
})

$(document).ready(function(){

	$("#addBuyer").click(function(){
		window.location.replace("/addBuyer?post_id="+$(this).val());
	})
	
})


>>>>>>> master
