function Like(id) {
          $.ajax({
              headers: { "X-CSRFToken": csrf_token },
    url: Likes,
    type: 'POST',
    dataType: "json",
    csrfmiddlewaretoken: csrf_token,
  data: {'key': id},
    success: function(data) {
          $('#like').attr('class', 'ion-android-favorite');

    },
          error: function(error) {
                console.log(error);
                }
    });
    
}




