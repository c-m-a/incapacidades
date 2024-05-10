from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('agregar-movimiento/', views.agregar_movimiento, name='agregar_movimiento'),
    path('b/resultados/', views.buscar_persona, name='buscar_persona'),
]
