function toggleShareButton(postId) {
    var commentInput = $('#comment_content_' + postId);
    var shareButton = $('#post_comment_btn_' + postId);

    if (commentInput.val().trim() !== '') {
      shareButton.show();
    } else {
      shareButton.hide();
    }
  }

  function toggleCommentsHeight(postId) {
    var commentsList = $('#comments-list-' + postId);

    if (commentsList.css('max-height') === '50px') {
      commentsList.css({
        'max-height': '600px',
        'overflow': 'scroll'
      });
    } else {
      commentsList.css({
        'max-height': '50px',
        'overflow': 'hidden'
      });
    }
}