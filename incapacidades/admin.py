from django.contrib import admin
from .models import Afp, CentroCosto, ClaseIncapacidad, Concepto,  Diagnostico, Eps, Empleado, EstadoIncapacidad, FechaDistribucion, Movimiento

class AfpAdmin(admin.ModelAdmin):
    list_display = ('id', 'codigo', 'nit', 'nombre')
    list_display_links = ('id',)
    list_editable = ('codigo', 'nit', 'nombre')
    search_fields = ['codigo', 'nit', 'nombre']

class CentroCostoAdmin(admin.ModelAdmin):
    list_display = ('id', 'codigo', 'nombre')
    list_display_links = ('id',)
    list_editable = ('codigo', 'nombre')
    search_fields = ['nombre']

class ClaseIncapacidadAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre')
    list_display_links = ('id',)
    list_editable = ('nombre',)
    search_fields = ['nombre']

class ConceptoAdmin(admin.ModelAdmin):
    list_display = ('id', 'codigo', 'nombre')
    list_display_links = ('id',)
    list_editable = ('codigo', 'nombre')
    search_fields = ['codigo', 'nombre']

class DiagnosticoAdmin(admin.ModelAdmin):
    list_display = ('id', 'codigo', 'nombre')
    list_display_links = ('id',)
    list_editable = ('codigo', 'nombre')
    search_fields = ['codigo', 'nombre']

class EpsAdmin(admin.ModelAdmin):
    list_display = ('id', 'codigo', 'nit', 'nombre')
    list_display_links = ('id',)
    list_editable = ('codigo', 'nit', 'nombre')
    search_fields = ['codigo', 'nit', 'nombre']

class EmpleadoAdmin(admin.ModelAdmin):
    list_display = ('docto_empleado', 'nombre', 'estado', 'eps', 'afp')
    list_filter = ('genero', 'estado', 'eps', 'afp')
    search_fields = ['docto_empleado', 'nombre']

class EstadoIncapacidadAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre')
    list_display_links = ('id',)
    list_editable = ('nombre',)
    search_fields = ['nombre']

class MovimientoAdmin(admin.ModelAdmin):
    list_display = (
        'cod_incapacidad',
        'serie',
        'empleado',
        'diagnostico',
        'centro_costo',
        'concepto',
        'incapacidad'
    )
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

