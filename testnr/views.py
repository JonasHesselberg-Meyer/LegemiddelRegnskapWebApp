from django.shortcuts import render


from .models import Legemiddel
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
     

def ta_ut(request,legemiddel_navn):#funkjer ikke
        if request.method == "POST":
            
            print(legemiddel_navn)
            taUtEllerUttak= "trykk 1 eller 2"
            uttakLegemiddel = request.POST["ta_ut"]
            produkt=Legemiddel.objects.get(name=legemiddel_navn)
            if request.POST["bool"] == "1":
                produkt.beholdning -= int(uttakLegemiddel)
                produkt.save()
                taUtEllerUttak = f"Du tok ut: {uttakLegemiddel} "
            if request.POST["bool"] == "2":
                produkt.beholdning += int(uttakLegemiddel)
                produkt.save()
                taUtEllerUttak = f"Du la til: {uttakLegemiddel} "
            print(produkt.beholdning)
            
            #produkt.beholdning -= 
            
            return render(request, "testnr/legemiddelside.html",{"legemiddelnavn":legemiddel_navn,
                                                             "legemiddelinfo":Legemiddel.objects.get(name=legemiddel_navn),
                                                             "nybeholdning":taUtEllerUttak})
        #else:
            #return render(request, "testnr/legemiddelside.html")
             

   # Example: Get a row where id=1
#row = MyModel.objects.get(id=1)
#specific_value = row.field_name  # Replace 'field_name' with the desired field