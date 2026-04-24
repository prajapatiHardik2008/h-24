const btn = document.querySelector('#make');
const input = document.querySelector('input');
const resultDiv = document.querySelector('.result');
const loader = document.querySelector('p');

btn.addEventListener('click', () => {
    // Tumne #prompt use kiya hai, ensure karo tumhare HTML input ki ID "prompt" ho.
    const promptValue = document.querySelector("#prompt").value.trim();
    
    if (promptValue) {
        // Loading text dikhao
        loader.style.display = 'block';
        loader.innerText = "Processing, please wait... (Flux model)";
        loader.style.color = "#8b949e";
        
        resultDiv.innerHTML = ''; // Purani image aur download button hatao

        // Naya image element create karo
        const img = document.createElement('img');
        
        // EncodeURIComponent zaroori hai
        const encodedPrompt = encodeURIComponent(promptValue);
        
        // Tumhara updated URL (Flux model ke saath)
        img.src = `https://gen.pollinations.ai/image/${encodedPrompt}?model=flux`;
        
        // Styling for the image to make sure it looks good in CSS
        img.style.maxWidth = "100%";
        img.style.height = "auto";
        img.style.borderRadius = "8px";

        // Jab image puri tarah load ho jaye
        img.onload = () => {
            loader.style.display = 'none';
            resultDiv.innerHTML = ''; // Clear loading text
            resultDiv.appendChild(img); // Image add karo
            
            // --- DOWNLOAD BUTTON LOGIC START ---
            
            // 1. Download Button create karo
            const downloadBtn = document.createElement('button');
            downloadBtn.innerText = "⬇️ Download Image";
            downloadBtn.id = "downloadBtn"; // Styling ke liye ID

            // 2. Button par click event lagao
            downloadBtn.addEventListener('click', () => {
                downloadImage(img.src, `H24_AI_${encodedPrompt.substring(0, 20)}.jpg`);
            });

            // 3. Button ko result div mein image ke neeche add karo
            resultDiv.appendChild(downloadBtn);
            
            // --- DOWNLOAD BUTTON LOGIC END ---
        };

        // Agar error aaye
        img.onerror = () => {
            loader.innerText = "Error: Server down.";
            loader.style.color = "red";
        };
    }
});

// Helper function to handle downloading across different browsers
function downloadImage(url, filename) {
    fetch(url)
        .then(response => response.blob())
        .then(blob => {
            const blobUrl = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = blobUrl;
            a.download = filename;
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            window.URL.revokeObjectURL(blobUrl);
        })
        .catch(err => {
            console.error('Download error:', err);
            alert("Download error");
        });
}