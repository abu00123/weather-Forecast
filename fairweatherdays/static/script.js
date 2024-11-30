// Get the form and loading elements
const form = document.getElementById('weatherForm');
const loading = document.getElementById('loading');
const spinner = document.getElementById('spinner');

// Event listener for the form submission
form.addEventListener('submit', function(e) {
    // Show the loading message when form is submitted
    loading.style.display = 'block';
    spinner.style.display = 'block'; // Show the spinner

    // Optional: Prevent default form submission to keep loading visible
    e.preventDefault();

    // Submit the form after a delay to keep loading visible
    setTimeout(function() {
        form.submit();
    }, 500);  // You can adjust this timeout if needed
});
