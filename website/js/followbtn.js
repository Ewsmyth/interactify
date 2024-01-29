$(document).ready(function () {
    $('.follow-btn').click(function (event) {
        event.preventDefault();  // Prevent the default form submission

        var button = $(this);
        var followed = button.data('followed');
        var form = button.closest('form');

        $.ajax({
            type: form.attr('method'),
            url: form.attr('action'),
            data: form.serialize(),  // Include form data
            success: function (data) {
                // Update button text and data attribute
                followed = !followed; // Reverse the state
                button.data('followed', followed);
                button.text(followed ? 'Unfollow' : 'Follow');

                // Update button class based on the state
                if (followed) {
                    button.removeClass('follow').addClass('unfollow');
                } else {
                    button.removeClass('unfollow').addClass('follow');
                }

                // You can add a flash message logic here based on the server response
                if (followed) {
                    // Display a success message for following
                    console.log('Successfully followed user');
                } else {
                    // Display a success message for unfollowing
                    console.log('Successfully unfollowed user');
                }
            },
            error: function (error) {
                console.error('Error:', error);
            }
        });
    });
});
