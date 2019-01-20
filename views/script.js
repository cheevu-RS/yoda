const config = {
  canvas: {
    height: 416,
    width: 416
  },
  serverURL: 'ws://127.0.0.1:8000'
}

const canvas = document.createElement('canvas')
canvas.height = config.canvas.height
canvas.width = config.canvas.width
document.getElementById('canvasContainer').append(canvas)
let ctx = canvas.getContext('2d')

ctx.fillStyle = 'red'
ctx.fillRect(0, 0, canvas.width, canvas.height)

canvas.toBlob((blob) => {
  console.log('​blob', blob)
  drawImage(blob)
})

function drawImage (blob) {
  let img = new Image()
  img.onload = function () {
    ctx.drawImage(img, 0, 0)
  }
  img.src = blob
  console.log(img.src);
}

// const socket = new WebSocket(config.serverURL)
// socket.onopen = (e) => {
//   console.log('​socket.onopen -> e', e)
//   console.log('connection established')
//   socket.send("tha dei oodu")
// }

// socket.onmessage = (e) => {
//   console.log('​socket.onmessage -> e', e)
//   socket.send("hahaha")
//   drawImage(e.data)
// }
// socket.onerror = (e) => {
//   console.log('Error'+JSON.stringify(e));
// }
// socket.onclose = (e) => {
//   console.log('closed')
// }
function str2ab(str) {
  var buf = new ArrayBuffer(str.length * 2); // 2 bytes for each char
  var bufView = new Uint16Array(buf);
  for (var i = 0, strLen = str.length; i < strLen; i++) {
    bufView[i] = str.charCodeAt(i);
  }
  return buf;
}

var socket = io.connect('http://127.0.0.1:5000');
    socket.on('connect', function() {
        console.log('connected!');
        socket.emit('my event', {data: 'I\'m connected!'});
      });
    // socket.on('message',function(message){
    // });
    socket.on('send_image',function(message){

      blob = 'data:image/jpeg;base64,'+String.fromCharCode.apply(null, new Uint8Array(message['image']));
      drawImage(blob);
    });
    socket.connect();
    