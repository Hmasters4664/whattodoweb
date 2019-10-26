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
    dataType: "html",
    success: function(data) {
      // do something with the return value here if you like
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
    dataType: "html",
    success: function(data) {
      // do something with the return value here if you like
      $('#dropdown3').html(data);
      $('#dropdown_s2').html(data);

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