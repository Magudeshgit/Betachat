function Emailvalidation(email) {   
    emailregex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
    if (emailregex.test(email) === !true){
        errortxt.innerHTML = 'Enter a Valid Email Address'
        return false
    }
    else{
        return true
    }
}
function usernamevalidation(username) {
    
}