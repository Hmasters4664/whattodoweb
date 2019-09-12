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
              console.log(data[0].text);
            console.log(data[0].created);

            $('<div class="sms_right"><p>' + $('#mess').val() + '</p><h6>' + dt + '</h6></div>').insertBefore('.type_messages');
            $('#mess').val('')

            $('#mess').focus()


    },
          error: function(error) {
                console.log(error);

                }
    });

}
