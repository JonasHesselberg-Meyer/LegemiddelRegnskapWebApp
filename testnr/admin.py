from django.contrib import admin

from .models import Legemiddel, Sykepleier

# Register your models here.
admin.site.register(Legemiddel)
admin.site.register(Sykepleier)
