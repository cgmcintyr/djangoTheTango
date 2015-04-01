$(document).ready(function() {
	$('#likes').click(function(){
		var catid;
		catid = $(this).attr("data-catid");
		$.get('/rango/like_category/', {category_id: catid}, function(data){
			$('#like_count').html(data);
			$('#likes').hide();
		});
	});

	$('#suggestion').keyup(function(){
		var query;
		query = $(this).val();
		$.get('/rango/suggest_category/', {suggestion: query}, function(data){
			$('#cats').html(data);
		});
	});
	
	$('.rango-add').click(function(){
		var title;
		var url;
		var catid;
		
		title = $(this).attr("data-title");
		url = $(this).attr("data-url");
		catid = $(this).attr("data-catid");
		$.get('/rango/auto_add_page/', {title: title, url: title, category_id: catid}, function(data){
			$('#pages').html(data);
		});
	});

});
