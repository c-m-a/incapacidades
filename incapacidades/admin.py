from django.contrib import admin
from .models import Afp, CentroCosto, ClaseIncapacidad, Concepto,  Diagnostico, Eps, Empleado, EstadoIncapacidad, FechaDistribucion, Movimiento

admin.site.register(Afp)
admin.site.register(CentroCosto)
admin.site.register(ClaseIncapacidad)
admin.site.register(Concepto)
admin.site.register(Diagnostico)
admin.site.register(Eps)
admin.site.register(Empleado)
admin.site.register(EstadoIncapacidad)
admin.site.register(FechaDistribucion)
admin.site.register(Movimiento)

