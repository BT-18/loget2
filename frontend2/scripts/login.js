const form = document.getElementById('login');
const statusText = document.getElementById('status');
const totpInput = document.getElementById('totp');
const totpLabel = document.getElementById('totpLabel');
const emailInput = document.getElementById('email');
const passwordInput = document.getElementById('password');

let msg = "";

function showMessage(message, error = false){
    statusText.hidden = false;
    statusText.textContent = message;
    
    if (error) {
        statusText.style = "color: red";
    } else {
        statusText.style = "color: green";
    }
}

async function statusManagement(response){
    error = false;
    const result = await response.json();
    if (response.status == 501) {
        msg = "Erreur lors de la connection"
    } else if (response.status == 401 && result ["msg"] != "TOTP_REQUIRED") {
        error = true;
        msg = "Le mot de passe ou identifiant de connexion est incorrecte";
    } else if (result ["msg"] == "TOTP_REQUIRED"){
        error = true;
        msg = "Veuillez entrer votre code de double authentification"
    } else if (response.ok  ) {
        msg = "Connection réussie";
    } else {
        msg = "Erreur inconnue";
    }
    
    showMessage(msg, error);
    console.log('Réponse du serveur :', result["msg"]);
    

   

    if (result["msg"] == "TOTP_REQUIRED"){
        emailInput.disabled = true;
        passwordInput.disabled = true
        totpInput.hidden = false;
        totpLabel.hidden = false;
        
    } else if (response.ok) {
        window.location.href = "dashboard.html";
    } 

}

form.addEventListener('submit', async (e) => {
    e.preventDefault();

    const formData = new FormData(form);
    const data = Object.fromEntries(formData);

    

    if (window.getComputedStyle(totpInput).display === "none") {

        try {
            const response = await fetch('http://192.168.214.1:3000/user/authenticate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                credentials: 'include', 
                body: JSON.stringify(data),
            });

            statusManagement(response);


        } catch (error) {;
            showMessage(msg, true)
            console.error(error);
        }
    } else {
        try {
            const response = await fetch('http://192.168.214.1:3000/user/check_totp', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                credentials: 'include', 
                body: JSON.stringify(data),
            });

            statusManagement(response);


        } catch (error) {
            console.log("Received Error");
            showMessage(msg, true)
            console.error(error);
        }
    }
    
});
