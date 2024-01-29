function displaySelectedImage() {
    var input = document.getElementById('a2');
    var img = document.getElementById('profile-img');
    var submitBtn = document.getElementById('submit-btn');
    var file = input.files[0];

    if (file) {
      var reader = new FileReader();
      reader.onload = function(e) {
        img.src = e.target.result;
        submitBtn.style.display = 'block'; // Show the submit button
      };
      reader.readAsDataURL(file);
    } else {
      submitBtn.style.display = 'none'; // Hide the submit button if no file is selected
    }
}