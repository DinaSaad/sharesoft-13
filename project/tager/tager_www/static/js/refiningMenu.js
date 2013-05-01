// var Enabled=true;
function posts_render(ids)
    	{
    		// if (Enabled == true)
    		// {

    		alert(ids);
   			$.ajax(
   			{
			    type: "GET",
			    url: "/menu_posts/",
			    data: {"sub_ch_id" : ids},

			    success: function(req)
		       {
		       	alert("d5al gowa el ajax for menu");
		         $('#posts_result').html(req);

		       }
    		});
   		// }

    	}

function channel_render(ids)
{
	alert(ids);
   			$.ajax(
   			{
			    type: "GET",
			    url: "/channel_posts/",
			    data: {"ch_id" : ids},

			    success: function(req)
		       {
		       	alert("d5al gowa el ajax for menu channel");
		       	// Enabled=false;
		         $('#posts_result').html(req);
		       }
    		});
}