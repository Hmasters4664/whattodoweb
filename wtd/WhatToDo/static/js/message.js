function sendMessage(){
      $.ajax({
    url: FRIEND,
    type: 'GET',
    dataType: "json",
    success: function(data) {
    },
          error: function(error) {
                console.log(error);
                }
    });

}