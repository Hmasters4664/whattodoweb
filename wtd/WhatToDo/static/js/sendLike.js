function Like(id) {
          $.ajax({
              headers: { "X-CSRFToken": csrf_token },
    url: Likes,
    type: 'POST',
    dataType: "json",
    csrfmiddlewaretoken: csrf_token,
  data: {'key': id},
    success: function(data) {
                  var response = JSON.parse(data);
          $('#like'+ id).attr('class', response.itemz);

          $('#count'+id).html(response.counter);

    },
          error: function(error) {
                console.log(error);
                }
    });
    
}




