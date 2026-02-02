const form = document.getElementById('login');
const statusText = document.getElementById('status');
const totpInput = document.getElementById('totp')
const totpLabel = document.getElementById('totpLabel')

let msg = "";

async function statusManagement(response){

    const result = await response.json();
    if (response.status == 501) {
        msg = "Erreur lors de la connection"
        throw new Error(msg +  " : " +  response.status);
    } else if (response.status == 401 && result ["msg"] != "TOTP_REQUIRED") {
        console.log(response.status)
        msg = "Le mot de passe ou identifiant de connexion est incorrecte";
        throw new Error(msg +  " : " +  response.status);
    } else if (result ["msg"] == "TOTP_REQUIRED"){
        msg = "Veuillez entrer votre code de double authentification"
    } else if (response.ok  ) {
        msg = "Connection réussie";
    } else {
        msg = "Erreur inconnue";
        throw new Error(msg +  " : " +  response.status);
    }
    
    statusText.hidden = false;
    statusText.textContent = msg;
    statusText.style = "color: green";
    console.log('Réponse du serveur :', result["msg"]);
    

   

    if (result["msg"] == "TOTP_REQUIRED"){
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


        } catch (error) {
            alert("test");
            statusText.hidden = false;
            statusText.textContent = msg;
            statusText.style = "color: red"
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
            statusText.hidden = false;
            statusText.textContent = msg;
            statusText.style = "color: red"
            console.error(error);
        }
    }
    
});
