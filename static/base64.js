
let encode= document.querySelector("#encodebase64");
async function Encode()
{
    const plainText = document.querySelector('#enb64').value;
    const response = await fetch('/base64E',
        {
            "method":"POST",
            "headers":{
                "Content-Type":"application/json"
                },
            "body":JSON.stringify({"plainText":plainText})
        });
    const data = await response.json();
    let encodedText = data.EncodedText;
    let result = document.querySelector("#enresult")
    result.innerText = encodedText;
}


let decode = document.querySelector("#decode-btn");

async function Decode() {
    const encText = document.querySelector("#decodeText").value;
    console.log(encText); // remove after testing
    const response = await fetch('/base64D',{
        "method":"POST",
        "headers":{
            "Content-Type":"application/json"
        },
        "body":JSON.stringify({"encText":encText})
    });
    const data = await response.json();
    let Decode_Text = data.DecodedText;
    let result = document.querySelector("#decoresult");
    result.innerText = Decode_Text;

};
// Copy Function
function copyToClipboard(elementId) {
    const text = document.getElementById(elementId).innerText;
    navigator.clipboard.writeText(text).then(() => {
        alert("Copied to clipboard!");
    });
}