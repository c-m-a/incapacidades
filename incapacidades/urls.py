from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('agregar-movimiento/', views.agregar_movimiento, name='agregar_movimiento'),
    path('b/conceptos/', views.buscar_conceptos, name='buscar_conceptos'),
    path('b/diagnosticos/', views.buscar_diagnosticos, name='buscar_diagnosticos'),

    # Empleados
    path('empleados/<int:id>/', views.empleado_detalles, name='empleado_detalles'),
    path('empleados/<int:empleado_id>/movimientos/<int:movimiento_id>/', views.editar_movimiento, name='editar_movimiento'),
    path('b/empleados/', views.buscar_personas, name='buscar_persona'),
    path('b/empleados/movimientos/', views.buscar_personas_movimientos, name='buscar_personas_movimientos'),
]
