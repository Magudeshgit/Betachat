let form = document.querySelector('.form')
const XML = new XMLHttpRequest()


form.addEventListener('submit', (e)=>{
    e.preventDefault()
    const formdata = new FormData(form)
    console.log(formdata)
    request = XML.open('POST', '/Signin/')
    XML.onload = function (){
        if (XML.status === 200){
            console.log('Success')
        }
        else{
            console.log('failed')
        }
    }
    XML.send(formdata)
    response = XML.open('GET', '/Signin/')
    
})