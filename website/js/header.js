document.addEventListener("DOMContentLoaded", function () {
    var lastScrollTop = 0;
    var header = document.querySelector('.header');

    window.addEventListener("scroll", function () {
        var scrollTop = window.pageYOffset || document.documentElement.scrollTop;

        if (scrollTop > lastScrollTop) {
            // Scroll down
            header.classList.add('show');
        } else {
            // Scroll up
            header.classList.remove('show');
        }

        lastScrollTop = scrollTop <= 0 ? 0 : scrollTop; // For mobile or negative scrolling
    });
});
