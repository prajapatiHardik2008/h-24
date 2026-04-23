const ALPHABET = 'abcdefghijklmnop';

// --- ENCODING LOGIC ---
function Encodeb16(plainText) {
    let enc = "";
    for(let i = 0 ; i < plainText.length ; i++) {
        let Charcode = plainText.charCodeAt(i);
        let binary = Charcode.toString(2).padStart(8, '0');
        let firsthalf = binary.substring(0, 4);
        let sechalf = binary.substring(4);
        
        enc += ALPHABET[parseInt(firsthalf, 2)];
        enc += ALPHABET[parseInt(sechalf, 2)];
    }
    return enc;
}

// --- DECODING LOGIC ---
function Decodeb16(encText) {
    // Remove spaces if any
    encText = encText.trim();
    let org_text = "";
    
    // Base16 (a-p) always in pair 
    if (encText.length % 2 !== 0) return "Invalid Encoded Text!";

    for(let i = 0; i < encText.length ; i += 2) {
        let pose1 = ALPHABET.indexOf(encText[i]);
        let pose2 = ALPHABET.indexOf(encText[i + 1]);
        
        // if char are not valid 
        if (pose1 === -1 || pose2 === -1) return "Error: Invalid Characters!";

        let charcode = (pose1 << 4) | pose2;
        org_text += String.fromCharCode(charcode);
    }
    return org_text;
}

// --- EVENT LISTENERS ---

// Encoding Button
let Ebtn = document.querySelector("#b16Encoding");
if(Ebtn) {
    Ebtn.addEventListener('click', () => {
        let text = document.querySelector("#Enctext").value;
        let resultEn = document.querySelector("#Encresult");
        
        if(text.trim() !== "") {
            resultEn.innerText = Encodeb16(text);
        } else {
            resultEn.innerText = "Please enter some text...";
        }
    });
}

// Decoding Button
let Dbtn = document.querySelector("#b16decoding");
if(Dbtn) {
    Dbtn.addEventListener("click", () => {
        let text = document.querySelector("#Decotext").value;
        let Dresult = document.querySelector("#Decresult");
        
        if(text.trim() !== "") {
            Dresult.innerText = Decodeb16(text);
        } else {
            Dresult.innerText = "Please enter encoded text...";
        }
    });
}