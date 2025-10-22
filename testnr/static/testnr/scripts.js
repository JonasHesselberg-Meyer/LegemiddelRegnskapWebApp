

const søkefeltVerdi = document.getElementById("søkefelt");
const legemiddelListe = document.querySelectorAll("#legemiddelListe li");




søkefeltVerdi.addEventListener("input",() => {
    

    legemiddelListe.forEach(item => {
        let legemiddelNavn = item.textContent;
        
            if(legemiddelNavn.includes(søkefeltVerdi.value.toLowerCase())){
                item.style.display = ""
                
            }
            else{
                item.style.display = "none";
            }
            
                
    });
})






function velkommenHilsen(){
    confirm("hei ta eller gi noe dop?");
    

}





// funksjon for knappen for uttak eller legge til legemiddel.
function taUTelleruttak(){

                let switchKnapp = document.getElementById("switch")
                console.log(switchKnapp.value);

                if(switchKnapp.value ==="1"){
                    switchKnapp.value = 2
                    trykkKnapp.innerHTML="Legg til"
                    return;
                }
                if(switchKnapp.value ==="2"){
                    switchKnapp.value = 1
                    trykkKnapp.innerHTML="Uttak"
                    return;
                }
        }