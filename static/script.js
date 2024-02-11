function scrollToMain() {
    const mainElement = document.getElementById('mainContent');

    if (mainElement) {
        mainElement.scrollIntoView({
            behavior: 'smooth'
        });
    }
}
