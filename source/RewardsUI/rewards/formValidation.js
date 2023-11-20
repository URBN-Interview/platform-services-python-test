/******************     NOT IN USE! MIGHT INCLUDE/DEVELOP LATER      ***************** */

document.addEventListener('DOMContentLoaded', function() {
    const emailInput = document.getElementById('emailInput');
    const emailError = document.getElementById('email-error');

    emailInput.addEventListener('input', function(event) {
        const email = event.target.value.trim();
        if (!email) {
            emailError.textContent = 'Please enter a valid email address';
        } else {
            emailError.textContent = '';
        }
    });
});
