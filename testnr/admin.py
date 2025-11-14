from django.contrib import admin

from .models import Legemiddel, Sykepleier,Lager, BrukerLagerTilgang, Bruker, LagerPreparatBeholdning, Preparat, LegemiddelLogg1, Stillingstype, Lagertype, Lokasjoner

# Register your models here.
admin.site.register(Legemiddel)
admin.site.register(Sykepleier)
admin.site.register(Lager)
admin.site.register(Bruker)
admin.site.register(BrukerLagerTilgang)
admin.site.register(LagerPreparatBeholdning)
admin.site.register(Preparat)
admin.site.register(LegemiddelLogg1)
admin.site.register(Stillingstype)
admin.site.register(Lagertype)
admin.site.register(Lokasjoner)



