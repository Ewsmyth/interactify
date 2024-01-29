$(document).ready(function () {
    // Listen for changes in the file input
    $('#media_files').on('change', function () {
      // Get the selected files
      var files = $(this)[0].files;

      // Display selected files in the .display-select div
      var displaySelect = $('.display-select');
      displaySelect.empty(); // Clear previous content

      for (var i = 0; i < files.length; i++) {
        var fileType = files[i].type.split('/')[0]; // Get the file type (image or video)

        // Create a preview element for each file
        var previewElement = $('<div class="file-preview"></div>');

        if (fileType === 'image') {
          var img = $('<img src="" alt="Image Preview">');
          img.attr('src', URL.createObjectURL(files[i]));
          previewElement.append(img);
        } else if (fileType === 'video') {
          var video = $('<video width="100%" height="100%" controls></video>');
          video.attr('src', URL.createObjectURL(files[i]));
          previewElement.append(video);
        }

        displaySelect.append(previewElement);
      }
    });
});