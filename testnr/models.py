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

#class Lager(models.Model):
    #lm_lager= models.ForeignKey(Legemiddel, on_delete=models.CASCADE, related_name="legemiddel")
#    beholdning = models.IntegerField(default=0)
#    lokasjon = models.CharField(max_length=64, default="mottak")
    
#    def __str__(self):
#        return f"{self.lm_lager.name} beholdning: {self.beholdning}"
