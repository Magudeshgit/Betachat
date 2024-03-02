//AWS KMS CONFIGURATIONS
AWS.config.region="ap-south-1"
AWS.config.credentials = new AWS.CognitoIdentityCredentials({
    IdentityPoolId: ""
})

const KEYID = ' '
const KMS = new AWS.KMS()
const Translate = new AWS.Translate()

const GAPI_KEY = ''
const TranslateURL = 'https://translation.googleapis.com/language/translate/v2?key='+GAPI_KEY

const chatbox = document.querySelector('.chatbox')
const cross_btn = document.querySelector('.crosswrap')
const rbx = document.querySelector('.rbx')
const joinbtn = document.querySelectorAll('.joinbtn')
const DOM_source = document.querySelector('.chatwrap')
const room_id = document.querySelector('.room_id')
const chat_room = document.querySelector('.roomname')
const beta_room = document.querySelector('.roomhead')
const beta_desc = document.querySelector('.room_desc')
const roomlink = document.querySelector('.roomlink')
const fileuplink = document.querySelector('.fileuplink')
let Loaded = false

joinbtn.forEach((i)=>{
    i.addEventListener('click', joinfunc)
})

function UpdateChats(UID) {
    data = fetch('http://127.0.0.1:8000/getmessages/'+UID, {method: 'GET'}).then(dt => dt.json()).then(pt=>pt)
    data.then(fd=>fd.forEach(chat=>{
        let jsonfied = {data: JSON.parse(chat['content'])}
        AWS_Decryptor(jsonfied).then((decrypted_message)=>{
                decrypted_message = TranslateText(decrypted_message).then(decrypted_message=>{

                actualchat = document.createElement("div")
                userdom = document.createElement("p")
                msgdom = document.createElement("p")
                timestamp = document.createElement("p")

                if (chat['user'] === window.username)
                {
                    actualchat.className = 'actualchat flex align-right flex-col'
                    userdom.className = 'username'
                    msgdom.className = 'message'
                    timestamp.className = 'timestamp'
                }

                else
                {
                    actualchat.className = 'actualchat bg'
                    userdom.className = 'username'
                    msgdom.className = 'message'
                    timestamp.classList = 'timestamp'
                }


                DOM_source.appendChild(actualchat)
                actualchat.appendChild(userdom)
                actualchat.appendChild(msgdom)
                actualchat.appendChild(timestamp)

                let date  = new Date(chat['timestamp'])

                userdom.innerHTML = chat['user']
                msgdom.innerHTML = decrypted_message['TranslatedText']
                timestamp.innerHTML = date.toLocaleTimeString()//date.getHours() +':'+ date.getMinutes() + ' | ' + date.getDay()
            })
        })
    })).then(()=>Loaded = true)
    console.log(Loaded)
}

cross_btn.addEventListener('click', ()=>{
    chatbox.classList.toggle('active')
    DOM_source.innerHTML = ''
    WSINS.close()
})

function joinfunc(e)
{
    FORM = document.querySelector('.chatform')
    console.log(e.target.parentNode.parentNode.childNodes[1].childNodes)
    const room_name = e.target.parentNode.parentNode.childNodes[1].childNodes[1].innerHTML  
    const UID = e.target.parentNode.parentNode.childNodes[1].childNodes[3].innerHTML.slice(0,11)
    console.log('adsasd', UID)
    const descrip = e.target.parentNode.parentNode.childNodes[1].childNodes[7].innerHTML
    const roomdbid = e.target.parentNode.parentNode.childNodes[1].childNodes[11].innerHTML
    window.keyword = e.target.parentNode.parentNode.childNodes[1].childNodes[9].innerHTML
    window.room_key=e.target.parentNode.parentNode.childNodes[1].childNodes[1].innerText
    window.UniqueID = UID
    room_id.innerText = UID
    beta_room.innerHTML = room_name
    beta_desc.innerHTML = descrip
    fileuplink.href = '/sharefiles/'+roomdbid



    data = fetch('http://127.0.0.1:8000/getmessages/'+UID, {method: 'GET'}).then(dt => dt.json()).then(pt=>pt)

    //Updating Chat History
    UpdateChats(UID)

    if (Loaded===true){
        console.log(Loaded)
        DOM_source.scrollTop = DOM_source.scrollHeight
    }
   

    const WSURL = `ws://${window.location.host}/ChatRoom/${UID}/`
    //console.log(WSURL)
    window.WSINS = new WebSocket(WSURL)
    chatbox.classList.toggle('active')

    let objDiv = document.querySelector(".chatwrap");
    objDiv.scrollTop = objDiv.scrollHeight

    FORM.addEventListener('submit', SendProtocol)
    WSINS.onmessage = ReceiveProtocol   
}
var databro;
async function AWS_Encryptor(message) {
    const encdata = new Promise((resolve,reject)=>{
        KMS.encrypt({
            KeyId: KEYID,
            Plaintext: message
        }, (err,dat)=>{
            if(!err)
            {
                databro = dat
                resolve(databro)
                //console.log(dat['CiphertextBlob'])
            }
            else{   
                reject(err)
                console.log(err)
            }
        })
    })
    const dt = await encdata
    return await dt.CiphertextBlob
}

async function AWS_Decryptor(message) {
    let sd = new Uint8Array(message['data'])
    const encdata = new Promise((resolve,reject)=>{
        KMS.decrypt({
            KeyId: KEYID,
            CiphertextBlob: sd
        }, (err,dat)=>{
            if(!err)
            {
                resolve(String.fromCharCode(...dat['Plaintext']))
            }
            else{   
                console.log(err)
                reject(err)
            }
        })
    })
    const dt = await encdata
    return await dt
}

function TranslateText(message)
{
    const params={
        SourceLanguageCode: "auto",
        TargetLanguageCode: window.language_preference,
        Text: message
    }
    const translation = new Promise((resolve, reject)=>{
        Translate.translateText(params, (err,data)=>{
            if (err)
            {
                reject(err)
            }
            else
            {
                resolve(data)
            }
        })
    })
    return translation
}

function ReceiveProtocol(e) {
    data = JSON.parse(e.data)
    console.log(data)
    if (data.status != '102')
    {
        actualchat = document.createElement("div")
        userdom = document.createElement("p")
        msgdom = document.createElement("p")

        DOM_source.appendChild(actualchat)
        actualchat.appendChild(userdom)
        actualchat.appendChild(msgdom)

        AWS_Decryptor(data['message']).then((resp)=>{
            TranslateText(resp).then(translatedtext=>{
                if(data.username === window.username)
                {
                    actualchat.className = 'actualchat flex align-right flex-col'
                    userdom.className = 'username'
                    msgdom.className = 'message'
                    //timestamp bug
                    timestamp.className = 'timestamp'
                    userdom.innerHTML = data.username
                    msgdom.innerHTML = translatedtext['TranslatedText']
                }
                else
                {
                    actualchat.className = 'actualchat'
                    userdom.className = 'username'
                    msgdom.className = 'message'
                    timestamp.className = 'timestamp'
                    userdom.innerHTML = data.username
                    msgdom.innerHTML = translatedtext['TranslatedText']
                }
            })
        })


        DOM_source.scrollTop = DOM_source.scrollHeight
    }
}
    