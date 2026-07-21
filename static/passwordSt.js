const passwordInput = document.getElementById('password');
const toggleBtn = document.getElementById('toggle-btn');
const eyeIcon = document.getElementById('eye-icon');
const meterBar = document.getElementById('meter-bar');
const strengthText = document.getElementById('strength-text').querySelector('span');

// Requirement Elements
const reqLength = document.getElementById('length');
const reqUppercase = document.getElementById('uppercase');
const reqNumber = document.getElementById('number');
const reqSpecial = document.getElementById('special');

// Toggle Password Visibility
toggleBtn.addEventListener('click', () => {
    if (passwordInput.type === 'password') {
        passwordInput.type = 'text';
        eyeIcon.classList.remove('fa-eye');
        eyeIcon.classList.add('fa-eye-slash');
    } else {
        passwordInput.type = 'password';
        eyeIcon.classList.remove('fa-eye-slash');
        eyeIcon.classList.add('fa-eye');
    }
});

// Password Evaluation Logic
passwordInput.addEventListener('input', () => {
    const value = passwordInput.value;
    
    // Check individual criteria
    const hasLength = value.length >= 8;
    const hasUppercase = /[A-Z]/.test(value);
    const hasNumber = /[0-9]/.test(value);
    const hasSpecial = /[^A-Za-z0-9]/.test(value);

    updateRequirementUI(reqLength, hasLength);
    updateRequirementUI(reqUppercase, hasUppercase);
    updateRequirementUI(reqNumber, hasNumber);
    updateRequirementUI(reqSpecial, hasSpecial);

    // Calculate score (0 to 4)
    let score = 0;
    if (hasLength) score++;
    if (hasUppercase) score++;
    if (hasNumber) score++;
    if (hasSpecial) score++;

    updateMeter(score, value.length);
});

function updateRequirementUI(element, isValid) {
    const icon = element.querySelector('i');
    if (isValid) {
        element.classList.remove('invalid');
        element.classList.add('valid');
        icon.className = 'fa-solid fa-circle-check';
    } else {
        element.classList.remove('valid');
        element.classList.add('invalid');
        icon.className = 'fa-solid fa-circle-xmark';
    }
}

function updateMeter(score, length) {
    if (length === 0) {
        meterBar.style.width = '0%';
        strengthText.textContent = 'Too weak';
        strengthText.style.color = '#8b949e';
        return;
    }

    switch (score) {
        case 0:
        case 1:
            meterBar.style.width = '25%';
            meterBar.style.backgroundColor = '#f85149'; // Red
            strengthText.textContent = 'Weak';
            strengthText.style.color = '#f85149';
            break;
        case 2:
        case 3:
            meterBar.style.width = '65%';
            meterBar.style.backgroundColor = '#d29922'; // Orange/Yellow
            strengthText.textContent = 'Moderate';
            strengthText.style.color = '#d29922';
            break;
        case 4:
            meterBar.style.width = '100%';
            meterBar.style.backgroundColor = '#3fb950'; // Green
            strengthText.textContent = 'Strong';
            strengthText.style.color = '#3fb950';
            break;
    }
}