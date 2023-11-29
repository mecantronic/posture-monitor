document.addEventListener('DOMContentLoaded', function () {
    console.log('La página index.html se ha cargado completamente.');

    var usernameInput = document.getElementById("username");

    if (usernameInput) {
        var username = usernameInput.value;
        console.log(username);
    } else {
        console.error("Elemento con id 'username' no encontrado.");
    }

    const imgActivities = document.querySelectorAll(".bg-activity-image");

    imgActivities.forEach(img => {
        img.addEventListener('click', function() {
            imgActivities.forEach(originalImg => {
                originalImg.style.width = '250px';
                originalImg.style.height = '200px';
            });

            img.style.width = '230px';
            img.style.height = '180px';
        });
    });

});


function openFileDialog() {
    // Trigger the file input dialog
    document.getElementById('videoInput').click();
}

// Handle file selection
document.getElementById('videoInput').addEventListener('change', function (event) {
    // Get the selected file
    const selectedFile = event.target.files[0];

    // Check if a file was selected
    if (selectedFile) {
        // Assign a fixed name to the file
        const fixedFileName = 'video.mp4';

        // Perform any additional actions if needed

        // Redirect to the upload route with the fixed filename
        window.location.href = '/upload?filename=' + encodeURIComponent(fixedFileName);
        console.log('/upload?filename=' + encodeURIComponent(fixedFileName));
    }
});

function toggleFileInput() {
    var fileInput = document.getElementById('file');
    var videoLabel = document.getElementById('videoLabel');
    var webcamCheckbox = document.getElementById('use_webcam');
    var videoOptions = document.getElementById('videoOptions');
    var videoOptionsLabel = document.getElementById('videoOptionsLabel');

    if (webcamCheckbox.checked) {
        fileInput.style.display = 'none';
        videoLabel.style.display = 'none';
        videoOptions.style.display = 'none';
        videoOptionsLabel.style.display = 'none';
    } else {
        fileInput.style.display = 'block';
        videoLabel.style.display = 'block';
        videoOptions.style.display = 'block';
        videoOptionsLabel.style.display = 'none';
    }
}
