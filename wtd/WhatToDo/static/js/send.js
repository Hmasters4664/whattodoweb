function sendMessage(){
   var dt = Date($.now());
   var now = $.now()/1000;
      $.ajax({
          headers: { "X-CSRFToken": csrf_token },
    url: "/send",
    type: 'POST',
    dataType: "json",
    data: {
        'message'  : $('#mess').val(),
        'id': document.getElementById("other").value,
        'time' : now
    },
    success: function(data) {
              console.log("sent");

            $('#mess').val('')

            $('#mess').focus()



    },
          error: function(error) {
                console.log(error);

                }
    });

}
