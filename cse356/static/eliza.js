$(function() {
	console.log("ready");
	$("#human").click(function() {
		var text = $("#input").val();
		$('#chatbox').append("<div class='human'><p>"+text+"</p></div>");
		$.ajax({
			url: '/eliza/DOCTOR/',
			data: {human: text},
			type: 'POST',
			success: function(data) {
				console.log(data);
				$('#chatbox').append("<div class='bot'><p>"+data.eliza+"</p></div>")
			},
			error: function(error) {
				console.log(error);
			}
		})
	});
});
