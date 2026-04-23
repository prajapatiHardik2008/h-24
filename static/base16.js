const ALPHABET = 'abcdefghijklmnop';

function Encodeb16(plainText)
{
    let enc = ""
    for(let i = 0 ; i < plainText.length ; i++)
    {
        let Charcode = plainText.charCodeAt(i);
        // make binary code of 8 bit like 01100110
        let binary = Charcode.toString(2).padStart(8,'0');
        let firsthalf = binary.substring(0, 4);
        let sechalf = binary.substring(4);
        //  convert into decimal  and map into ALPHABET  
        enc += ALPHABET[parseInt(firsthalf, 2)];
        enc += ALPHABET[parseInt(sechalf, 2)];

    }
    return enc
}

let Ebtn =  document.querySelector("#b16Encoding");
Ebtn.addEventListener('click',()=>{
    let Text = document.querySelector("#Enctext").value;
    let EncodedText = Encodeb16(Text);
    let resultEn = document.querySelector("#Encresult");
    resultEn.innerText = EncodedText;
});

function Decodeb16(encText)
{
    let org_text = "";
    for(let i =0;i < encText.length ; i+= 2)
    {
        let pose1 = ALPHABET.indexOf(encText[i]);
        let pose2 = ALPHABET.indexOf(encText[i + 1]);
        let charcode = (pose1 << 4) | pose2;
        org_text+=String.fromCharCode(charcode);
    }
    return org_text;
}

let Dbtn = document.querySelector("#b16decoding");

Dbtn.addEventListener("click",()=>{
    let text = document.querySelector("#Decotext").value;
    let DecodedText = Decodeb16(text);
    let Dresult = document.querySelector("#Decresult");
    Dresult.innerText = DecodedText;
});