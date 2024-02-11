function scrollToMain() {
    const mainElement = document.getElementById('mainContent');

    if (mainElement) {
        mainElement.scrollIntoView({
            behavior: 'smooth'
        });
    }
}

function rangeSlide(selectedModels) {
    return function(value) {
        var sliderValues = {};
        var sliders = document.querySelectorAll('.range');
        var sliderValueSpans = document.querySelectorAll('.slider-value');

        sliders.forEach(function(slider, index) {
            sliderValues[slider.getAttribute('name')] = slider.value;
            sliderValueSpans[index].innerHTML = slider.value;
        });

        var requestData = {sliderValues: sliderValues, selectedModels: selectedModels};
        var xhr = new XMLHttpRequest();
        xhr.open("POST", "/prediction", true);
        xhr.setRequestHeader("Content-Type", "application/json");
        xhr.onreadystatechange = function() {
            if (xhr.readyState === XMLHttpRequest.DONE) {
                if (xhr.status === 200) {
                    var response = JSON.parse(xhr.responseText);
                    document.querySelector('.blob-text').textContent = response.message;
                } else {
                    console.error('Error occurred while making AJAX request:', xhr.status);
                }
            }
        };
        xhr.send(JSON.stringify(requestData));
    }
}

$(document).ready(function() {
    var selectedModels = []; 
    $('#model-options2').addClass('clicked');
    $('.model-options').on('click', function() {
        var anyClicked = $('.model-options.clicked').length > 1 || !$(this).hasClass('clicked');
        if (!anyClicked) {
            return;
        }
        $(this).toggleClass('clicked');
        
        selectedModels = [];
        $('.model-options.clicked').each(function() {
            var modelName = $(this).text();
            if (modelName === "Logistic") {
                selectedModels.push("log");
            } else if (modelName === "LightGBM") {
                selectedModels.push("lgb");
            } else if (modelName === "xgbBooster") {
                selectedModels.push("xgb");
            } else {
                selectedModels.push(modelName);
            }
        });

        rangeSlide(selectedModels)();
    });

    $('.range').on('change', function() {
        rangeSlide(selectedModels)();
    });
});
