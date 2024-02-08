const videoElement = document.querySelector('.input_video');
const canvasElement = document.querySelector('.output_canvas');
const canvasCtx = canvasElement.getContext('2d');
const landmarkContainer = document.querySelector('.landmark-grid-container');
const grid = new LandmarkGrid(landmarkContainer);
const fpsDisplayElement = document.getElementById('fpsDisplay');

// Ocultar el elemento <video> al inicio
videoElement.style.display = 'none';

let previousTimestamp = 0;
const fpsList = [];
let frameCounter = 0;  // Contador de fotogramas

let mirrored = false;

function onResults(results) {
  // Calcular FPS
  const timestamp = performance.now();
  const deltaTime = timestamp - previousTimestamp;
  const fps = 1000 / deltaTime;
  fpsList.push(fps);
  previousTimestamp = timestamp;

  // Incrementar el contador de fotogramas
  frameCounter += 1;

  if (!results.poseLandmarks) {
    // ... Actualización de puntos de referencia ...
    return;
  }

  if (frameCounter % 1 === 0) {
    // Aplicar "mirror" solo una vez
    if (!mirrored) {
      mirrorElements();
      mirrored = true;
    }

    canvasCtx.clearRect(0, 0, canvasElement.width, canvasElement.height);
    canvasCtx.fillStyle = 'black';
    canvasCtx.fillRect(0, 0, canvasElement.width, canvasElement.height);
    canvasCtx.drawImage(results.image, 0, 0, canvasElement.width, canvasElement.height);

    canvasCtx.globalCompositeOperation = 'source-over';
    drawConnectors(canvasCtx, results.poseLandmarks, POSE_CONNECTIONS, { color: '#FF0000', lineWidth: 3 });
    drawLandmarks(canvasCtx, results.poseLandmarks, { color: '#FFFFFF', lineWidth: 2 });

    frameCounter = 0;
  }
}

function mirrorElements() {
  videoElement.style.transform = 'scaleX(-1)';
  canvasCtx.scale(-1, 1);
  canvasCtx.translate(-canvasElement.width, 0);
}

function calculateAverageFPS() {
  if (fpsList.length === 0) {
    fpsDisplayElement.textContent = "No FPS data available.";
    return;
  }

  const sum = fpsList.reduce((acc, fps) => acc + fps, 0);
  const averageFPS = sum / fpsList.length;
  fpsDisplayElement.textContent = `Average FPS: ${averageFPS.toFixed(1)}`;
}

const pose = new Pose({locateFile: (file) => {
  return `https://cdn.jsdelivr.net/npm/@mediapipe/pose@0.5.1675469404/${file}`;
}});
pose.setOptions({
  modelComplexity: 1,  // Complexity of the pose landmark model: 0, 1 or 2. Default: 1.
  static_image_mode: false, // The solution threats the input images as a video stream. Default: False.
  runningMode: "VIDEO",
  numPoses: 1,  // The maximum number of poses that can be detected by the Pose Landmarker.  
  smoothLandmarks: true,  // The solution filters pose landmarks across different input images to reduce jitter. Default: True.
  enableSegmentation: false,  // In addition to the pose landmarks the solution also generates the segmentation mask. Default: False.
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

// Iniciar el cálculo del promedio usando requestAnimationFrame
let animationId = null;
function startAnimation() {
  animationId = requestAnimationFrame(startAnimation);
  calculateAverageFPS();
}
startAnimation();

camera.start();