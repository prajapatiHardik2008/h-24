// Global variable taaki hum track rakh sakein konsi news dikhani hai
let currentNewsIndex = 0;
let allArticles = [];

async function Getnews() {
    const keyResponse = await fetch('/get-news-data');
    const keyData = await keyResponse.json();
    const apiKey = keyData.apiKey;
    const url = `https://newsapi.org/v2/everything?q=cybersecurity&pageSize=20&apiKey=${apiKey}`;

    try {
        const response = await fetch(url);
        const data = await response.json();
        
        if (data.articles && data.articles.length > 0) {
            allArticles = data.articles; // Saari 20 news save kar li
            displaySingleNews(currentNewsIndex);
        } else {
            document.querySelector("#news-content").innerText = "No News Found.";
        }
    } catch (error) {
        console.error("Fetch Error:", error);
        document.querySelector("#news-content").innerText = "Connection Failed.";
    }
}

// Ye function srif ek news ko filter karke dikhayega
function displaySingleNews(index) {
    const result = document.querySelector("#news-content");
    const article = allArticles[index];

    if (!article) {
        result.innerText = "No more news available.";
        return;
    }

    // Filtered Data: Sirf kaam ki cheezein
    const title = article.title || "No Title";
    const source = article.source.name || "Unknown Source";
    const description = article.description || "No Description available.";
    const time = new Date(article.publishedAt).toLocaleDateString();

    // UI par display karna
    result.innerHTML = `
        <div style="border-bottom: 1px solid #1a1a1a; padding-bottom: 10px; margin-bottom: 10px;">
            <span style="color: #00ff41; font-size: 12px;">[ SOURCE: ${source.toUpperCase()} ]</span>
            <span style="color: #888; font-size: 12px; float: right;">${time}</span>
        </div>
        <h3 style="color: #fff; margin: 10px 0;">${title}</h3>
        <p style="color: #ccc; font-size: 16px;">${description}</p>
        <div style="margin-top: 15px; font-size: 12px; color: #444;">
            STATUS: DECRYPTED_SUCCESSFULLY
        </div>
    `;
}

// Event Handler for Next Button
document.querySelector("#next-btn").addEventListener("click", () => {
    currentNewsIndex++;
    if (currentNewsIndex < allArticles.length) {
        displaySingleNews(currentNewsIndex);
    } else {
        // Agar 20 news khatam ho jayein toh wapas pehli par ya naya fetch
        currentNewsIndex = 0;
        Getnews();
    }
});

// Pehli baar news load karne ke liye
Getnews();