function Evntselect()
{
     $.ajax({
    headers: { "X-CSRFToken": csrf_token },
    url: EventSelect,
    type: 'POST',
    dataType: "html",
    data: {
        'city': city,
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