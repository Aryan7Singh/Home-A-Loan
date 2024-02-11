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

    sliders.forEach(function(slider,index) {
        sliderValues[slider.getAttribute('name')] = slider.value;
        sliderValueSpans[index].innerHTML = slider.value;
    });

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
    xhr.send(JSON.stringify(sliderValues));
}
$(document).ready(function() {
    $('#viewInsightsButton').on('click', function(event) {
        event.preventDefault(); 
        
        var xhr = new XMLHttpRequest();
        xhr.open("POST", "/insights", true);
        xhr.setRequestHeader("Content-Type", "application/json");
        xhr.onreadystatechange = function() {
            if (xhr.readyState === XMLHttpRequest.DONE) {
                if (xhr.status === 200) {
                    var response = JSON.parse(xhr.responseText);
                    if (response && response.redirect) {
                        console.log("Redirecting...");
                        window.location.href = response.redirect;
                    } else {
                        console.error('Error: No redirect URL provided in response');
                    }
                } else {
                    console.error('Error occurred while making AJAX request:', xhr.status);
                }
            }
        };
        xhr.send();
    });
});


