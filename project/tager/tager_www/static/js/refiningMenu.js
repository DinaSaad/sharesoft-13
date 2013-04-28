function posts_render(ids)
    	{
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

    	}