function scrollToMain() {
    const mainElement = document.getElementById('mainContent');

    if (mainElement) {
        mainElement.scrollIntoView({
            behavior: 'smooth'
        });
    }
}

function rangeSlide(featureName, value) {
    var sliderValues = {};
    var sliders = document.querySelectorAll('.range');
    document.getElementById(featureName + 'Display').innerHTML = value;
    sliders.forEach(function(slider) {
        sliderValues[slider.getAttribute('name')] = slider.value;
    });

    var xhr = new XMLHttpRequest();
    xhr.open("POST", "/predict", true);
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.send(JSON.stringify(sliderValues));
}

document.getElementById('submit-button').addEventListener('click', function() {
    var sliderValues = {};
    var sliders = document.querySelectorAll('.range');
    sliders.forEach(function(slider) {
        sliderValues[slider.getAttribute('name')] = slider.value;
    });

    var xhr = new XMLHttpRequest();
    xhr.open("POST", "/prediction", true);
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.send(JSON.stringify(sliderValues));
});
