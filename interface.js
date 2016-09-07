var app = require('express')();
var http = require('http').createServer(app);
var io = require('socket.io')(http);

app.get('/jquery', function(req,res){
	res.sendFile(__dirname+'/jquery-1.11.1.js');
});

app.get('/',function(req,res){
	res.sendFile(__dirname+'/interface.html');
});

io.on('connection', function(socket){
	socket.on('mousePositionChanged',function(msg){
		console.log(msg);
	});
});

http.listen(3000,function(){
});
