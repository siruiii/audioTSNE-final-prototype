let currentlyPlayingSound = null; // Make sure this is defined globally
let startTime = null; // Define this globally as well
let clickedPoints = new Set(); // Define this globally
let totalPoint = 0;
let previousSphere = null; // Track the previous sphere

function loadAndCreateSpheres(url) {
  fetch(url)
    .then((response) => response.json())
    .then((data) => {
      totalPoint = data.length;
      const container = document.getElementById("sphere-container");
      const maxX = Math.max(...data.map(item => item.point[1]));
      const minX = Math.min(...data.map(item => item.point[1]));
      const rangeX = maxX - minX;
      const radius = 150;

      console.log(totalPoint);

      data.forEach((item) => {
        const point = item.point;
        const soundPath = item.path;
        const id = parseInt(soundPath.split('/').pop().split('_')[0], 10);
        const x2d = point[1];
        const y2d = point[0];
        const z2d = 200;
        const theta = ((x2d - minX) / rangeX) * 2 * Math.PI;
        const x3d = radius * Math.cos(theta);
        const z3d = radius * Math.sin(theta);
        const y3d = y2d;

        // Create the sphere
        const sphere = document.createElement("a-sphere");
        sphere.setAttribute("id", id);
        sphere.setAttribute("position", `${x3d} ${y3d} ${z3d}`);
        sphere.setAttribute("radius", "2"); // Default radius
        sphere.setAttribute("color", "white"); // Default color
        sphere.classList.add('raycastable');

        // Create the sound
        const sound = document.createElement("a-sound");
        sound.setAttribute("src", soundPath);
        sound.setAttribute("autoplay", "false");
        sound.setAttribute("volume", "50");
        sphere.appendChild(sound);

        container.appendChild(sphere);

        sphere.addEventListener("raycaster-intersected", () => {
          // Check if there was a previous sphere
          if (previousSphere && previousSphere !== sphere) {
            // Revert the previous sphere
            previousSphere.setAttribute("radius", "2"); // Reset radius
            previousSphere.setAttribute("color", "green"); // Change color to green if it was clicked
            if (currentlyPlayingSound) {
              currentlyPlayingSound.components.sound.stopSound();
              logDurationAndStopSound(); // Stop and log duration of the previous sound
            }
          }

          // Check if the sound is currently playing
          if (currentlyPlayingSound === sound) {
            // Revert the currently playing sphere
            sphere.setAttribute("radius", "2"); // Reset radius
            sphere.setAttribute("color", "white"); // Reset color to white
            sound.components.sound.stopSound();
            startTime = null;
            currentlyPlayingSound = null;
          } else {
            // Set up the new currently playing sphere
            sphere.setAttribute("radius", "5");
            sphere.setAttribute("color", "red"); // Set color to red when radius is 5
            sound.components.sound.playSound();
            currentlyPlayingSound = sound;
            startTime = new Date();
          }

          // Update previous sphere
          previousSphere = sphere;

          // Update clickedPoints and progress bar
          clickedPoints.add(id);
          updateProgressBar();
        });

        sound.addEventListener('sound-ended', () => {
          // Revert the sphere when the sound ends
          if (sphere === previousSphere) {
            sphere.setAttribute("radius", "2"); // Reset radius
            sphere.setAttribute("color", "green"); // Reset color to white
          }
          logDurationAndStopSound();
        });
      });
    })
    .catch((error) => console.error("Error loading JSON:", error));
}

function logDurationAndStopSound() {
  if (currentlyPlayingSound) {
    currentlyPlayingSound.components.sound.stopSound();
    const endTime = new Date();
    const duration = (endTime - startTime) / 1000; // Duration in seconds
    const soundPath = currentlyPlayingSound.getAttribute('src');
    console.log(`Duration: ${duration}, Path: ${soundPath}`);
    startTime = null;
    currentlyPlayingSound = null;
  }
}

function updateProgressBar() {
  const progressBar = document.getElementById("progress-bar");
  const percentage = (clickedPoints.size / totalPoint) * 100;
  progressBar.style.width = `${percentage}%`;
  var progressPanel = document.querySelector('#progress-panel');
  var progressFill = document.querySelector('#progress-fill');
  progressFill.setAttribute('width', percentage / 100 * (progressPanel.getAttribute('width')));
  updateProgressFillPosition();
}

function updateProgressFillPosition() {
  var progressPanel = document.querySelector('#progress-panel');
  var progressFill = document.querySelector('#progress-fill');
  
  // Get the width of the progress panel
  var panelWidth = progressPanel.getAttribute('width');
  
  // Update the position of the progress fill
  var fillWidth = progressFill.getAttribute('width');
  var newPositionX = - (panelWidth / 2) + (fillWidth / 2);
  
  progressFill.setAttribute('position', `${newPositionX} 0.08 0.005`);
}
