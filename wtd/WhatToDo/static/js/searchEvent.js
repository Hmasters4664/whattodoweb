function searchEvent()
{
     $.ajax({
          headers: { "X-CSRFToken": csrf_token },
    url: "/main",
    type: 'POST',
    dataType: "html",
    data: {
        'name': document.getElementById("evntSearch").value,
    },
    success: function(data) {
              $("html").html(data);
    },
          error: function(error) {
                console.log(error);

                }
    });
}