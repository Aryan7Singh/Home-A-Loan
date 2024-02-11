function scrollToMain() {
    const mainElement = document.getElementById('mainContent');

    if (mainElement) {
        mainElement.scrollIntoView({
            behavior: 'smooth'
        });
    }
}

function rangeSlide(value) {
    var sliderValues = {};
    var sliders = document.querySelectorAll('.range');
    var sliderValueSpans = document.querySelectorAll('.slider-value');
    sliders.forEach(function(slider, index) {
        sliderValues[slider.getAttribute('name')] = slider.value;
        sliderValueSpans[index].innerHTML = slider.value;
    });

    var xhr = new XMLHttpRequest();
    xhr.open("POST", "/prediction", true);
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.send(JSON.stringify(sliderValues));
    
}