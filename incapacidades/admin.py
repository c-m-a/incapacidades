import csv
from django.contrib import admin, messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import path, reverse
from django import forms

from .models import Afp, CentroCosto, ClaseIncapacidad, Concepto,  Diagnostico, Eps, Empleado, EstadoIncapacidad, FechaDistribucion, Movimiento

# Define a mixin class with the import_csv action
class ImportCSVActionMixin:
    def import_csv(self, request):
        model = self.model
        opts = model._meta

        if request.method == 'POST':
            form = CSVUploadForm(request.POST, request.FILES)
            if form.is_valid():
                csv_file = request.FILES['csv_file']
                if csv_file.name.endswith('.csv'):
                    csv_data = csv_file.read().decode('utf-8').splitlines()
                    reader = csv.reader(csv_data)
                    header_skipped = False

                    # Get the header row to dynamically map fields
                    header_row = next(reader)

                    for row in reader:
                        if not header_skipped:
                            header_skipped = True
                            continue  # Skip the header row

                        model_instance = model()  # Use the passed model
                        for header, value in zip(header_row, row):
                            try:
                                # Dynamically set the field value based on the header name
                                setattr(model_instance, header, value)
                            except AttributeError:
                                # Handle the case where the header doesn't match any field in the model
                                messages.error(request, f"No field '{header}' in model {model.__name__}")
                                return HttpResponseRedirect(reverse('admin:%s_%s_changelist' % (model._meta.app_label, model._meta.model_name)))

                        try:
                            model_instance.save()
                        except Exception as e:
                            # Handle the case where the save operation fails
                            messages.error(request, f"Error: {e}")
                            return HttpResponseRedirect(reverse('admin:%s_%s_changelist' % (model._meta.app_label, model._meta.model_name)))
                            # return redirect(f'admin:{model._meta.app_label}_{model._meta.model_name}_changelist')

                    messages.success(request, 'CSV file imported successfully.')
                    return HttpResponseRedirect(reverse('admin:%s_%s_changelist' % (model._meta.app_label, model._meta.model_name)))
                else:
                    messages.error(request, "Error: Invalid file format.")
            else:
                messages.error(request, "Error: Form is invalid.")
        else:
            form = CSVUploadForm()

        context = {
            'form': form,
            'opts': opts,
            'app_label': opts.app_label,
        }

        return render(
            request,
            'admin/csv_upload/index.html',
            context
        )  # Render the upload template

    # import_csv.short_description = "Import selected objects from CSV"


class AfpAdmin(admin.ModelAdmin, ImportCSVActionMixin):
    list_display = ('id', 'codigo', 'nit', 'nombre')
    list_display_links = ('id',)
    list_editable = ('codigo', 'nit', 'nombre')
    search_fields = ['codigo', 'nit', 'nombre']


    def get_urls(self):
        urls = super().get_urls()
        new_urls = [path('import-csv/', self.import_csv),]
        return new_urls + urls


class CentroCostoAdmin(admin.ModelAdmin):
    list_display = ('id', 'codigo', 'nombre')
    list_display_links = ('id',)
    list_editable = ('codigo', 'nombre')
    search_fields = ['nombre']

class ClaseIncapacidadAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'dias_empresa')
    list_display_links = ('id',)
    list_editable = ('nombre','dias_empresa')
    search_fields = ['nombre']

class ConceptoAdmin(admin.ModelAdmin):
    list_display = ('id', 'codigo', 'nombre', 'responsable')
    list_display_links = ('id',)
    list_editable = ('codigo', 'nombre', 'responsable')
    search_fields = ['codigo', 'nombre']

class CSVUploadForm(forms.Form):
    csv_file = forms.FileField()

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
    list_display = ('id', 'codigo', 'nombre')
    list_display_links = ('id',)
    list_editable = ('codigo', 'nombre',)
    search_fields = ['nombre']


class FechaDistribucionAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'fecha_inicial',
        'fecha_final',
        'salario',
        'total_dias',
        'empresa_dias',
        'empresa_valor',
        'entidad_dias',
        'entidad_valor',
    )
    list_display_links = ('id',)


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
admin.site.register(FechaDistribucion, FechaDistribucionAdmin)
admin.site.register(Movimiento, MovimientoAdmin)

