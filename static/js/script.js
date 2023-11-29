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