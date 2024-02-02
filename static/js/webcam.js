const videoElement = document.getElementsByClassName('input_video')[0];
// Ocultar el video original usando CSS.
videoElement.style.display = "none";
const canvasElement = document.getElementsByClassName('output_canvas')[0];
const canvasCtx = canvasElement.getContext('2d');
const landmarkContainer = document.getElementsByClassName('landmark-grid-container')[0];
const grid = new LandmarkGrid(landmarkContainer);
// Checkbox for Mask
var maskOn = false;
// init variables
let goodFrames = 0;
let badFrames = 0;
let videoMetrics = [];

class Metrics {
  constructor() {
    this.timestamp = 0;
    this.leftShoulder = { x: 0, y: 0 };
    this.rightShoulder = { x: 0, y: 0 };
    this.leftElbow = { x: 0, y: 0 };
    this.leftWrist = { x: 0, y: 0 };
    this.leftHip = { x: 0, y: 0 };
    this.shouldersAligned = false;
    this.shoulderInclination = 0;
    this.elbowInclination = 0;
    this.goodPosture = false;
  }
}

function onResults(results) {
  if (!results.poseLandmarks) {
     grid.updateLandmarks([]);
    return;
  }
  // Put camera image con canva, apply optional mask
  canvasCtx.save();
  canvasCtx.clearRect(0, 0, canvasElement.width, canvasElement.height);
  if (maskOn) {
    canvasCtx.globalCompositeOperation = 'source-in';
    canvasCtx.drawImage(results.image, 0, 0,
                        canvasElement.width, canvasElement.height);

    canvasCtx.globalCompositeOperation = 'destination-atop';
    canvasCtx.fillStyle = '#000000';
    canvasCtx.fillRect(0, 0, canvasElement.width, canvasElement.height);
    
  } else {
    canvasCtx.globalCompositeOperation = 'destination-atop';
    canvasCtx.drawImage(
      results.image, 0, 0, canvasElement.width, canvasElement.height);
  }
  // Canvas setup for displaying metrics
  canvasCtx.globalCompositeOperation = 'source-over';
  
  // For debugging
  // if (counter == 30) {
  //   console.log(results)
  //   console.log(videoMetrics)
  // }
  // Run metrics calculations
  decantProcess(results.poseLandmarks, 270, 480)
  counter += 1;
  canvasCtx.restore();

   grid.updateLandmarks(results.poseWorldLandmarks);

  // Calculate the time of remaining in a particular posture (assuming 30 fps)
  goodTime = (1 / 30) * goodFrames
  badTime = (1 / 30) * badFrames

  // Pose time.
  if (goodTime > 0) {
    timeStringGood = 'Good Posture Time : ' + goodTime.toFixed(1).toString() + 's'
    canvasCtx.fillStyle = 'green'
    canvasCtx.fillText(timeStringGood, 10, 250);
  }   
  else {
    timeStringBad = 'Bad Posture Time : ' + badTime.toFixed(1).toString() + 's'
    canvasCtx.fillStyle = 'red'
    canvasCtx.fillText(timeStringBad, 10, 250);
  }
}

const pose = new Pose({locateFile: (file) => {
  return `https://cdn.jsdelivr.net/npm/@mediapipe/pose/${file}`;
}});
pose.setOptions({
  modelComplexity: 2,
  smoothLandmarks: true,
  enableSegmentation: true,
  smoothSegmentation: true,
  minDetectionConfidence: 0.5,
  minTrackingConfidence: 0.3
});
// call function on every pose results
pose.onResults(onResults);


function findDistance(x1, y1, x2, y2) {
  // Calculate the Euclidean distance between two points
  var dist = Math.sqrt((x2 - x1) * (x2 - x1) + (y2 - y1) * (y2 - y1));
  return dist;
}

function findAngle(x1, y1, x2, y2) {
  // Calculate the angle between two points with respect to the y-axis
  if (y1 == 0) {
      return 0
  }
  var theta = Math.acos((y2 - y1) * (-y1) / (Math.sqrt((x2 - x1) * (x2 - x1) + (y2 - y1) * (y2 - y1)) * y1));
  var degree = Math.round((180 / Math.PI) * theta);
  return degree;
}

