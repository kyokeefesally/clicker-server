$(document).ready(function(){

    //connect to the socket server.
    var socketio = io.connect('http://' + document.domain + ':' + location.port);
    
    // on connect event handler
    socketio.on('connect', function() {
        socketio.emit('web_message', {web_message: 'hey'});
        console.log("I'm connected");
    });

    socketio.on('my_response', function(msg) {

        // console log message from server
        console.log(msg);

    });


});