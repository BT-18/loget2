import {verify} from './util/verifyLogin.js'

if (await verify() == false){
    document.location.href="index.html"
}