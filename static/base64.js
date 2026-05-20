
let encode= document.querySelector("#encodebase64");
async function Encode()
{
    const plainText = document.querySelector('#enb64').value;

    const encoded = btoa(plainText);
    let result = document.querySelector("#enresult")
    result.innerText = encoded;
}


let decode = document.querySelector("#decode-btn");

async function Decode() {
    const encText = document.querySelector("#decodeText").value;
    const Decode_Text = atob(encText);
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