const form = document.getElementById("form");
form.addEventListener("submit", (event) => {
    event.preventDefault();
    const formData = new FormData(form);
    let message = null;
    let image = null;
    for (const [key, value] of formData.entries()) {
        if (key === 'message') {
            message = value;
        } else if (key === 'image') {
            image = value;
        }
    }

    console.log(message, image);

    fetch('/api/upload', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        console.log('Success:', data);
        let historyComment = document.createElement("div");
        historyComment.className = "history_comment";
        if (message != null){
            console.log(message);
            let text = document.createElement("div");
            text.textContent = message;
            historyComment.appendChild(text);
            document.querySelector(".history_comments").appendChild(historyComment);
        }
        if (image != null){
            console.log(image.filename);
            let commentImg = document.createElement("img");
            commentImg.className = "comment_img";
            commentImg.src = data.file_name;
            historyComment.appendChild(commentImg);
            document.querySelector(".history_comments").appendChild(historyComment);
        }
    })
    .catch((error) => {
        console.error('Error:', error);
    });
});


function load_history(){
    fetch('/api/history', {
        method: 'GET'
    })
    .then(response => response.json())
    .then(data => {
        console.log('Success:', data);
        for(let item of data){
            let historyComment = document.createElement("div");
            historyComment.className = "history_comment";
            
            if (item.comment != null){
                let text = document.createElement("div");
                text.textContent = item.comment;
                historyComment.appendChild(text);
                document.querySelector(".history_comments").appendChild(historyComment);
            }
            if (item.image != null){
                let commentImg = document.createElement("img");
                commentImg.className = "comment_img";
                commentImg.src = `https://df6a6ozdjz3mp.cloudfront.net/${item.image}`;
                historyComment.appendChild(commentImg);
                document.querySelector(".history_comments").appendChild(historyComment);
            }
        }
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}

function initialize(){
    load_history();
}

window.onload = initialize;

