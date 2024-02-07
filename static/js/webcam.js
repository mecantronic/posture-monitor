const videoElement = document.getElementsByClassName('input_video')[0];
const canvasElement = document.getElementsByClassName('output_canvas')[0];
const canvasCtx = canvasElement.getContext('2d');
const landmarkContainer = document.getElementsByClassName('landmark-grid-container')[0];
const grid = new LandmarkGrid(landmarkContainer);

// Ocultar el elemento <video> al inicio
videoElement.style.display = 'none';

let previousTimestamp = 0;
const fpsList = [];
let frameCounter = 0;  // Contador de fotogramas

function onResults(results) {
  // Calcular FPS
  const timestamp = Date.now();
  const deltaTime = timestamp - previousTimestamp;
  const fps = 1000 / deltaTime;
  fpsList.push(fps);
  previousTimestamp = timestamp;

  // Incrementar el contador de fotogramas
  frameCounter++;

  // console.log(`FPS: ${fps.toFixed(1)}`); FPS instantaneos

  if (!results.poseLandmarks) {
     grid.updateLandmarks([]);
    return;
  }
  if (frameCounter % 2 === 0) {  // Actualizar cada 5 fotogramas (ajustable según sea necesario)
    // Aplicar mirror horizontal a videoElement
    videoElement.style.transform = 'scaleX(-1)';  

    canvasCtx.save();
    canvasCtx.clearRect(0, 0, canvasElement.width, canvasElement.height);

    // Aplicar mirror horizontal a canvasElement
    canvasCtx.scale(-1, 1);
    canvasCtx.translate(-canvasElement.width, 0);

    // Agrega la SegmentationMasks
    //canvasCtx.drawImage(results.segmentationMask, 0, 0,
    //                    canvasElement.width, canvasElement.height);

    // Agrega un fondo negro al lienzo
    canvasCtx.fillStyle = 'black'; // Puedes cambiar 'black' por cualquier color de fondo que desees
    canvasCtx.fillRect(0, 0, canvasElement.width, canvasElement.height);

    // Only overwrite existing pixels.
    canvasCtx.globalCompositeOperation = 'source-in';
    canvasCtx.fillStyle = 'black';
    canvasCtx.fillRect(0, 0, canvasElement.width, canvasElement.height);

    // Only overwrite missing pixels.
    canvasCtx.globalCompositeOperation = 'destination-atop';
    canvasCtx.drawImage(
        results.image, 0, 0, canvasElement.width, canvasElement.height);
    
    canvasCtx.globalCompositeOperation = 'source-over';
    drawConnectors(canvasCtx, results.poseLandmarks, POSE_CONNECTIONS,
                  {color: '#FF0000', lineWidth: 3});
    drawLandmarks(canvasCtx, results.poseLandmarks,
                  {color: '#FFFFFF', lineWidth: 2});
    canvasCtx.restore();

    //grid.updateLandmarks(results.poseWorldLandmarks);
    frameCounter = 0;  // Reiniciar el contador de fotogramas
  }
}

function calculateAverageFPS() {
  if (fpsList.length === 0) {
    console.log("No FPS data available.");
    return;
  }

  const sum = fpsList.reduce((acc, fps) => acc + fps, 0);
  const averageFPS = sum / fpsList.length;
  console.log(`Average FPS: ${averageFPS.toFixed(1)}`);
}

const pose = new Pose({locateFile: (file) => {
  return `https://cdn.jsdelivr.net/npm/@mediapipe/pose/${file}`;
}});
pose.setOptions({
  modelComplexity: 0,  // Complexity of the pose landmark model: 0, 1 or 2. Default: 1.
  static_image_mode: false, // The solution threats the input images as a video stream. Default: False.
  runningMode: "VIDEO",
  numPoses: 1,  // The maximum number of poses that can be detected by the Pose Landmarker.  
  smoothLandmarks: true,  // The solution filters pose landmarks across different input images to reduce jitter. Default: True.
  enableSegmentation: true,  // In addition to the pose landmarks the solution also generates the segmentation mask. Default: False.
  smoothSegmentation: true,  // The solution filters pose landmarks across different input images to reduce jitter. Default: True.
  minDetectionConfidence: 0.5,  // Minimum confidence value ([0.0, 1.0]) from the person-detection model for the detection to be considered successful. Default to 0.5.
  minTrackingConfidence: 0.2,  // Minimum confidence value ([0.0, 1.0]) from the landmark-tracking model for the pose landmarks to be considered tracked successfully.  Setting it to a higher value can increase robustness of the solution, at the expense of a higher latency. Default to 0.5.
  outputSegmentationMasks: false  // Whether Pose Landmarker outputs a segmentation mask for the detected pose.
});
pose.onResults(onResults);

const camera = new Camera(videoElement, {
  onFrame: async () => {
    await pose.send({image: videoElement});
  },
  width: 720,
  height: 480,
  videoMirror: false
});

// Iniciar el cálculo del promedio después de unos segundos
setTimeout(() => {
  setInterval(calculateAverageFPS, 2000); // Calcular el promedio cada 5 segundos
}, 2000);

camera.start();