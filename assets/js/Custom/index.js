//A list of all object classes detected by YOLO
let labels = ["car", "person", "bicycle", "motorbike", "aeroplane", "bus", "train", "truck", "boat", "traffic light", "cat", "dog", "stop sign", "parking meter", "backpack", "bottle", "cup", "laptop", "mouse", "remote", "keyboard", "cell phone", "microwave", "oven", "toaster", "sink", "refrigerator", "book", "clock", "vase", "scissors", "teddy bear", "hair drier", "toothbrush"]

function createCanvas(){
    let canvas_container = document.getElementById("mainCanvasContainer");
    let canvas = document.createElement("canvas");
    canvas.setAttribute("width", 640);
    canvas.setAttribute("height", 480);
    canvas_container.appendChild(canvas);
}

function populateDropdown(labels){
    let drop_down = document.getElementById("objectSelect");
    drop_down.setAttribute("style", "");
    for (let i = 0; i < labels.length; ++i){
        let label = labels[i];
        let option = document.createElement("option");
        option.setAttribute("value", label);
        option.innerHTML = label;

        drop_down.appendChild(option);
    }
}

function updateValues(predictions, target_label){
    let cars = 0;
    let pedestrians = 0;
    let target = 0;
    let cycles = 0;
    for(let i = 0; i < predictions.length; ++i){
        prediction = predictions[i];
        console.log(prediction)
        if(prediction.label === "car"){
            ++cars;
        }
        else if(prediction.label === "person"){
            ++pedestrians;
        }
        else if(prediction.label === target_label){
            ++target;
        }
        else if (prediction.label === "bicycle"){
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
    vehicleBar2.setAttribute("width", (cars * 4) + "%")
    pedestrianText = document.getElementById("pedText");    
    pedestrianText.innerHTML = pedestrians + " pedestrians";
    pedestrianBar2.setAttribute("width", (pedestrians * 4) + "%"); 
}


function Speech2Text(){

}

//Function to initialize the main front-end
function init(){
    createCanvas();
    populateDropdown(labels);
    //TODO: Add socket initialization
}

//Function to start processing all the video files

//Initializing the value
init();




