function Comments(post){
      var dt = Date($.now());
    var now = $.now()/1000;
      $.ajax({
          headers: { "X-CSRFToken": csrf_token },
    url: "/postcomments",
    type: 'POST',
    dataType: "json",
    data: {
        'comment'  : $("#comm"+post).val(),
        'id': post,
        'time' : now
    },
    success: function(data) {
              console.log("sent");
              location.reload();

            $("#comm"+post).val('');

            $("#comm"+post).focus();



    },
          error: function(error) {
                console.log(error);

                }
    });

}
