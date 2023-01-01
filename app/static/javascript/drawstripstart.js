let socket = io();

function getMousePosition(canvas, event) {
    let rect = canvas.getBoundingClientRect();
    let x = event.clientX - rect.left;
    let y = event.clientY - rect.top;
    let xx = Math.round(x) * 2;
    let yy = Math.round(y) * 2;
    //console.log("Coordinate x: " + xx + 
    //            "Coordinate y: " + yy);

    const data = [(xx),(yy),strip_number];
    socket.emit("start_point_rec", data);
    }

let canvasElem = document.querySelector('canvas');

canvasElem.addEventListener("mousedown", function(e){
    getMousePosition(canvasElem, e);
});

socket.on('redirect', function(destination) {
    window.location.href = destination;
    console.log(destination)
});

var donedrawing = document.getElementById('donedrawing');
donedrawing.addEventListener('click', function(){
    
    var sel = document.querySelector('donedrawing');
    location.replace('/setup/' + strip_number);
});
