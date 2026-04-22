console.log(1);
const tools = document.querySelectorAll('.card');

let timer;
document.querySelector("#search").addEventListener('keyup',(event)=>{
    clearTimeout(timer);
    timer = setTimeout(()=> {
        let qur = event.target.value.toLowerCase();
        console.log("User stoped !",qur);
        tools.forEach(tool=>{
            const toolName = tool.querySelector('h3').innerText.toLowerCase();
            if (toolName.includes(qur))
            {
                tool.style.display = "block";
            }
            else
            {
                tool.style.display = "none";
            }
        });
    },300);
});