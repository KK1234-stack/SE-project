// JavaScript to handle scroll-triggered animations
window.addEventListener('scroll', function() {
    const elements = document.querySelectorAll('.fade-in');
    elements.forEach(element => {
        if (element.getBoundingClientRect().top < window.innerHeight) {
            element.classList.add('visible');
        }
    });

    const slideLeftElements = document.querySelectorAll('.slide-in-left');
    slideLeftElements.forEach(element => {
        if (element.getBoundingClientRect().top < window.innerHeight) {
            element.classList.add('visible');
        }
    });

    const slideRightElements = document.querySelectorAll('.slide-in-right');
    slideRightElements.forEach(element => {
        if (element.getBoundingClientRect().top < window.innerHeight) {
            element.classList.add('visible');
        }
    });
});


