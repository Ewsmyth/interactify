function toggleShareButton(postId) {
    var commentInput = $('#comment_content_' + postId);
    var shareButton = $('#post_comment_btn_' + postId);

    if (commentInput.val().trim() !== '') {
      shareButton.show();
    } else {
      shareButton.hide();
    }
}