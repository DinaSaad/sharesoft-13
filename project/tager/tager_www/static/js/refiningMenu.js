function posts_render(ids)
    	{
    		// alert(ids);
   			$.ajax(
   			{
			    type: "GET",
			    url: "/menu_posts/",
			    data: {"sub_ch_id" : ids},

			    success: function(req)
			    {
			    	// alert("sucess");
			      
			      $(req).find('#mydiv').each(function(i)
			      {
				      // alert($(req).find('#mydiv'));
				      $('#mydiv').append($(req).find('#post_id'));
				  }

 				  );
    			}
    		});

    	}