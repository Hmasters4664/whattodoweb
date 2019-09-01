function executeQuery() {
  $.ajax({
    url: FRIEND,
    type: 'GET',
    dataType: "json",
    success: function(data) {
      // do something with the return value here if you like
      var num = data.length;
      $('#fnumber').text(num);
      var link = "/pending";
      $('#dropdown4').html('');
      $('#dropdown_s1').html('');
      var holder1 = "circle responsive-img";
      var blank = "";
      var profileImage = "";
      var holder2 = "image img-cir img-40";
      var holder3 = "images/icon/avatar-04.jpg";
      var holder4 = "content";
      var holder5 = "time";
      $('#dropdown4').append(
          "<li class="+"hed_notic"+">" + "Friend Boo" + "<span><i class=" +"ion-ios-gear-outline"+ "></i></span></li>"
      );

      $('#dropdown_s1').append(
          "<li class="+"hed_notic"+">" + "Friend Boo" + "<span><i class=" +"ion-ios-gear-outline"+ "></i></span></li>"
      );

      for (i = 0; i < num; i++) {
        $('#dropdown4').append(
              "<li>" +
                               "<a href="+ "#" +">" +
                                   "<div class= "+ "media" + ">" +
                                        "<img src=" + profileImage + " alt= " + blank +  "class=" + holder1 + ">" +
                                        "<div class=" + "media_body"+ ">" +
                                            "<p><b>  " + data[i].from_user.profile.name +" </b> sent you a friend request.</p>" +
                                            "<div class=" +"btn_group"+">" +
                                                "<span class=" +"waves-effect follow_b"+">" + "Accept" +"</span>" +
                                                "<span class=" +"waves-effect "+">" + "Reject" +"</span>" +
                                            "</div>" +
                                        "</div>" +
                                   "</div>" +
                               "</a>" +
                            "</li>"
        );
           $('#dropdown_s1').append(
              "<li>" +
                               "<a href="+ "#" +">" +
                                   "<div class= "+ "media" + ">" +
                                        "<img src=" + profileImage + " alt= " + blank +  "class=" + holder1 + ">" +
                                        "<div class=" + "media_body"+ ">" +
                                            "<p><b>  " + data[i].from_user.profile.name +" </b> sent you a friend request.</p>" +
                                            "<div class=" +"btn_group"+">" +
                                                "<span class=" +"waves-effect follow_b"+">" + "Accept" +"</span>" +
                                                "<span class=" +"waves-effect "+">" + "Reject" +"</span>" +
                                            "</div>" +
                                        "</div>" +
                                   "</div>" +
                               "</a>" +
                            "</li>"
        );
      }

      $('#dropdown4').append(
          "<li><a href=" +"requests.html"+" class=" +"waves-effect chack_all_btn"+ ">" + "All Friend Request" + "</a></li>"
      );

      $('#dropdown_s1').append(
          "<li><a href=" +"requests.html"+" class=" +"waves-effect chack_all_btn"+ ">" + "All Friend Request" + "</a></li>"
      );




    },
    error: function(error) {
                console.log(error);
                }
  });
  setTimeout(executeQuery, 300000); // you could choose not to continue on failure...
}

$(document).ready(function() {
  // run the first time; all subsequent calls will take care of themselves
  setTimeout(executeQuery, 300);
});