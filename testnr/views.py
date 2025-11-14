from django.shortcuts import render, redirect


from .models import Legemiddel, Sykepleier, Bruker, BrukerLagerTilgang, Lager, Preparat, LagerPreparatBeholdning,LegemiddelLogg1
from datetime import datetime, timezone
# Create your views here.


def index(request):
    
    lager= LagerPreparatBeholdning.objects.all().filter(lager__lagernavn="Psykiatrisk mottak Drammen sykehus")
    for produkt in lager:
        print(produkt.preparat, produkt.beholdning)

    tilbakemelding = request.GET.get("tilbakemelding")
    if tilbakemelding:
        tilbakemelding="fant ikke noe legemiddel. Eller forsøker du å tukle?! din lille luring!"
    else:
        tilbakemelding=""

    return render(request, "testnr/index.html",{"tilbakemelding":tilbakemelding,
                                                "lager":lager})
    
def leggtil(request):
    return render(request, "testnr/leggtil.html")


def legemiddelside(request,legemiddel_navn):
    
    lager= LagerPreparatBeholdning.objects.all().filter(lager__lagernavn="Psykiatrisk mottak Drammen sykehus")
    print(legemiddel_navn)
    for legemiddel in lager:
        print(legemiddel.preparat)
        
        if str(legemiddel_navn) == str(legemiddel.preparat):
            loggObjekt = LegemiddelLogg1.objects.all().order_by("-tidspunkt").filter(preparat= legemiddel_navn, lager="Psykiatrisk mottak Drammen sykehus")[:25]
            
            return render(request, "testnr/legemiddelside.html",{"legemiddelnavn":legemiddel_navn,
                                                                        "legemiddelinfo":legemiddel,
                                                                        "loggObjekt":loggObjekt})
    
    #denne kan fjernes?
    lager= LagerPreparatBeholdning.objects.all().filter(lager__lagernavn="Psykiatrisk mottak Drammen sykehus")    
    
    return redirect(f"/testnr/?tilbakemelding={legemiddel_navn} finnes ikke!")
    
    
     

