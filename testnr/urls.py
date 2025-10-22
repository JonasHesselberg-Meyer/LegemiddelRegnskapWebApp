
from django.urls import path
from . import views
app_name = "testnr"
urlpatterns = [
    path("", views.index, name="index"),
    path("leggtil", views.leggtil, name="leggtil"),
    path("legemiddel/<str:legemiddel_navn>", views.legemiddelside, name="legemiddel"),
    path("legemiddel/<str:legemiddel_navn>/ta_ut", views.ta_ut, name="ta_ut")#funker ikke
]

