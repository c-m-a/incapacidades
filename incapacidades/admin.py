from django.contrib import admin
from .models import Afp, CentroCosto, ClaseIncapacidad, Concepto,  Diagnostico, Eps, Empleado, EstadoIncapacidad, FechaDistribucion, Movimiento

class AfpAdmin(admin.ModelAdmin):
    search_fields = ['codigo', 'nit', 'nombre']

class CentroCostoAdmin(admin.ModelAdmin):
    search_fields = ['nombre']

class ClaseIncapacidadAdmin(admin.ModelAdmin):
    search_fields = ['nombre']

class ConceptoAdmin(admin.ModelAdmin):
    search_fields = ['codigo', 'nombre']

class DiagnosticoAdmin(admin.ModelAdmin):
    search_fields = ['codigo', 'nombre']

class EpsAdmin(admin.ModelAdmin):
    search_fields = ['codigo', 'nit', 'nombre']

class EmpleadoAdmin(admin.ModelAdmin):
    search_fields = ['docto_empleado', 'nombre']

class EstadoIncapacidadAdmin(admin.ModelAdmin):
    search_fields = ['nombre']

class MovimientoAdmin(admin.ModelAdmin):
    search_fields = ['cod_incapacidad', 'serie']

admin.site.register(Afp, AfpAdmin)
admin.site.register(CentroCosto, CentroCostoAdmin)
admin.site.register(ClaseIncapacidad, ClaseIncapacidadAdmin)
admin.site.register(Concepto, ConceptoAdmin)
admin.site.register(Diagnostico, DiagnosticoAdmin)
admin.site.register(Eps, EpsAdmin)
admin.site.register(Empleado, EmpleadoAdmin)
admin.site.register(EstadoIncapacidad, EstadoIncapacidadAdmin)
admin.site.register(FechaDistribucion)
admin.site.register(Movimiento, MovimientoAdmin)

