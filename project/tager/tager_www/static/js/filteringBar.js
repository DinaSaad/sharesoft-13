<script type="text/javascript">

$(function() 
{
 var refine_list
 var status_list
 var min_price
 var max_price
   $('.refiningSubchannels').on('change', function() 
    {
    var refine_list = new Array();        
        $('.refiningSubchannels:checked').each(function() {
            var tmp = $('#subchannel_id').val();
            refine_list.push(tmp);
            // alert(refine_list.length)
;        });

          var status_list = new Array();        
        $('.statusChange:checked').each(function() {
            var tmp = $('#status').val();
            status_list.push(tmp);
            // alert(status_list.length)
;        });

        min_price= parseInt($('#buying_slider_min').val());
        max_price= parseInt($('#buying_slider_max').val());
        
   $.ajax
    ({
       type: "GET",
       url: "/viewingPosts/",
       data: {  "list": refine_list, "status": status_list , "min":min_price , "max":max_price},
       
       // , min_price, max_price 
       success: function(req)
       {
        // alert("success");
         $('#posts_result').html(req);
       }
    });

    });
  
   $('.statusChange').on('change', function() 
    {
     var refine_list = new Array();        
        $('.refiningSubchannels:checked').each(function() {
            var tmp = $('#subchannel_id').val();
            refine_list.push(tmp);
            // alert(refine_list.length)
;        });

          var status_list = new Array();        
        $('.statusChange:checked').each(function() {
            var tmp = $('#status').val();
            status_list.push(tmp);
            // alert(status_list.length)
;        });

         min_price= parseInt($('#buying_slider_min').val());
        max_price= parseInt($('#buying_slider_max').val());

   $.ajax
    ({
       type: "GET",
       url: "/viewingPosts/",
       data: {  "list": refine_list, "status": status_list , "min":min_price , "max":max_price },
       success: function(req)
       {
        // alert("success");
         $('#posts_result').html(req);
       }
    });
    });

$('#buying_slider_min').change(function() {
    
    var min = parseInt($('#buying_slider_min').val());
    var max = parseInt($('#buying_slider_max').val());
    
    if (min > max) {
        $('#buying_slider_min').val(max);
        // $(this).slider('refresh');
    }

    var refine_list = new Array();        
        $('.refiningSubchannels:checked').each(function() {
            var tmp = $('#subchannel_id').val();
            refine_list.push(tmp);
            // alert(refine_list.length)
;        });

          var status_list = new Array();        
        $('.statusChange:checked').each(function() {
            var tmp = $('#status_list').val();
            status_list.push(tmp);
            // alert(status_list.length)
;        });

        min_price= parseInt($('#buying_slider_min').val());
        max_price= parseInt($('#buying_slider_max').val());
        

        $.ajax
    ({
       type: "GET",
       url: "/viewingPosts/",
       data: {  "list": refine_list, "status": status_list , "min":min_price , "max":max_price },
       success: function(req)
       {
        // alert("success");
         $('#posts_result').html(req);
       }
    });
});
$('#buying_slider_max').change(function() {
    var min = parseInt($('#buying_slider_min').val());
    var max = parseInt($('#buying_slider_min').val());

    if (min > max) {
        $('#buying_slider_max').val(min);
        // $(this).slider('refresh');
    }
    // alert(max);
    var refine_list = new Array();        
        $('.refiningSubchannels:checked').each(function() {
            var tmp = $('#subchannel_id').val();
            refine_list.push(tmp);
            // alert(refine_list.length)
;        });

          var status_list = new Array();        
        $('.statusChange:checked').each(function() {
            var tmp = $('#status').val();
            status_list.push(tmp);
            // alert(status_list.length)
;        });

min_price= parseInt($('#buying_slider_min').val());
        max_price= parseInt($('#buying_slider_max').val());
        
$.ajax
    ({
       type: "GET",
       url: "/viewingPosts/",
       data: {  "list": refine_list, "status": status_list , "min":min_price , "max":max_price },
       success: function(req)
       {
        // alert("success");
         $('#posts_result').html(req);
       }
    });
});
});

</script>