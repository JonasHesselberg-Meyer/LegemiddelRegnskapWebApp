from django.db import models

# Create your models here.
class Legemiddel(models.Model):
    name = models.CharField(max_length= 64)
    ab_prep = models.CharField(max_length=1)
    beholdning = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.name}"
    

class Sykepleier(models.Model):
    signatur = models.CharField(max_length= 6, primary_key=True)
    fulltNavn = models.CharField(max_length= 64)
    pin = models.CharField(max_length= 4)
    
    def __str__(self):
        return f"{self.signatur}"

# ny database design.

class Stillingstype(models.Model):
    stillingstype = models.CharField(max_length=64, default="Sykepleier")

    def __str__(self):
        return f"{self.stillingstype}"


class Lokasjoner(models.Model):
    lokasjoner = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.lokasjoner}"
    
class Lagertype(models.Model):
    lagertype = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.lagertype}"




class Bruker(models.Model):
    brukernavn = models.CharField(max_length= 6, primary_key=True)
    fulltnavn = models.CharField(max_length= 64)
    stillingstype = models.ForeignKey(Stillingstype,blank=False, on_delete=models.CASCADE)
    pin = models.CharField(max_length= 4)
    
    def __str__(self):
        return f"{self.brukernavn}"
    


class Lager(models.Model):
    
    lagernavn = models.CharField(max_length= 64, primary_key=True)
    lokasjon = models.ForeignKey(Lokasjoner,blank=False, on_delete=models.CASCADE)
    lagertype = models.ForeignKey(Lagertype,blank=False, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.lagernavn}"
    
    
    
class BrukerLagerTilgang(models.Model):
    #pk= models.CompositePrimaryKey("lager_id","bruker_id")
    bruker=models.ForeignKey(Bruker, blank=False, on_delete=models.CASCADE)
    lager=models.ForeignKey(Lager, blank=False, on_delete=models.CASCADE)
    fikkTilgang = models.DateTimeField(blank=False)
    avsluttTilgang = models.DateTimeField()
    
    
    def __str__(self):
        return f"{self.bruker}-{self.lager}"
    

class Preparat(models.Model):
    preparatnavn = models.CharField(max_length= 64)
    virkestoff = models.CharField(max_length=64)
    ab_prep = models.CharField(max_length=1)
    styrke = models.PositiveIntegerField()
    styrekbenevnelse = models.CharField(max_length=64)
    legemiddelform = models.CharField(max_length=64)
    

    def __str__(self):
        return f"{self.preparatnavn} {self.styrke}{self.styrekbenevnelse}"
    

class LagerPreparatBeholdning(models.Model):
    lager = models.ForeignKey(Lager, on_delete=models.CASCADE,blank=False)
    preparat = models.ForeignKey(Preparat, on_delete=models.CASCADE,blank=False)
    beholdning = models.PositiveIntegerField(blank=False)

    class Meta:
        unique_together = ('lager','preparat')
    
    

    def __str__(self):
        return f"{self.lager}-{self.preparat}: {self.beholdning}"
    

    

class LegemiddelLogg1(models.Model):
    preparat = models.CharField(max_length=64)
    preparatbeholdningStart= models.PositiveIntegerField(blank=False)
    preparatbeholdningSlutt = models.PositiveIntegerField(blank=False)
    lager= models.CharField(max_length=64,default="test")
    bruker = models.ForeignKey(Bruker, on_delete=models.DO_NOTHING, blank=False)
    tidspunkt = models.DateTimeField(blank=False, auto_now=True)
    kommentar = models.TextField(default="Ingen kommentar")
    
    

    def __str__(self):
        return f"{self.preparat}-{self.bruker}-{self.preparatbeholdningSlutt}--{self.lager}"
    

