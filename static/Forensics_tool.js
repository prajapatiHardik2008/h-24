// --- 1. STRING EXTRACTION LOGIC ---
function extractStrings(file) {
    if (!file) {
        alert("Bhai, pehle file toh select karo!");
        return;
    }

    const reader = new FileReader();
    reader.onload = function(e) {
        let buffer = e.target.result;
        let view = new Uint8Array(buffer); // 'new' keyword zaruri hai
        let currentstring = ""; 
        let allStrings = [];

        for(let i = 0; i < view.length; i++) {
            let byte = view[i];
            if(byte >= 32 && byte <= 126) {
                currentstring += String.fromCharCode(byte);
            } else {
                if(currentstring.length > 4) {
                    allStrings.push(currentstring);
                }
                currentstring = "";
            }
        }
    
        // Nayi ID ko target kar rahe hain
        let resultBox = document.querySelector("#result");
        if (allStrings.length > 0) {
            resultBox.innerText = allStrings.join("\n");
        } else {
            resultBox.innerText = "No readable strings found!";
        }
    };
    reader.readAsArrayBuffer(file);
}

// --- 2. METADATA LOGIC ---
function getmetadate() {
    let fileElement = document.querySelector("#filein");
    let file = fileElement.files[0];

    if (!file) {
        alert("Bhai, pehle file toh select karo!");
        return;
    }

    // EXIF.getData (D capital)
    EXIF.getData(file, function() {
        let allmetaData = EXIF.getAllTags(this);
        let resultBox = document.querySelector('#Exif-result');

        if (allmetaData && Object.keys(allmetaData).length > 0) {
            let make = EXIF.getTag(this, "Make") || "Unknown";
            let model = EXIF.getTag(this, "Model") || "Unknown";
            
            // JSON format mein sundar dikhane ke liye
            let formattedData = JSON.stringify(allmetaData, null, 2);
            
            resultBox.innerText = `Make: ${make} \nModel: ${model} \n\n--- Full Metadata ---\n${formattedData}`;
        } else {
            resultBox.innerText = "No EXIF data found!";
        }
    });
}