function sendMessage(){
      $.ajax({
    url: FRIEND,
    type: 'POST',
    dataType: "json",
    data: {
        'message'  : $('#mess').val()
    },
    success: function(data) {
         $('#messages-1').append(
          '<div class="sms">'+
                        '<p>'+ data.text +'</p>' +
                        '<h6>'+data.created + '</h6>' +
                    '</div>'
      );

    },
          error: function(error) {
                console.log(error);
                }
    });

}

$('#btn').click(function() {
    sendMessage()

});