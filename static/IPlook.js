let btn = document.querySelector("#Getdata");
let result = document.querySelector(".result");

btn.addEventListener("click", async () => {
    let ip = document.querySelector("#IP").value;
    
    if (!ip) {
        result.innerText = "Please enter an IP address";
        return;
    }

    result.innerText = `Wait a min, fetching data for: ${ip}...`;

    try {
        // ip-api.com ki jagah ipapi.co use kar rahe hain
        let url = `https://ipapi.co/${ip}/json/`;
        let response = await fetch(url);
        
        if (!response.ok) {
            throw new Error("Network response was not ok");
        }

        let data = await response.json();
        result.innerText = JSON.stringify(data, null, 2);
    } catch (error) {
        result.innerText = "Error: " + error.message + ". Try a different IP or check connection.";
        console.error("Fetch error:", error);
    }
});