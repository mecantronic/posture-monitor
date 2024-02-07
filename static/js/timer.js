// Temporizador para codo
let elbowhr = elbowmin = elbowsec = "00"
let elbowstartTimer;
let shoulderhr = shouldermin = shouldersec = "00"
let shoulderstartTimer;

const elbowStartBtn = document.querySelector(".elbowstart"),
elbowStopBtn = document.querySelector(".elbowstop"),
elbowResetBtn = document.querySelector(".elbowreset");

elbowStartBtn.addEventListener("click", elbowStart);
elbowStopBtn.addEventListener("click", elbowstop);
elbowResetBtn.addEventListener("click", elbowreset);

function elbowStart() {
elbowStartBtn.classList.add("active");
elbowStopBtn.classList.remove("stopActive");

elbowstartTimer = setInterval(() => {
  elbowsec++;
  elbowsec = elbowsec < 10 ? "0" + elbowsec : elbowsec;

  if (elbowsec == 60) {
    elbowmin++;
    elbowmin = elbowmin < 10 ? "0" + elbowmin : elbowmin;
    elbowsec = "00";
  }

  if (elbowmin == 60) {
    elbowhr++;
    elbowhr = elbowhr < 10 ? "0" + elbowhr : elbowhr;
    elbowmin = "00";
  }

  if (elbowhr == 24) {
    elbowhr = "00";
  }

  putValue(elbowsec, elbowmin, elbowhr);
}, 1000);
}

function elbowstop() {
elbowStartBtn.classList.remove("active");
elbowStopBtn.classList.add("stopActive");
clearInterval(elbowstartTimer);
}

function elbowreset() {
elbowStartBtn.classList.remove("active");
elbowStopBtn.classList.remove("stopActive");
clearInterval(elbowstartTimer);
elbowhr = elbowmin = elbowsec = "00";
putValue();
}

// Temporizador para hombro

const shoulderStartBtn = document.querySelector(".shoulderstart"),
shoulderStopBtn = document.querySelector(".shoulderstop"),
shoulderResetBtn = document.querySelector(".shoulderreset");

shoulderStartBtn.addEventListener("click", shoulderStart);
shoulderStopBtn.addEventListener("click", shoulderstop);
shoulderResetBtn.addEventListener("click", shoulderreset);

function shoulderStart() {
shoulderStartBtn.classList.add("active");
shoulderStopBtn.classList.remove("stopActive");

shoulderstartTimer = setInterval(() => {
  shouldersec++;
  shouldersec = shouldersec < 10 ? "0" + shouldersec : shouldersec;

  if (shouldersec == 60) {
    shouldermin++;
    shouldermin = shouldermin < 10 ? "0" + shouldermin : shouldermin;
    shouldersec = "00";
  }

  if (shouldermin == 60) {
    shoulderhr++;
    shoulderhr = shoulderhr < 10 ? "0" + shoulderhr : shoulderhr;
    shouldermin = "00";
  }

  if (shoulderhr == 24) {
    shoulderhr = "00";
  }

  putValue();
}, 1000);
}

function shoulderstop() {
shoulderStartBtn.classList.remove("active");
shoulderStopBtn.classList.add("stopActive");
clearInterval(shoulderstartTimer);
}

function shoulderreset() {
shoulderStartBtn.classList.remove("active");
shoulderStopBtn.classList.remove("stopActive");
clearInterval(shoulderstartTimer);
shoulderhr = shouldermin = shouldersec = "00";
putValue(elbowsec, elbowmin, elbowhr, shouldersec, shouldermin, shoulderhr);
}

function putValue() {
  // Actualiza los valores del hombro
  document.querySelector('.shouldersecond').innerHTML = shouldersec;
  document.querySelector('.shoulderminute').innerHTML = shouldermin;
  document.querySelector('.shoulderhour').innerHTML = shoulderhr;

  // Actualiza los valores del codo
  document.querySelector('.elbowsecond').innerHTML = elbowsec;
  document.querySelector('.elbowminute').innerHTML = elbowmin;
  document.querySelector('.elbowhour').innerHTML = elbowhr;
}