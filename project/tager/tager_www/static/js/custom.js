
$(document).ready(function(){
  $("#hide").click(function(){
    $("p").hide();
  });
  $("#show").click(function(){
    $("p").show();
  });
});

$(document).ready(function(){

	$("#addBuyer").click(function(){
		window.location.replace("post/addBuyer");
	})
})
// $(document).ready(function(){

// 	$("#rateSeller").click(function(){
// 		window.location.replace("post/addBuyer");
// 	})
// })

$(document).ready(function(){

	$("#post").click(function(){
		window.location.replace("post?post_id="+$(this).val());
	})
})

$(document).ready(function(){

	$("#addBuyer").click(function(){
		window.location.replace("post/addBuyer");
	})
})
"hello?ch_id="+$(this).val()