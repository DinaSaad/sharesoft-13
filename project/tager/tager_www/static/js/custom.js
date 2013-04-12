



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


