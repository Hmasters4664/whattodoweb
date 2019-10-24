function executeQuery() {
  $.ajax({
    url: FRIEND,
    type: 'GET',
    dataType: "html",
    success: function(data) {
      // do something with the return value here if you like

      $('#dropdown4').html(data);
      $('#dropdown_s1').html(data);


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
      $('#dropdown2').html(data);
      $('#dropdown_s3').html(data);

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
      var val = "/messageview"

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
                                        '<img src="'+ profileImage +'" alt="" class="circle responsive-img">' +
                                        '<div class="media_body">' +
                                            '<h4>'+ data[i].from_user__profile__name + '<small>'+ data[i].created +'</small><h4>' +
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
                                        '<img src="'+ profileImage +'" alt="" class="circle responsive-img">' +
                                        '<div class="media_body">' +
                                            '<h4>'+ data[i].from_user__profile__name + '<small>'+ data[i].created +'</small><h4>' +
                                            ' <p>' + data[i].text + '</p>' +
                                        '</div>'+
                                   '</div>'+
                               '</a>'+
                            '</li>'
        );
      }

         $('#dropdown3').append(
          '<li><a href="' + val + '" class="' + holder4 + '" >' + "Messages" + '</a></li>'
      );
             $('#dropdown_s2').append(
          '<li><a href="' + val + '" class="' + holder4 + '" >' + "Messages" + '</a></li>'
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