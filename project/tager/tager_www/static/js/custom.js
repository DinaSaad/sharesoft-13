
// $(document).ready(function(){
//   $("#hide").click(function(){
//     $("p").hide();
//   });
//   $("#show").click(function(){
//     $("p").show();
//   });
// });

$(document).ready(function(){

	$("#addBuyer").click(function(){
		window.location.replace("addBuyer");
	})
})
$(document).ready(function(){

	$("#rateSeller").click(function(){
		window.location.replace("profile?user_id="+$(this).val());
	})
})

$(document).ready(function(){

	$("#post").click(function(){
		window.location.replace("post?post_id="+$(this).val());
	})
})
$(document).ready(function(){


	$('#star').raty({ score: $('#rating').val()});

	// $('#star').raty()

})




// $(document).ready(function(){

// 	$("#addBuyer").click(function(){
// 		window.location.replace("addBuyer");
// 	})
// })
// "hello?ch_id="+$(this).val()