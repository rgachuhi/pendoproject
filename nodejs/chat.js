/**
 * 
 */
//var cookieParser = require('socket.io-cookie');
var http = require('http');
var server = http.createServer().listen(4000);
var io = require('/usr/local/lib/node_modules/socket.io')(server);
var cookie_reader = require('/usr/local/lib/node_modules/cookie');
var querystring = require('querystring');

var redis = require('/usr/local/lib/node_modules/redis');
var sub = redis.createClient();

//Subscribe to the Redis chat channel
sub.subscribe('chat');

io.sockets.on('connection', function (socket) {
    //Grab message from Redis and send to client
    sub.on('message', function(channel, message){
    	for(var i = 0; i<socket.rooms.length; i++){
    		console.log('Socket room ' + socket.rooms[i] + ' vs ' +socket.id);
    		if(socket.rooms[i] !== socket.id){
    			console.log('Sending message to room ' + socket.rooms[i]);
    			io.sockets.to(socket.rooms[i]).emit('chat', message);
    		}
    	}
    });
    
    socket.on('join_stream', function (message) {
    	for(var i = 0; i<socket.rooms.length; i++){
    		if(socket.rooms[i] !== socket.id){
    			console.log('leaving Socket room ' + socket.rooms[i]);
    			socket.leave(socket.rooms[i]);
    		}
    	}
    	console.log('Join Socket room ' + message);
    	socket.join(message);
    });
    
    /*socket.on('leave_stream', function (message) {
    	console.log('Leave Socket room ' + message);
    	socket.leave(message);
    });*/
    
   /* //Client is sending message through socket.io
    socket.on('send_message', function (message) {
    	//console.log('connection param on message : ' + socket.handshake.query.name);
        values = querystring.stringify({
            comment: message,
            sessionid: socket.id, //socket.handshake.cookie['sessionid'],
        });
        console.log('Socket Id: ' + socket.id);
        
        var options = {
            host: 'localhost',
            port: 8000,
            path: 'chat/chat_create',
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Content-Length': values.length
            }
        };
        
        //Send message to Django server
        var req = http.request(options, function(res){
            res.setEncoding('utf8');
            
            //Print out error message
            res.on('data', function(message){
                if(message != 'Everything worked :)'){
                    //console.log('Message: ' + message);
                }
            });
        });
        
        req.write(values);
        req.end();
    });*/
    
    socket.on('disconnect', function () {
    	//console.log('disconnection param : ' + socket.handshake.query.name);
    });
});