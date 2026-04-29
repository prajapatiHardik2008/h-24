let repoChart = null; // Chart instance track karne ke liye
let search_btn = document.querySelector("#config");
search_btn.addEventListener("click", async () => {
    const username = document.querySelector("#gitname").value;
    const result = document.querySelector("#result");

    const response = await fetch('/Git_Hub', {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ "Username": username })
    });

    const data = await response.json();

    if (data.status === "error") {
        result.innerText = data.message;
    } else {
        const info = data.User_information;
        
        // 1. Text Data Display
        result.innerHTML = `
            <h2 style="color:var(--neon)">${info.Name || username}</h2>
            <p>Followers: ${info.Followers}</p>
            <p>Public Repos: ${info.PublicRepos}</p>
            <hr border="1px solid #222">
            <h4>Latest Repos:</h4>
            <ul>${info.Repos.slice(0, 5).map(r => `<li>${r.Name} (⭐${r.Stars})</li>`).join('')}</ul>
        `;

        // 2. Prepare Data for Chart (Top 5 repos by Stars)
        const labels = info.Repos.slice(0, 5).map(r => r.Name);
        const stars = info.Repos.slice(0, 5).map(r => r.Stars);

        // 3. Render Chart
        updateChart(labels, stars);
    }
});

function updateChart(labels, stars) {
    const ctx = document.getElementById('repoChart').getContext('2d');
    
    // Purana chart delete karo agar naya search kiya hai
    if (repoChart) { repoChart.destroy(); }

    repoChart = new Chart(ctx, {
        type: 'bar', // Tum ise 'pie' ya 'doughnut' bhi kar sakte ho
        data: {
            labels: labels,
            datasets: [{
                label: 'Stars per Repo',
                data: stars,
                backgroundColor: 'rgba(0, 255, 65, 0.5)',
                borderColor: '#00ff41',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: { beginAtZero: true, grid: { color: '#222' } }
            }
        }
    });
}