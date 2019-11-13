$(function() {
    $('#txtSearch').keyup(function() {
        $.ajax({
            url: SEARCH,
           data: {'search': document.getElementById('txtSearch').value,},
            type: 'GET',
            dataType: "json",
            success: function(data) {

                //data = JSON.parse(data[0]);
                //console.log(data[0].asset_name);
                $('#dropdownsearch').html('');
                for (i in data){
                     var profileImage = "/media/"+ data[i].profile_picture;
                $('#dropdownsearch').append(
                     '<li>' +
                               '<a href="/results?item='+data[i].name+'">' +
                                   '<div class="media">' +
                                        '<img src="' + profileImage +'" alt="" class="circle responsive-img" width="30" height="30">' +
                                        '<div class="media_body">' +
                                            '<p>'+ data[i].name +'</p>' +
                                            '<p><b>'+ data[i].city + '</b>' + ' ' + data[i].country +'</p>' +
                                        '</div>'+
                                   '</div>'+
                               '</a>'+
                            '</li>'
                    //console.log(data);
                );

                };
                $('#p').trigger("click");
            },
            error: function(error) {
                console.log(error);
            }
        });
    });
});




