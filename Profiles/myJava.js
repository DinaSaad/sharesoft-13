
$(document).ready(function(){
// Set the interval to be 3 seconds
var t = setInterval(function(){
$("#anim").animate({marginLeft:-480},1000,function(){
$(this).find("li:last").after($(this).find("li:first"));
$(this).css({marginLeft:0});
})
},3000);
});