def ta_ut(request,legemiddel_navn):
        if request.method == "POST":
            signaturLogin = request.POST["signatur"].lower()
            pinLogin = request.POST["pin"]
            kommentarfelt = request.POST["kommentar"]
            
            radioKnapp =request.POST["radioButton"]
            uttakLegemiddel = request.POST["antallLegemiddel"]
            beholdningFørTransaksjon= request.POST["startBeholdning"]

            tilbakeMelding ="ikke gyldig forespørsel"
            if kommentarfelt.strip() == "":
                kommentarfelt = "Ingen kommentar"

            #denne variabelen skal i fremtiden kunne forteller hvilket lager vi er i
            lagernavn = "Psykiatrisk mottak Drammen sykehus"
            
            produkter=LagerPreparatBeholdning.objects.all().filter(lager=lagernavn)
            for produkt in produkter:
                    print(produkt)
                    if legemiddel_navn == str(produkt.preparat) and lagernavn == str(produkt.lager):
                        produktFunnet = True
                        break
                    else:
                        produktFunnet = False

            # feilhådtering hvis legemiddler blir endret
            if not produktFunnet:
                 tilbakeMelding = "Legemiddel ikke funnet"
                 return redirect(f"/testnr/?tilbakemelding={tilbakeMelding}")
            
            # feilhådtering hvis noen sniker inn negative verdier
            try:
                if int(beholdningFørTransaksjon) < 0 or int(uttakLegemiddel) < 0:
                    tilbakeMelding = "slutt å tukle med tall!"
                    return redirect(f"/testnr/?tilbakemelding={tilbakeMelding}")
            except ValueError:
                tilbakeMelding = "slutt å tukle med tall!"
                return redirect(f"/testnr/?tilbakemelding={tilbakeMelding}")
                 
            # feilhådtering hvis noen tukerl med radioknappene
            if radioKnapp == "1" or radioKnapp == "2":
                print("slutt å tukle med radioknappene!") 
            else:    
                tilbakeMelding = "slutt å tukle med radioknappene!"
                return redirect(f"/testnr/?tilbakemelding={tilbakeMelding}")
            
            
            try:
                brukerTilgang = BrukerLagerTilgang.objects.get(bruker=signaturLogin,lager=lagernavn)
            except BrukerLagerTilgang.DoesNotExist:
                tilbakeMelding="Bruker tilgang ikke funnet"
                return redirect(f"/testnr/legemiddel/{legemiddel_navn}")
                # loggObjekt = LegemiddelLogg1.objects.all().order_by("-tidspunkt").filter(preparat= legemiddel_navn, lager="Psykiatrisk mottak Drammen sykehus")[:25]   
                # return render(request, "testnr/legemiddelside.html",{"legemiddelnavn":legemiddel_navn,
                #                                                      "legemiddelinfo":produkt,
                #                                                     "tilbakemelding":tilbakeMelding,
                #                                                     "loggObjekt":loggObjekt})
            

            #Sjekk om bruker har en aktiv tilgang
            startTilgang = datetime.fromisoformat(str(brukerTilgang.fikkTilgang))
            sluttTilgang = datetime.fromisoformat(str(brukerTilgang.avsluttTilgang))
            now = datetime.now(timezone.utc)
            if startTilgang < now and sluttTilgang > now:
                print(f"{brukerTilgang.bruker} har en aktiv tilgang som slutter {sluttTilgang}")
                tilgang = True

            else:
                print(f"{brukerTilgang.bruker} har ikke en aktiv tilgang")
                tilgang = False
            if tilgang:
                 
                brukerobjekt = Bruker.objects.get(brukernavn=signaturLogin)     
                if pinLogin == brukerobjekt.pin:
                                
                                beholdningFørTansaksjon= produkt.beholdning


                                print(produkt.beholdning,"beholdingen før sync")
                                produkt.beholdning = int(beholdningFørTransaksjon)
                                if int(produkt.beholdning)-int(uttakLegemiddel) >= 0:
                                    print("over null!!!")
                                    
                                    print(produkt.beholdning,"beholdingen")
                                    if request.POST["radioButton"] == "1":
                                        produkt.beholdning -= int(uttakLegemiddel)
                                        produkt.save()
                                        logg= LegemiddelLogg1.objects.create(preparat=legemiddel_navn,lager=lagernavn, preparatbeholdningStart=beholdningFørTransaksjon ,preparatbeholdningSlutt=produkt.beholdning, bruker=brukerobjekt, kommentar= kommentarfelt)
                                        tilbakeMelding = f"{brukerobjekt.fulltnavn} tok ut: {uttakLegemiddel}"

                                    elif request.POST["radioButton"] == "2":
                                        produkt.beholdning += int(uttakLegemiddel)
                                        produkt.save()
                                        logg= LegemiddelLogg1.objects.create(preparat=legemiddel_navn,lager=lagernavn, preparatbeholdningStart=beholdningFørTransaksjon ,preparatbeholdningSlutt=produkt.beholdning, bruker=brukerobjekt, kommentar= kommentarfelt)
                                        tilbakeMelding = f"{brukerobjekt.fulltnavn} la til: {uttakLegemiddel} "

                                    else:
                                        produkt.beholdning = beholdningFørTansaksjon
                                        tilbakeMelding = "feil med forespørsel!"     
                                else:
                                    tilbakeMelding = "Du kan ikke ta ut mer enn aktuel beholdning!"
                                    produkt.beholdning = beholdningFørTansaksjon
                else:
                    tilbakeMelding = "feil signatur"
            #denne må sjekkes
            else:
                tilbakeMelding = f"{brukerTilgang.bruker} har ikke en aktiv tilgang"                    
                        
            loggObjekt = LegemiddelLogg1.objects.all().order_by("-tidspunkt").filter(preparat= legemiddel_navn, lager="Psykiatrisk mottak Drammen sykehus")[:25]   
            return render(request, "testnr/legemiddelside.html",{"legemiddelnavn":legemiddel_navn,
                                                                        "legemiddelinfo":produkt,
                                                                        "tilbakemelding":tilbakeMelding,
                                                                        "loggObjekt":loggObjekt})
        
        return redirect(f"/testnr/legemiddel/{legemiddel_navn}")                                                                
            
           
       
       
       
       
       
       
     