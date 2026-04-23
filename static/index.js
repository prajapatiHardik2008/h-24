
const tools = document.querySelectorAll('.card');

let timer;
document.querySelector("#search").addEventListener('keyup',(event)=>{
    clearTimeout(timer);
    timer = setTimeout(()=> {
        let qur = event.target.value.toLowerCase();
        tools.forEach(tool=>{
            const toolName = tool.querySelector('h3').innerText.toLowerCase();
            if (toolName.includes(qur))
            {
                tool.style.display = "block";
            }
            else
            {
                tool.style.display = "none";
            }
        });
    },300);
});
document.querySelectorAll('.star-rating input').forEach(star => {
    star.addEventListener('change', (e) => {
        // Hidden input ki value update karo
        document.querySelector("#selected-rating").value = e.target.value;
        console.log("Current Rating Set to:", e.target.value);
    });
});

let feedbackForm = document.querySelector("#feedbackForm");

if(feedbackForm) {
    // Yahan 'async' likhna compulsory hai
    feedbackForm.addEventListener('submit', async (event) => {
        event.preventDefault();

        // Data collection
        const dataToSend = {
            username: document.querySelector('#username').value,
            userphone: document.querySelector('#phonenumber').value,
            star: document.querySelector("#selected-rating").value,
            userquery: document.querySelector("#discry").value
        };

        try {
            const response = await fetch('/feedBack', {
                method: "POST",
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(dataToSend) // Sahi variable use kiya
            });

            if(response.ok) {
                const result = await response.json();
                // Check karne ke liye '==' use karo, '=' nahi
                if (result.Ans === "Success") {
                    alert("Feedback Submitted Successfully! ✅");
                    feedbackForm.reset();
                } else {
                    alert("Form not Submit. Try again! ❌");
                }
            }
        } catch(error) {
            console.log("Error logic:", error);
            alert("Network error! Check your connection.");
        }
    });
}