$(document).ready(function() {
    // Intercept the button click instead of form submission
    $('.post-comment-btn').click(function() {
        // Get the form data
        var formData = $(this).closest('form').serialize();
        var postId = $(this).data('post-id'); // Get post ID

        // Submit the form using AJAX
        $.ajax({
            type: 'POST',
            url: $(this).closest('form').attr('action'),
            data: formData,
            dataType: 'json',
            success: function(response) {
                // Handle the JSON response here (optional)
                console.log(response);

                // Update the likes count or perform any other actions
                $('#likes_count_' + response.post_id).text(response.likes_count);

                // Refresh the page after a short delay (e.g., 500 milliseconds)
                setTimeout(function() {
                    location.reload();
                }, 500);
            },
            error: function(error) {
                // Handle errors if needed
                console.error('Error:', error);
            }
        });
    });
});
