
// $(document).ready(function(){

// 	$("#addBuyer").click(function(){
// 		window.location.replace("post/addBuyer");
// 	})
// })
// $(document).ready(function(){

// 	$("#rateSeller").click(function(){
// 		window.location.replace("post/addBuyer");
// 	})
// })

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
"hello?ch_id="+$(this).val()