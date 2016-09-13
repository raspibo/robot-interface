var app = require('express')();
var http = require('http').createServer(app);
var io = require('socket.io')(http);

app.get('/jquery', function(req,res){			//only if jquery is
	res.sendFile(__dirname+'/jquery-1.11.1.js');	//stored locally
});

app.get('/mouse.html',function(req,res){
	res.sendFile(__dirname+'/mouse.html');	//mouse reader
});

app.get('/joystick.html',function(req,res){
	res.sendFile(__dirname+'/joystick.html');
});

app.get('/*',function(req,res){
	res.sendFile(__dirname+'/index.html');
});

io.on('connection', function(socket){
	socket.on('mousePositionChanged',function(msg){ //output in stdout
		console.log(msg);
	});
});

io.on('connection', function(socket){
	socket.on('joyMoved',function(msg){ //output in stdout
		console.log(msg);
	});
});

http.listen(3000,function(){
});