function decantProcess(lm, 
  h, 
  w, 
  offsetThreshold=100, 
  shoulderAngleThreshold=[20,60], 
  elbowAngleThreshold=[60,100]) 
  { // Process frame metrics and display results on canva
  // Initialize metrics
  var frameMetrics = new Metrics();
  frameMetrics.timestamp = new Date().toISOString();

  // Left shoulder.
  frameMetrics.leftShoulder.x = parseInt(lm[POSE_LANDMARKS.LEFT_SHOULDER].x * w);
  frameMetrics.leftShoulder.y = parseInt(lm[POSE_LANDMARKS.LEFT_SHOULDER].y * h);

  // Right shoulder.
  frameMetrics.rightShoulder.x = parseInt(lm[POSE_LANDMARKS.RIGHT_SHOULDER].x * w);
  frameMetrics.rightShoulder.y = parseInt(lm[POSE_LANDMARKS.RIGHT_SHOULDER].y * h);

  // Left ELBOW.
  frameMetrics.leftElbow.x = parseInt(lm[POSE_LANDMARKS.LEFT_ELBOW].x * w);
  frameMetrics.leftElbow.y = parseInt(lm[POSE_LANDMARKS.LEFT_ELBOW].y * h);

  // Left WRIST.
  frameMetrics.leftWrist.x = parseInt(lm[POSE_LANDMARKS.LEFT_WRIST].x * w);
  frameMetrics.leftWrist.y = parseInt(lm[POSE_LANDMARKS.LEFT_WRIST].y * h);

  // Left hip.
  frameMetrics.leftHip.x = parseInt(lm[POSE_LANDMARKS.LEFT_HIP].x * w);
  frameMetrics.leftHip.y = parseInt(lm[POSE_LANDMARKS.LEFT_HIP].y * h);
  
  // Calculate distance between left shoulder and right shoulder points.
  const offset = findDistance(frameMetrics.leftShoulder.x, 
    frameMetrics.leftShoulder.y, 
    frameMetrics.rightShoulder.x, 
    frameMetrics.rightShoulder.y);

  // Assist to align the camera to point at the side view of the person.
  // Offset threshold 30 is based on results obtained from analysis over 100 samples.

  canvasCtx.font = '16px Hershey Simplex bold';  // Establece la fuente y el tamaño 
  if (offset < offsetThreshold) {
      canvasCtx.fillStyle = 'green'
      canvasCtx.fillText(`${parseInt(offset)} Shoulders aligned`, 320, 30);
      frameMetrics.shouldersAligned = true;
  } else {
      canvasCtx.fillStyle = 'red'
      canvasCtx.fillText(`${parseInt(offset)} Shoulders not aligned`, 300, 30);
      frameMetrics.shouldersAligned = false;
  }

  // Calculate angles.
  const shoulderInclination = findAngle(frameMetrics.leftElbow.x, 
    frameMetrics.leftElbow.y, 
    frameMetrics.leftShoulder.x, 
    frameMetrics.leftShoulder.y);
  frameMetrics.shoulderInclination = shoulderInclination;

  const elbowInclination = findAngle(frameMetrics.leftElbow.x, 
    frameMetrics.leftElbow.y, 
    frameMetrics.leftWrist.x, 
    frameMetrics.leftWrist.y);
  frameMetrics.elbowInclination = elbowInclination;

  // Draw landmarks.
  canvasCtx.beginPath();           // Begin a new path
  canvasCtx.arc(frameMetrics.leftShoulder.x, frameMetrics.leftShoulder.y, 7, 0, 2 * Math.PI);  // (x, y, radius, startAngle, endAngle)
  canvasCtx.fillStyle = 'white';    // Set the fill color
  canvasCtx.fill();                // Fill the circle
  canvasCtx.closePath();           // Close the path

  canvasCtx.beginPath();           
  canvasCtx.arc(frameMetrics.leftElbow.x, frameMetrics.leftElbow.y, 7, 0, 2 * Math.PI);
  canvasCtx.fill();                
  canvasCtx.closePath();     
  
  canvasCtx.beginPath();           
  canvasCtx.arc(frameMetrics.leftWrist.x, frameMetrics.leftWrist.y, 7, 0, 2 * Math.PI);
  canvasCtx.fill();      
  canvasCtx.closePath();   

  canvasCtx.beginPath();           
  canvasCtx.arc(frameMetrics.rightShoulder.x, frameMetrics.rightShoulder.y, 7, 0, 2 * Math.PI);
  canvasCtx.fillStyle = 'pink';
  canvasCtx.fill();                
  canvasCtx.closePath();   

  canvasCtx.beginPath();           
  canvasCtx.arc(frameMetrics.leftHip.x, frameMetrics.leftHip.y, 7, 0, 2 * Math.PI);
  canvasCtx.fillStyle = 'yellow'
  canvasCtx.fill();                
  canvasCtx.closePath();   

  // Put text, Posture and angle inclination.
  // Text string for display.
  const angleTextStringShoulder = `Shoulder inclination: ${shoulderInclination}`;
  const angleTextStringElbow = `Elbow inclination: ${elbowInclination}`;

  // Determine whether good posture or bad posture.
  if (elbowInclination < elbowAngleThreshold[1] && elbowInclination > elbowAngleThreshold[0]) {
      badFrames = 0;
      goodFrames += 1;
      frameMetrics.goodPosture = true;

      canvasCtx.fillStyle = 'lightgreen'
      canvasCtx.fillText(angleTextStringElbow, 10, 60);
      canvasCtx.fillText(`${parseInt(elbowInclination)}`, frameMetrics.leftElbow.x + 10, frameMetrics.leftElbow.y);
      
      canvasCtx.beginPath();         // Comienza un nuevo trazo
      canvasCtx.moveTo(frameMetrics.leftShoulder.x, frameMetrics.leftShoulder.y);      // Mueve el lápiz a la posición inicial (x, y)
      canvasCtx.lineTo(frameMetrics.leftElbow.x, frameMetrics.leftElbow.y);    // Dibuja una línea hasta la posición (x, y)
      canvasCtx.lineWidth = 2;       // Establece el ancho de la línea
      canvasCtx.strokeStyle = 'green';  // Establece el color de la línea
      canvasCtx.stroke();            // Dibuja la línea
      canvasCtx.closePath();    

      canvasCtx.beginPath();         
      canvasCtx.moveTo(frameMetrics.leftWrist.x, frameMetrics.leftWrist.y);     
      canvasCtx.lineTo(frameMetrics.leftElbow.x, frameMetrics.leftElbow.y);    
      canvasCtx.lineWidth = 2;       
      canvasCtx.strokeStyle = 'green';  
      canvasCtx.stroke();            
      canvasCtx.closePath();   
  } else {
      goodFrames = 0;
      badFrames += 1;
      frameMetrics.goodPosture = false;

      canvasCtx.fillStyle = 'red'
      canvasCtx.fillText(angleTextStringElbow, 10, 60);
      canvasCtx.fillText(`${parseInt(elbowInclination)}`, frameMetrics.leftElbow.x + 10, frameMetrics.leftElbow.y);

      canvasCtx.beginPath();         // Comienza un nuevo trazo
      canvasCtx.moveTo(frameMetrics.leftShoulder.x, frameMetrics.leftShoulder.y);      // Mueve el lápiz a la posición inicial (x, y)
      canvasCtx.lineTo(frameMetrics.leftElbow.x, frameMetrics.leftElbow.y);    // Dibuja una línea hasta la posición (x, y)
      canvasCtx.lineWidth = 2;       // Establece el ancho de la línea
      canvasCtx.strokeStyle = 'red';  // Establece el color de la línea
      canvasCtx.stroke();            // Dibuja la línea
      canvasCtx.closePath();    

      canvasCtx.beginPath();         
      canvasCtx.moveTo(frameMetrics.leftWrist.x, frameMetrics.leftWrist.y);     
      canvasCtx.lineTo(frameMetrics.leftElbow.x, frameMetrics.leftElbow.y);   
      canvasCtx.lineWidth = 2;       
      canvasCtx.strokeStyle = 'red';  
      canvasCtx.stroke();            
      canvasCtx.closePath();  
  }

  if (shoulderInclination > 0 && shoulderInclination < shoulderAngleThreshold[0]) {
      badFrames = 0;
      goodFrames += 1;
      frameMetrics.goodPosture = true;

      canvasCtx.fillStyle = 'lightgreen'
      canvasCtx.fillText(angleTextStringShoulder, 10, 30);
      canvasCtx.fillText(`${parseInt(shoulderInclination)}`, frameMetrics.leftShoulder.x + 10, frameMetrics.leftShoulder.y);

      canvasCtx.beginPath();         // Comienza un nuevo trazo
      canvasCtx.moveTo(frameMetrics.leftShoulder.x, frameMetrics.leftShoulder.y);      // Mueve el lápiz a la posición inicial (x, y)
      canvasCtx.lineTo(frameMetrics.leftElbow.x, frameMetrics.leftElbow.y);    // Dibuja una línea hasta la posición (x, y)
      canvasCtx.lineWidth = 2;       // Establece el ancho de la línea
      canvasCtx.strokeStyle = 'green';  // Establece el color de la línea
      canvasCtx.stroke();            // Dibuja la línea
      canvasCtx.closePath();    

      canvasCtx.beginPath();         
      canvasCtx.moveTo(frameMetrics.leftHip.x, frameMetrics.leftHip.y);     
      canvasCtx.lineTo(frameMetrics.leftShoulder.x, frameMetrics.leftShoulder.y);    
      canvasCtx.lineWidth = 2;       
      canvasCtx.strokeStyle = 'green';  
      canvasCtx.stroke();            
      canvasCtx.closePath();   

  } else if (shoulderInclination > shoulderAngleThreshold[0] && shoulderInclination < shoulderAngleThreshold[1]) {
      badFrames = 0;
      goodFrames += 1;
      frameMetrics.goodPosture = true;

      canvasCtx.fillStyle = 'yellow'
      canvasCtx.fillText(angleTextStringShoulder, 10, 30);
      canvasCtx.fillText(`${parseInt(shoulderInclination)}`, frameMetrics.leftShoulder.x + 10, frameMetrics.leftShoulder.y);

      canvasCtx.beginPath();         // Comienza un nuevo trazo
      canvasCtx.moveTo(frameMetrics.leftShoulder.x, frameMetrics.leftShoulder.y);      // Mueve el lápiz a la posición inicial (x, y)
      canvasCtx.lineTo(frameMetrics.leftElbow.x, frameMetrics.leftElbow.y);    // Dibuja una línea hasta la posición (x, y)
      canvasCtx.lineWidth = 2;       // Establece el ancho de la línea
      canvasCtx.strokeStyle = 'yellow';  // Establece el color de la línea
      canvasCtx.stroke();            // Dibuja la línea
      canvasCtx.closePath();    

      canvasCtx.beginPath();         
      canvasCtx.moveTo(frameMetrics.leftHip.x, frameMetrics.leftHip.y);     
      canvasCtx.lineTo(frameMetrics.leftShoulder.x, frameMetrics.leftShoulder.y);    
      canvasCtx.lineWidth = 2;       
      canvasCtx.strokeStyle = 'yellow';  
      canvasCtx.stroke();            
      canvasCtx.closePath();  

  } else {
      goodFrames = 0;
      badFrames += 1;
      frameMetrics.goodPosture = false;
    
      canvasCtx.fillStyle = 'red'
      canvasCtx.fillText(angleTextStringShoulder, 10, 30);
      canvasCtx.fillText(`${parseInt(shoulderInclination)}`, frameMetrics.leftShoulder.x + 10, frameMetrics.leftShoulder.y);
      
      canvasCtx.beginPath();         // Comienza un nuevo trazo
      canvasCtx.moveTo(frameMetrics.leftShoulder.x, frameMetrics.leftShoulder.y);      // Mueve el lápiz a la posición inicial (x, y)
      canvasCtx.lineTo(frameMetrics.leftElbow.x, frameMetrics.leftElbow.y);    // Dibuja una línea hasta la posición (x, y)
      canvasCtx.lineWidth = 2;       // Establece el ancho de la línea
      canvasCtx.strokeStyle = 'red';  // Establece el color de la línea
      canvasCtx.stroke();            // Dibuja la línea
      canvasCtx.closePath();    

      canvasCtx.beginPath();         
      canvasCtx.moveTo(frameMetrics.leftHip.x, frameMetrics.leftHip.y);     
      canvasCtx.lineTo(frameMetrics.leftShoulder.x, frameMetrics.leftShoulder.y);    
      canvasCtx.lineWidth = 2;       
      canvasCtx.strokeStyle = 'red';  
      canvasCtx.stroke();            
      canvasCtx.closePath();  
  }
  // Store frame metrics results
  videoMetrics.push(frameMetrics)
}

const camera = new Camera(videoElement, {
  onFrame: async () => {
    await pose.send({image: videoElement});
  },
  width: 480,
  height: 270
});
camera.start();