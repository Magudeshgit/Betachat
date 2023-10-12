const chatbox = document.querySelector('.chatbox')
const cross_btn = document.querySelector('.crosswrap')
const rbx = document.querySelector('.rbx')

// rbx.addEventListener('click', ()=>{
//     chatbox.classList.toggle('active')
// })

// Main Chat Functionality side of things

const joinbtn = document.querySelectorAll('.joinbtn')
const DOM_source = document.querySelector('.chatwrap')
const room_id = document.querySelector('.room_id')
const chat_room = document.querySelector('.roomname')
const beta_room = document.querySelector('.roomhead')
const beta_desc = document.querySelector('.room_desc')

joinbtn.forEach((i)=>{
    i.addEventListener('click', joinfunc)
})

function joinfunc(e)
{
    FORM = document.querySelector('.chatform')
    const UID = e.target.parentNode.parentNode.childNodes[1].childNodes[3].innerHTML.slice(0,11)
    const descrip = e.target.parentNode.parentNode.childNodes[1].childNodes[5].innerHTML
    const room_name = e.target.parentNode.parentNode.childNodes[1].childNodes[1].innerHTML
    window.keyword = e.target.parentNode.parentNode.childNodes[1].childNodes[7].innerHTML
    window.room_key=e.target.parentNode.parentNode.childNodes[1].childNodes[1].innerText
    room_id.innerHTML = UID
    beta_room.innerHTML = room_name
    beta_desc.innerHTML = descrip


    const WSURL = `ws://${window.location.host}/ChatRoom/${UID}/`
    console.log(WSURL)
    window.WSINS = new WebSocket(WSURL)
    chatbox.classList.toggle('active')
    
    cross_btn.addEventListener('click', ()=>{
        chatbox.classList.toggle('active')
        WSINS.close()
    })

    FORM.addEventListener('submit', SendProtocol)
    WSINS.onmessage = ReceiveProtocol   
}


function AES_Encryptor(message) {
    let encrypted = CryptoJS.AES.encrypt(message, room_key);
    return encrypted.toString()
}
function AES_Decryptor(message) {
    console.log(room_key)
    let decrypted = CryptoJS.AES.decrypt(message, room_key);
    return decrypted.toString(CryptoJS.enc.Utf8)
}
function ReceiveProtocol(e) {
    data = JSON.parse(e.data)
    //console.log(data)
    if (data.status != '102')
    {
        actualchat = document.createElement("div")
        userdom = document.createElement("p")
        msgdom = document.createElement("p")

        actualchat.className = 'actualchat'
        userdom.className = 'username'
        msgdom.className = 'message'

        DOM_source.appendChild(actualchat)
        actualchat.appendChild(userdom)
        actualchat.appendChild(msgdom)

        userdom.innerHTML = data.username
        msgdom.innerHTML = AES_Decryptor(data.message)

        let objDiv = document.querySelector(".chatwrap");
        objDiv.scrollTop = objDiv.scrollHeight;
    }
}
