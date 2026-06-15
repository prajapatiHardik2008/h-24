// --- 1. STRING EXTRACTION LOGIC ---
function extractStrings(file) {
    if (!file) {
        alert("Select a file first, bro!");
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

        let resultBox = document.querySelector("#result");
        if (allStrings.length > 0) {
            resultBox.innerText = allStrings.join("\n");
        } else {
            resultBox.innerText = "No readable strings found!";
        }
    };
    reader.readAsArrayBuffer(file);
}
function getmetadata() {
    let fileElement = document.querySelector("#filein");
    let file = fileElement.files[0];

    if (!file) {
        alert("Select a file first, bro!");
        return;
    }

    // Zaruri: Check karein kya library load hui hai
    if (typeof EXIF === 'undefined') {
        alert("EXIF library load nahi hui hai! Script tag check karein.");
        return;
    }

    EXIF.getData(file, function() {
        // Yahan 'this' file ko refer karega
        let allmetaData = EXIF.getAllTags(this);
        let resultBox = document.querySelector('#Exif-result');

        if (allmetaData && Object.keys(allmetaData).length > 0) {
            let make = EXIF.getTag(this, "Make") || "Unknown";
            let model = EXIF.getTag(this, "Model") || "Unknown";
            
            let formattedData = JSON.stringify(allmetaData, null, 2);
            resultBox.innerText = `Make: ${make} \nModel: ${model} \n\nFull Metadata:\n${formattedData}`;
        } else {
            resultBox.innerText = "No EXIF data found!";
        }
    });
}

