// Get the search term input and search button elements
const searchInput = document.getElementById('search_term');
const searchButton = document.getElementById('search_button');

// Add an event listener to the input to toggle the search button visibility
searchInput.addEventListener('input', function () {
// Show the search button if the input has a value, hide it otherwise
if (searchInput.value.trim() !== '') {
    searchButton.style.display = 'block';
} else {
    searchButton.style.display = 'none';
}
});