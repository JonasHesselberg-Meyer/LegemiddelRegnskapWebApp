from django.shortcuts import render


from .models import Legemiddel, Sykepleier
# Create your views here.


def index(request):
    fullLegemiddelListe = sorted(Legemiddel.objects.values_list("name", flat=True))
    #for i in fullLegemiddelListe:
    #    print(i)

    #print(Legemiddel.objects.values("name","beholdning"))
    return render(request, "testnr/index.html",{"legemiddler":fullLegemiddelListe})
    
def leggtil(request):
    return render(request, "testnr/leggtil.html")


def legemiddelside(request,legemiddel_navn):
    listeAllelegemidler =sorted(Legemiddel.objects.values_list("name", flat=True))
    

    #for i in listeAllelegemidler:
    #     print(i)
         
    #print(legemiddel_navn)
    if legemiddel_navn in listeAllelegemidler:
        #print(Legemiddel.objects.get(name=legemiddel_navn))
        return render(request, "testnr/legemiddelside.html",{"legemiddelnavn":legemiddel_navn,
                                                             "legemiddelinfo":Legemiddel.objects.get(name=legemiddel_navn),
                                                             "beholdning":"s"})
    print("hei")
     

def ta_ut(request,legemiddel_navn):
        if request.method == "POST":
            signaturLogin = request.POST["signatur"].lower()
            pinLogin = request.POST["pin"]
            print(signaturLogin)

            alleBrukere = Sykepleier.objects.values_list("signatur", flat=True)
            print(alleBrukere)

            uttakLegemiddel = request.POST["ta_ut"]
            produkt=Legemiddel.objects.get(name=legemiddel_navn)
            
            
            if signaturLogin in alleBrukere:
                print("signatur funnet i databasen")
                signaturDatabase = Sykepleier.objects.get(signatur=signaturLogin)
                
                if pinLogin == signaturDatabase.pin:
                    print("suksess!!")
     
            
                    if request.POST["bool"] == "1":
                        produkt.beholdning -= int(uttakLegemiddel)
                        produkt.save()
                        tilbakeMelding = f"Du tok ut: {uttakLegemiddel} "
                    if request.POST["bool"] == "2":
                        produkt.beholdning += int(uttakLegemiddel)
                        produkt.save()
                        tilbakeMelding = f"Du la til: {uttakLegemiddel} "
                else:
                    tilbakeMelding = "feil signatur"
            else:
                tilbakeMelding = "feil signatur"
            
                
            return render(request, "testnr/legemiddelside.html",{"legemiddelnavn":legemiddel_navn,
                                                             "legemiddelinfo":Legemiddel.objects.get(name=legemiddel_navn),
                                                             "nybeholdning":tilbakeMelding})
            
            #return render(request, "testnr/legemiddelside.html",{"tilbakemelding":"feil Login"})
            
       
       
       
       
       
       
     