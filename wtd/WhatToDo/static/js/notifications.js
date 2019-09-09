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
      var holder2 = "image img-cir img-40";
      var holder3 = "waves-effect follow_b";
      var holder4 = "waves-effect chack_all_btn";
      var holder5 = "time";
      $('#dropdown4').append(
          "<li class="+"hed_notic"+">" + "Friend Requests" + "<span><i class=" +"ion-ios-gear-outline"+ "></i></span></li>"
      );

      $('#dropdown_s1').append(
          "<li class="+"hed_notic"+">" + "Friend Requests" + "<span><i class=" +"ion-ios-gear-outline"+ "></i></span></li>"
      );
      if (num > 5) {
        num = 5;
      }
      for (var i = 0; i < num; i++) {
        var profileImage = "/media/"+data[i].from_user__profile__profile_picture;
        $('#dropdown4').append(
              "<li>" +
                               "<a href="+ "#" +">" +
                                   "<div class= "+ "media" + ">" +
                                        "<img src=" + profileImage + " alt= " + blank +  "class=" + holder1 + ">" +
                                        "<div class=" + "media_body"+ ">" +
                                            "<p><b> " + data[i].action +"</b></p>" +
                                            "<div class=" +"btn_group"+">" +
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
                                            "<p><b> " + data[i].action +"</b></p>" +
                                            "<div class=" +"btn_group"+">" +
                                            "</div>" +
                                        "</div>" +
                                   "</div>" +
                               "</a>" +
                            "</li>"
        );
      }
      var val = "/allrequests"

      $('#dropdown4').append(
          '<li><a href="' + val + '" class="' + holder4 + '" >' + "All Friend Request" + '</a></li>'

      );


      $('#dropdown_s1').append(
         '<li><a href="' + val + '" class="' + holder4 + '" >' + "All Friend Request" + '</a></li>'
      );




    },
    error: function(error) {
                console.log(error);
                }
  });
  setTimeout(executeQuery, 300000); // you could choose not to continue on failure...
}

function executeQuery2() {
  $.ajax({
    url: NOTIFICATION,
    type: 'GET',
    dataType: "json",
    success: function(data) {
      // do something with the return value here if you like
      var num = data.length;
      $('#Nnumber').text(num);
      var link = "/pending";
      $('#dropdown2').html('');
         $('#dropdown_s3').html('');
      var holder1 = "circle responsive-img";
      var blank = "";
      var holder4 = "waves-effect chack_all_btn";
      var val = "/allnotifications"

      $('#dropdown2').append(
          "<li class="+"hed_notic"+">" + "Notifications" + "<span><i class=" +"ion-ios-gear-outline"+ "></i></span></li>"
      );
      $('#dropdown_s3').append(
          "<li class="+"hed_notic"+">" + "Notifications" + "<span><i class=" +"ion-ios-gear-outline"+ "></i></span></li>"
      );
       if (num > 5) {
        num = 5;
      }
      for (var i = 0; i < num; i++) {
        var profileImage = "/media/"+data[i].from_user__profile__profile_picture;
        $('#dropdown2').append(
               '<li>' +
                               '<a href="#">' +
                                   '<div class="media">' +
                                        '<img src="images/profile-1.jpg" alt="" class="circle responsive-img">' +
                                        '<div class="media_body">' +
                                            '<p><b> ' + data[i].action +'</b></p>' +
                                            '<h6>' + data[i].created + '</h6>' +
                                        '</div>'+
                                   '</div>'+
                               '</a>'+
                            '</li>'
        );
            $('#dropdown_s3').append(
               '<li>' +
                               '<a href="#">' +
                                   '<div class="media">' +
                                        '<img src="images/profile-1.jpg" alt="" class="circle responsive-img">' +
                                        '<div class="media_body">' +
                                            '<p><b> ' + data[i].action +'</b></p>' +
                                            '<h6>' + data[i].created + '</h6>' +
                                        '</div>'+
                                   '</div>'+
                               '</a>'+
                            '</li>'
        );
      };

         $('#dropdown2').append(
          '<li><a href="' + val + '" class="' + holder4 + '" >' + "Notifications" + '</a></li>'
      );
             $('#dropdown_s3').append(
          '<li><a href="' + val + '" class="' + holder4 + '" >' + "Notifications" + '</a></li>'
      );

    },
    error: function(error) {
                console.log(error);
                }
  });
  setTimeout(executeQuery2, 300000); // you could choose not to continue on failure...
}


function executeQuery3() {
  $.ajax({
    url: MESSAGE,
    type: 'GET',
    dataType: "json",
    success: function(data) {
      // do something with the return value here if you like
      var num = data.length;
      $('#Mnumber').text(num);
      var link = "/pending";
      $('#dropdown3').html('');
         $('#dropdown_s2').html('');
      var holder1 = "circle responsive-img";
      var blank = "";
      var holder4 = "waves-effect chack_all_btn";
      var val = "requests.html"

      $('#dropdown3').append(
          "<li class="+"hed_notic"+">" + "Notifications" + "<span><i class=" +"ion-ios-gear-outline"+ "></i></span></li>"
      );
      $('#dropdown_s2').append(
          "<li class="+"hed_notic"+">" + "Notifications" + "<span><i class=" +"ion-ios-gear-outline"+ "></i></span></li>"
      );
       if (num > 5) {
        num = 5;
      }
      for (var i = 0; i < num; i++) {
        var profileImage = "/media/"+data[i].from_user__profile__profile_picture;
        $('#dropdown3').append(
               '<li>' +
                               '<a href="#">' +
                                   '<div class="media">' +
                                        '<img src="images/profile-1.jpg" alt="" class="circle responsive-img">' +
                                        '<div class="media_body">' +
                                            '<h4>'+ data[i].from_user.profile.name + '<small>'+ data[i].created +'</small><h4>' +
                                            ' <p>' + data[i].text + '</p>' +
                                        '</div>'+
                                   '</div>'+
                               '</a>'+
                            '</li>'
        );
            $('#dropdown_s2').append(
               '<li>' +
                               '<a href="#">' +
                                   '<div class="media">' +
                                        '<img src="images/profile-1.jpg" alt="" class="circle responsive-img">' +
                                        '<div class="media_body">' +
                                            '<h4>'+ data[i].from_user.profile.name + '<small>'+ data[i].created +'</small><h4>' +
                                            ' <p>' + data[i].text + '</p>' +
                                        '</div>'+
                                   '</div>'+
                               '</a>'+
                            '</li>'
        );
      };

         $('#dropdown3').append(
          '<li><a href="' + val + '" class="' + holder4 + '" >' + "Messages" + '</a></li>'
      );
             $('#dropdown_s2').append(
          '<li><a href="' + val + '" class="' + holder4 + '" >' + "Notifications" + '</a></li>'
      );

    },
    error: function(error) {
                console.log(error);
                }
  });
  setTimeout(executeQuery3, 300000); // you could choose not to continue on failure...
}




$(document).ready(function() {
  // run the first time; all subsequent calls will take care of themselves
  setTimeout(executeQuery, 100);
  setTimeout(executeQuery2, 200);
  setTimeout(executeQuery3, 300);

});