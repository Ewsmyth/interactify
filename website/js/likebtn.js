$(document).ready(function () {
  $('.like-btn').click(function () {
    var button = $(this);
    var post_id = button.data('post-id');
    var liked = button.data('liked');

    $.get('/like_post/' + post_id, function (data) {
      // Update button image source
      var likeIcon = button.find('.like-icon');
      liked = data.liked;
      likeIcon.attr('src', liked ? '/staticp/css/icons/unlike.png' : '/staticp/css/icons/like.png');

      // Update data-liked attribute
      button.data('liked', liked);

      // Update likes count
      var likes_count = $('#likes_count_' + post_id);
      likes_count.text(data.likes_count);
    });
  });
});
