
var firebaseConfig = {
    apiKey: "AIzaSyCq6uALYLbOA2Yg4OiBdG809k6Bdt62gck",
    authDomain: "whattodo-73491.firebaseapp.com",
    databaseURL: "https://whattodo-73491.firebaseio.com",
    projectId: "whattodo-73491",
    storageBucket: "",
    messagingSenderId: "734162391132",
    appId: "1:734162391132:web:26784556d1ce7fcf901699"
  };

  // Initialize Firebase
  firebase.initializeApp(firebaseConfig);
  var firestore = firebase.firestore();

  const docRef = firestore.collection("chats/conversations/"+document.getElementById("chatroom").value );

  function loadChats(){

      docRef.get().then(function(querySnapshot) {
           $('#mess').val('')
        querySnapshot.forEach(function(doc) {
            // doc.data() is never undefined for query doc snapshots
            const data = doc.data();
             const dt = data.time;
                if (data.id === document.getElementById("other").value ) {
                    $('<div class="sms"><p>' + data.message + '</p><h6>' + dt + '</h6></div>').insertBefore('.type_messages');
                } else {
                    $('<div class="sms_right"><p>' + data.message + '</p><h6>' + dt + '</h6></div>').insertBefore('.type_messages');
                }

        });
        console.log("Got the  documents");
    })
    .catch(function(error) {
        console.log("Error getting documents: ", error);
    });

  }

//$(document).ready(loadChats);

getRealTimeUpdates= function() {

    docRef.orderBy('seconds').onSnapshot(function (querySnapshot) {
        querySnapshot.docChanges().forEach(function (change) {
            if (change.type === "added") {
                const data = change.doc.data();
                const dt = data.time;
                if (data.id === document.getElementById("other").value ) {
                    $('<div class="sms"><p>' + data.message + '</p><h6>' + dt + '</h6></div>').insertBefore('.type_messages');
                } else {
                    $('<div class="sms_right"><p>' + data.message + '</p><h6>' + dt + '</h6></div>').insertBefore('.type_messages');
                }
            }

        });


    });
}

function Save(){
     var dt = Date($.now());
   var now = $.now();

    docRef.add({
    message: $('#mess').val(),
    id: document.getElementById("me").value,
    time: dt,
    seconds: now
})
.then(function(docRef) {
    console.log("Document written with ID: ", docRef.id);
    sendNotification()
})
.catch(function(error) {
    console.error("Error adding document: ", error);
});


}


function sendNotification(){
       var dt = Date($.now());
   var now = $.now()/1000;
      $.ajax({
          headers: { "X-CSRFToken": csrf_token },
    url: "/send",
    type: 'POST',
    dataType: "json",
    data: {
        'message'  : $('#mess').val(),
        'id': document.getElementById("other").value,
        'time' : now
    },
    success: function(data) {
              console.log("sent");

            $('#mess').val('')

            $('#mess').focus()



    },
          error: function(error) {
                console.log(error);

                }
    });

}


getRealTimeUpdates();