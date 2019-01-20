const canvas = document.createElement('canvas')
const config = {
    canvas: {
        height: 480,
        width: 640
    },
}
canvas.height = config.canvas.height
canvas.width = config.canvas.width
document.getElementById('mainCanvasContainer').append(canvas)
let ctx = canvas.getContext('2d')
let targetLabel = "all";
// ctx.fillStyle = 'red'
// ctx.fillRect(0, 0, canvas.width, canvas.height)
//A list of all object classes detected by YOLO
let labels = ["car", "person", "bicycle", "motorbike", "aeroplane", "bus", "train", "truck", "boat", "traffic light", "cat", "dog", "stop sign", "parking meter", "backpack", "bottle", "cup", "laptop", "mouse", "remote", "keyboard", "cell phone", "microwave", "oven", "toaster", "sink", "refrigerator", "book", "clock", "vase", "scissors", "teddy bear", "hair drier", "toothbrush"]


function populateDropdown(labels) {
    let drop_down = document.getElementById("objectSelect");
    drop_down.setAttribute("style", "");
    for (let i = 0; i < labels.length; ++i) {
        let label = labels[i];
        let option = document.createElement("option");
        option.setAttribute("value", label);
        option.innerHTML = label;

        drop_down.appendChild(option);
    }
}

function updateValues(predictions) {
    let cars = 0;
    let pedestrians = 0;
    let target = 0;
    let cycles = 0;
    for (let i = 0; i < predictions.length; ++i) {
        prediction = predictions[i];
        if (prediction.label === "car") {
            ++cars;
        }
        else if (prediction.label === "person") {
            ++pedestrians;
        }
        else if (prediction.label === targetLabel) {
            ++target;
        }
        else if (prediction.label === "bicycle") {
            ++cycles;
        }
    }
    document.getElementById("carCount").innerHTML = cars;
    document.getElementById("pedestrianCount").innerHTML = pedestrians;
    document.getElementById("selectedObjectCount").innerHTML = target;
    document.getElementById("cycleCount").innerHTML = cycles;

    //Updating the progress bars
    vehicleBar = document.getElementById("vehicleCount");
    pedestrianBar = document.getElementById("pedestrianCount");
    pedestrianBar2 = document.getElementById("pedestrianBar");
    vehicleBar2 = document.getElementById("vehicleBar");
    vehicleText = vehicleBar.querySelector("div");
    vehicleText.innerHTML = cars + " vehicles";
    vehicleBar2.style.width= (cars * 4) + "%"
    pedestrianText = document.getElementById("pedText");
    pedestrianText.innerHTML = pedestrians + " pedestrians";
    pedestrianBar2.style.width= (pedestrians * 5) + "%";
}


function Speech2Text() {

}

function Speech2TextInit() {
    var SpeechRecognition = SpeechRecognition || webkitSpeechRecognition
    var SpeechGrammarList = SpeechGrammarList || webkitSpeechGrammarList
    var SpeechRecognitionEvent = SpeechRecognitionEvent || webkitSpeechRecognitionEvent
    var grammar = '#JSGF V1.0; grammar labels; public <label> = ' + labels.join(' | ') + ' ;'
    var recognition = new SpeechRecognition();
    var speechRecognitionList = new SpeechGrammarList();
    recognition.grammars = speechRecognitionList;
    //recognition.continuous = false;
    recognition.lang = 'en-US';
    recognition.interimResults = false;
    recognition.maxAlternatives = 1;
    document.querySelector('#micContainer').onclick = function () {
        recognition.start();
        console.log('Ready to receive a color command.');
    }
    recognition.onresult = function (event) {
        var last = event.results.length - 1;
        var label = event.results[last][0].transcript;
        document.querySelector('#input-normal').value = label;
        targetLabel = label;
    }
}

//Function to initialize the main front-end
function init() {
    populateDropdown(labels);
    Speech2TextInit()
    //TODO: Add socket initialization
}

//Function to start processing all the video files

//Initializing the value
init();

function drawOneBox(prediction) {
    let x1 = prediction['topleft']['x'];
    let y1 = prediction['topleft']['y'];
    let x2 = prediction['bottomright']['x'];
    let y2 = prediction['bottomright']['y'];
    ctx.beginPath();
    ctx.strokeStyle = "white";
    ctx.lineWidth = Number(prediction.confidence * 10);
    ctx.strokeRect(x1, y1, x2 - x1, y2 - y1);
    ctx.font = "30px Arial";
    ctx.fillStyle = "white";
    ctx.fillText(prediction.label, (x1 + x2) / 2, y1 - 20);
}

function DrawBoxes(predictions) {
    let allLabels = true;
    if (targetLabel !== "all") {
        allLabels = false;
    }
    for (let i = 0; i < predictions.length; ++i) {
        if (predictions[i].label === targetLabel) {
            drawOneBox(predictions[i]);
        }
        else if (allLabels) {
            drawOneBox(predictions[i]);
        }
    }
}

document.querySelector('#resetBtn').onclick = ()=>{
    targetLabel = 'all'
}

document.querySelector('#objectSelect').onchange = (e)=>{
    targetLabel =  e.target.value
}

function drawImage(blob, predictions) {
    let img = new Image()
    img.onload = function () {
        ctx.drawImage(img, 0, 0)
        DrawBoxes(predictions)
    }
    img.src = blob
}


var socket = io.connect('http://127.0.0.1:5000');
socket.on('connect', function () {
    console.log('connected!');
    socket.emit('my event', { data: 'I\'m connected!' });
});
socket.on('send_image', function (message) {
    blob = 'data:image/jpeg;base64,' + String.fromCharCode.apply(null, new Uint8Array(message['image']));
    predictions = JSON.parse((message['result']).replace(/'/g, '"'))
    updateValues(predictions)
    drawImage(blob, predictions);
});
socket.connect();
