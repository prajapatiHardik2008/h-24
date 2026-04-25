    function Rot()
    {
        const Text = document.querySelector("#Text").value;
        const key = parseInt(document.querySelector("#key").value);

        let encText = ""
        for(let i = 0 ; i<Text.length;i++)
        {
            let c = Text[i];
            let code = Text.charCodeAt(i);

            if(code >= 97 && code <= 122)
            {
                encText+=String.fromCharCode((code - 97 + key) %26 + 97);
            }
            else if(code >= 65 && code <=90)
            {
                encText+=String.fromCharCode((code - 65 + key) % 26 + 65);
            }
            else
            {
                encText+=c;
            }
        }
        return encText;
    }


let btn = document.querySelector("#rot");

btn.addEventListener("click",()=>{
    let result = document.querySelector(".result");
    let encText = Rot()
    result.innerText = encText;
});