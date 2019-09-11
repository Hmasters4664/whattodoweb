function getM(id) {
          $.ajax({
              headers: { "X-CSRFToken": csrf_token },
    url: GETMESSAGES,
    type: 'POST',
    dataType: "json",
    csrfmiddlewaretoken: csrf_token,
  data: {'key': id},
    success: function(data) {
        for (i in data){
         $('#messages-1').append(
          '<div class="sms">'+
             '<h6>'+data.name + '</h6>' +
                        '<p>'+ data.text +'</p>' +
                        '<h6>'+data.created + '</h6>' +
                    '</div>'
      );

        }

    },
          error: function(error) {
                console.log(error);
                }
    });
    
}




