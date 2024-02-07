const videoElement = document.getElementsByClassName('input_video')[0];
const canvasElement = document.getElementsByClassName('output_canvas')[0];
const canvasCtx = canvasElement.getContext('2d');
const landmarkContainer = document.getElementsByClassName('landmark-grid-container')[0];
const grid = new LandmarkGrid(landmarkContainer);

let previousTimestamp = 0;

function onResults(results) {
  // Calcular FPS
  const timestamp = Date.now();
  const deltaTime = timestamp - previousTimestamp;
  const fps = 1000 / deltaTime;
  console.log(`FPS: ${fps.toFixed(1)}`);
  previousTimestamp = timestamp;

  if (!results.poseLandmarks) {
     grid.updateLandmarks([]);
    return;
  }

  // Aplicar espejo horizontal al videoElement
  videoElement.style.transform = 'scaleX(-1)';

  canvasCtx.save();
  canvasCtx.clearRect(0, 0, canvasElement.width, canvasElement.height);

  // Aplicar mirror (espejo) horizontal al canvasElement
  canvasCtx.scale(-1, 1);
  canvasCtx.translate(-canvasElement.width, 0);

  canvasCtx.drawImage(results.segmentationMask, 0, 0,
                      canvasElement.width, canvasElement.height);

  // Only overwrite existing pixels.
  canvasCtx.globalCompositeOperation = 'source-in';
  canvasCtx.fillStyle = '#00FF00';
  canvasCtx.fillRect(0, 0, canvasElement.width, canvasElement.height);

  // Only overwrite missing pixels.
  canvasCtx.globalCompositeOperation = 'destination-atop';
  canvasCtx.drawImage(
      results.image, 0, 0, canvasElement.width, canvasElement.height);

  //canvasCtx.scale(-1, 1); // Flip the image horizontally
  
  canvasCtx.globalCompositeOperation = 'source-over';
  drawConnectors(canvasCtx, results.poseLandmarks, POSE_CONNECTIONS,
                 {color: '#191970', lineWidth: 4});
  drawLandmarks(canvasCtx, results.poseLandmarks,
                {color: '#191970', lineWidth: 2});
  canvasCtx.restore();

  grid.updateLandmarks(results.poseWorldLandmarks);
}

const pose = new Pose({locateFile: (file) => {
  return `https://cdn.jsdelivr.net/npm/@mediapipe/pose/${file}`;
}});
pose.setOptions({
  modelComplexity: 0,
  runningMode: "VIDEO", 
  smoothLandmarks: true,
  enableSegmentation: true,
  smoothSegmentation: true,
  minDetectionConfidence: 0.5,
  minTrackingConfidence: 0.3
});
pose.onResults(onResults);

const camera = new Camera(videoElement, {
  onFrame: async () => {
    await pose.send({image: videoElement});
  },
  width: 480,
  height: 270,
  videoMirror: false
});
camera.start();