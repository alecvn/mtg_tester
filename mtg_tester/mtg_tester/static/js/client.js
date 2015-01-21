var socket = new io.Socket();

socket.connect();

socket.on('connect', function(a) {
  socket.subscribe("my_channel");
});

socket.on('message', function(data) {
  if (data != null) {
    if (data['message'] != null) {
//      broadcast_message(data['message']);
    }
    if (data['card_drawn'] != null) {
      broadcast_message(data['card_drawn'], data['idx']);
    }
  }
});
