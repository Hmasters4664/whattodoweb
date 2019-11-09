function executeQuery() {
  $.ajax({
    url: FRIENDCOUNT,
    type: 'GET',
    dataType: "json",
    success: function(data) {
      // do something with the return value here if you like

      if (Number(data)>0)
      {
        friends()
      }
       $('#fnumber').html(data);

    },
    error: function(error) {
                console.log(error);
                }
  });
  setTimeout(executeQuery, 300000); // you could choose not to continue on failure...
}
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
function friends() {
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

}
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
function executeQuery2() {
  $.ajax({
    url: NOTIFICATIONCOUNT,
    type: 'GET',
    dataType: "json",
    success: function(data) {
       if (Number(data)>0)
      {
        notification()
      }
       $('#Nnumber').html(data);
    },
    error: function(error) {
                console.log(error);
                }
  });
  setTimeout(executeQuery2, 300000); // you could choose not to continue on failure...
}
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
function notification() {
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

}
/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
function executeQuery3() {
  $.ajax({
    url: MESSAGECOUNT,
    type: 'GET',
    dataType: "json",
    success: function(data) {
      // do something with the return value here if you like
      if (Number(data)>0)
      {
        message()
      }
       $('#Mnumber').html(data);

    },
    error: function(error) {
                console.log(error);
                }
  });
  setTimeout(executeQuery3, 300000); // you could choose not to continue on failure...
}
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
function message(){
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
}


$(document).ready(function() {
  // run the first time; all subsequent calls will take care of themselves
  setTimeout(executeQuery, 100);
  setTimeout(executeQuery2, 200);
  setTimeout(executeQuery3, 300);

});