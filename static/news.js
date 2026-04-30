let currentNewsIndex = 0;
// Kyunki tera backend abhi ek baar mein 1 hi news summarize kar raha hai (pageSize=1)
// Isliye hum seedha news display karenge.

async function Getnews() {
    const newsContainer = document.querySelector("#news-content");
    newsContainer.innerHTML = "Initializing AI Analysis..."; // Loader vibe

    try {
        // Ab hum tere Flask backend se data le rahe hain
        const response = await fetch('/get-news-data');
        const data = await response.json();

        if (data.news) {
            // Backend se jo "news" key aa rahi hai, wo AI ka summarized content hai
            displayNews(data.news);
        } else {
            newsContainer.innerText = "Error: AI could not process news.";
        }
    } catch (error) {
        console.error("Fetch Error:", error);
        newsContainer.innerText = "Connection to H-24 Terminal Failed.";
    }
}

function displayNews(summarizedContent) {
    const result = document.querySelector("#news-content");
    
    // UI ko clean rakho
    result.innerHTML = `
        <div style="margin-bottom: 10px; font-weight: bold;">>> H-24 INTEL_FEED</div>
        <pre>${summarizedContent}</pre>
    `;
}
// Next button par wapas API call hogi naye data ke liye
document.querySelector("#next-btn").addEventListener("click", () => {
    Getnews();
});

// Initial Load
Getnews();