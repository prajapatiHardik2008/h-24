document.getElementById('loginForm').addEventListener('submit', function(e) {
    const btn = document.getElementById('loginBtn');
    
    btn.innerText = "Authenticating...";
    btn.style.opacity = "0.7";
    btn.disabled = true;

});