function searchEvent()
{
     $.ajax({
    headers: { "X-CSRFToken": csrf_token },
    url: Event,
    type: 'POST',
    dataType: "html",
    data: {
        'item': document.getElementById("evntSearch").value,
        'category': Cate
    },
    success: function(data) {
              $("#infinite_scroll").html(data);
    },
          error: function(error) {
                console.log(error);

                }
    });
}