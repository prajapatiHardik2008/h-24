let btn = document.querySelector("#Getdata");
let result = document.querySelector(".result");
btn.addEventListener("click",async ()=>{
    let ip = document.querySelector("#IP").value;
    result.innerText = `Wait a min ${ip}`
    url = `http://ip-api.com/json/${ip}`
    response = await fetch(url);
    data = await response.json()
   
    result.innerText = JSON.stringify(data,null,2);
});