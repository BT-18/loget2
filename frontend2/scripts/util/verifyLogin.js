async function verify(){
    try {
        const response = await fetch('http://192.168.214.1:3000/user/verify',{
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            },
            credentials: 'include',            
        });
        if (response.ok){
            return true;
        } else {
            return false;
        }
    } catch (error) {
        console.error(error)
        return false;
    }
}

export {verify};