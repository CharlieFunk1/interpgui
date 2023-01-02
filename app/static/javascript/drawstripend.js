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
    socket.emit("end_point_rec", data);
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

document.onkeydown = checkKey;

function checkKey(e) {

    e = e || window.event;

    if (e.keyCode == '38' && e.altKey == false) {
        // up arrow
	fetch('/nudge_up/url/' + strip_number + '/' + 10 + '/' + "end").then(response => window.location = response.url);
    }
    else if (e.keyCode == '38' && e.altKey == true) {
	//ctrl + up arrow
	fetch('/nudge_up/url/' + strip_number + '/' + 1 + '/' + "end").then(response => window.location = response.url);
    }
    else if (e.keyCode == '40' && e.altKey == false) {
        // down arrow
	fetch('/nudge_down/url/' + strip_number + '/' + 10 + '/' + "end").then(response => window.location = response.url);
    }
    else if (e.keyCode == '40' && e.altKey == true) {
	//ctrl + down arrow
	fetch('/nudge_down/url/' + strip_number + '/' + 1 + '/' + "end").then(response => window.location = response.url);
    }
    else if (e.keyCode == '37' && e.altKey == false) {
        // left arrow
	fetch('/nudge_left/url/' + strip_number + '/' + 10 + '/' + "end").then(response => window.location = response.url);
    }
    else if (e.keyCode == '37' && e.altKey == true) {
	//ctrl + left arrow
	fetch('/nudge_left/url/' + strip_number + '/' + 1 + '/' + "end").then(response => window.location = response.url);
    }
    else if (e.keyCode == '39' && e.altKey == false) {
        // right arrow
	fetch('/nudge_right/url/' + strip_number + '/' + 10 + '/' + "end").then(response => window.location = response.url);
    }
    else if (e.keyCode == '39' && e.altKey == true) {
	//ctrl + right arrow
	fetch('/nudge_right/url/' + strip_number + '/' + 1 + '/' + "end").then(response => window.location = response.url);
    }

}


