let main = document.querySelector('main');
function render(message, imageURL){ // render 留言
    let messageText = document.createTextNode(message);
    let messageDiv = document.createElement('div');
    messageDiv.setAttribute('class', 'common-style')
    messageDiv.appendChild(messageText);
    let image = document.createElement('img');
    image.setAttribute('src', imageURL)
    image.setAttribute('class', 'common-style')
    let hr = document.createElement('hr');
    main.appendChild(messageDiv);
    main.appendChild(image)
    main.appendChild(hr)
}

window.addEventListener('load', () => { // 網頁載入時 render 畫面
    fetch("/api/message", {
        method:"GET"
    }).then(res => res.json()).then((data) => {
        // console.log(data.data);
        data.data.forEach( data => render(data.message, data.image) );
    })
})

let messageData = new FormData();
let image = "";
let file = document.getElementById('select-file');
file.addEventListener('change', (e) => {
    image = e.target.files[0];
});   

document.getElementById('send-btn').addEventListener('click', () => {
    let message = document.getElementById('type-message').value;
    if(message !== "" || image !== ""){
        alert("成功送出")
        console.log('圖檔名稱', image);
        messageData.append('message', message);
        messageData.append('file', image);
        // 帶資料給後端
        fetch("/api/message", {
            method:"POST",
            body: messageData
        }).then(res => res.json()).then(data => {
                console.log(`${data.ok}`);
                document.getElementById('type-message').value = "";
                document.getElementById('select-file').value = "";
                window.location.reload()
        }).catch( err => console.log('出錯了...', err) )
    }else{
        alert("請輸入留言或圖片");
    }
})