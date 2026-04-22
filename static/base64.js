
let encode= document.querySelector("#encodebase64");
async function Encode()
{
    const plainText = document.querySelector('#enb64').value;
    console.log(plainText)
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