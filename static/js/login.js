window.addEventListener("load", function(){

    var password1 = document.getElementById('id_contraseña_aux');
    var password_hash = this.document.getElementById('id_contraseña');

    var form = document.getElementById('form_login');
    form.addEventListener('submit', function(evento) {
        evento.preventDefault();

        // alert("Enviando");

        if(password1.value.length === 8){

            // Obtenemos hash (viene como un hexadecimal 32 bytes)
            hash = CryptoJS.MD5(password1.value);
            // Convertimos a string (16 bytes)
            result = hex_to_ascii(hash);
            console.log(result.toString());      
            console.log(result.length);      
            
            password_hash.value = result;
            this.submit();
        }

    });

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