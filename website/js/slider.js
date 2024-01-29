document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll(".post-media").forEach(function (mediaContainer) {
        var mediaList = mediaContainer.querySelector("ul");
        var mediaItems = mediaList.querySelectorAll("li");
        var currentIndex = 0;
        var startX, startY, distX, distY;
        var threshold = 50; // Minimum distance required to trigger a swipe

        function showMedia(index) {
            if (index < 0) {
                index = mediaItems.length - 1;
            } else if (index >= mediaItems.length) {
                index = 0;
            }

            currentIndex = index;

            mediaItems.forEach(function (item, i) {
                if (i === currentIndex) {
                    item.style.display = "block";
                    item.style.transition = "transform 0.3s ease"; // Add transition effect
                    item.style.transform = "translateX(0)";
                } else {
                    item.style.display = "none";
                }
            });
        }

        mediaContainer.addEventListener("touchstart", function (e) {
            startX = e.changedTouches[0].pageX;
            startY = e.changedTouches[0].pageY;
        });

        mediaContainer.addEventListener("touchmove", function (e) {
            distX = e.changedTouches[0].pageX - startX;
            distY = e.changedTouches[0].pageY - startY;

            // Check if the swipe is horizontal
            if (Math.abs(distX) > Math.abs(distY)) {
                e.preventDefault(); // Prevent vertical scrolling

                // Move the media container with the swipe
                mediaItems.forEach(function (item, i) {
                    if (i === currentIndex) {
                        item.style.transform = "translateX(" + distX + "px)";
                    }
                });
            }
        });

        mediaContainer.addEventListener("touchend", function (e) {
            if (Math.abs(distX) > threshold) {
                // Swipe distance is greater than the threshold, trigger next or previous accordingly
                if (distX > 0) {
                    showMedia(currentIndex - 1);
                } else {
                    showMedia(currentIndex + 1);
                }
            } else {
                // Reset the position if the swipe distance is below the threshold
                showMedia(currentIndex);
            }

            // Clear the transition property after the animation completes
            setTimeout(function () {
                mediaItems.forEach(function (item) {
                    item.style.transition = "";
                });
            }, 300); // Adjust this timeout to match the transition duration
        });

        showMedia(currentIndex);
    });
});
