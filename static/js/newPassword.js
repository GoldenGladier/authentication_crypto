window.addEventListener("load", function(){
    var textPasswordHelp = document.getElementById('passwordsHelp');
    var password1 = document.getElementById('id_new_password1');
    var password2 = document.getElementById('id_new_password2');

    password1.addEventListener('keyup', function(e) {
        if(password1.value.length === 8){      
            if(password1.value === "" || password1.value === null || password1.value === ''){
                textPasswordHelp.innerHTML = "Las contraseñas no coinciden";   
            }
            else{                    
                if(password1.value === password2.value){
                    // console.log("Enter: " + password1.value);
                    textPasswordHelp.innerHTML = "Las contraseñas coinciden";
                }
                else{
                    // console.log("Enter: " + password1.value);
                    textPasswordHelp.innerHTML = "Las contraseñas no coinciden";                
                }                    
            }
        }
        else{
            textPasswordHelp.innerHTML = "La contraseña debe tener 8 caracteres";    
        }
    });    

    password2.addEventListener('keyup', function(e) {
        if(password1.value.length === 8){
            if(password2.value === "" || password2.value === null || password2.value === ''){
                textPasswordHelp.innerHTML = "Las contraseñas no coinciden";   
            }
            else{                    
                if(password2.value === password1.value){
                    // console.log("Enter: " + password2.value);
                    textPasswordHelp.innerHTML = "Las contraseñas coinciden";
                }
                else{
                    // console.log("Enter: " + password2.value);
                    textPasswordHelp.innerHTML = "Las contraseñas no coinciden";                
                }                    
            }
        }
        else{
            textPasswordHelp.innerHTML = "La contraseña debe tener 8 caracteres";    
        }

    });

    var form = document.getElementById('form_set_new_password');
    form.addEventListener('submit', function(evento) {
        evento.preventDefault();

        // alert("Enviando");
        if(aseguraPassword()){

            // Obtenemos hash (viene como un hexadecimal 32 bytes)
            hash = CryptoJS.MD5(password1.value);
            // Convertimos a string (16 bytes)
            result = hex_to_ascii(hash);
            console.log(result.toString());      
            console.log(result.length);      
            
            password1.value = result;
            password2.value = result;
            this.submit();
        }

    });

    function aseguraPassword(){
        if(password1.value.length === 8 && password2.value.length === 8 && password1.value === password2.value){
            // alert("Si coinciden");
            return true;
        }
        // alert("NO coinciden");   
        return false;
    }
   
    function hex_to_ascii(str1)
    {
       var hex  = str1.toString();
       var str = '';
       for (var n = 0; n < hex.length; n += 2) {
           str += String.fromCharCode(parseInt(hex.substr(n, 2), 16));
       }
       return str;
    }      

});


// Hash -> MD5 (128 bits -> genera 16 bytes)
// Hash -> SHA1 (máximo)