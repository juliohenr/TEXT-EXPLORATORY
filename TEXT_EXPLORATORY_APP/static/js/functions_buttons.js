
buttonRun = document.querySelector(".buttonRun")



buttonRun.addEventListener("click", function() {

    console.log("clicou aqui!")
    
const Http = new XMLHttpRequest();

const url='http://127.0.0.1:8000/persist_results';


contentTwitter = document.querySelector(".contentTwitter").value;

console.log(contentTwitter)

dados = {data:contentTwitter};

let data = new FormData();

data.append("contentTwitter", contentTwitter);

console.log(dados)

Http.open("POST", url,true);

Http.send(data);

Http.onreadystatechange = (e) => {
  console.log(Http.responseText);
  location.reload(true);
}


}


)


