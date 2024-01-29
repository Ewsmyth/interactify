function displayImage() {
  const fileInput = document.getElementById('file-input');
  const imageContainer = document.getElementById('image-container');
  const selectedImage = document.getElementById('selected-image');

  const file = fileInput.files[0];

  if (file) {
    const reader = new FileReader();

    reader.onload = function (e) {
      selectedImage.src = e.target.result;
      selectedImage.style.display = 'block'; // Show the image
    };

    reader.readAsDataURL(file);
  } else {
    selectedImage.style.display = 'none'; // Hide the image if no file is selected
  }
}
