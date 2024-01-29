$(document).ready(function () {
    $('.delete-post-btn').click(function () {
        var post_id = $(this).data('post-id');

        // Use jQuery to send a POST request to the delete_post route
        $.post('/delete_post/' + post_id, function (data) {
            if (data.status === 'success') {
                alert(data.message);
                // Reload the page after a short delay (e.g., 500 milliseconds)
                setTimeout(function () {
                    location.reload();
                }, 500);
            } else {
                alert(data.message);
            }
        });
    });
});
