from django.db.models import Q
from django.shortcuts import render
from .models import Afp, CentroCosto, ClaseIncapacidad, Concepto, Diagnostico, Empleado, Eps, EstadoIncapacidad, Movimiento

# Create your views here.
def inicio(request):
   movimientos = Movimiento.objects.select_related('empleado').all()
   return render(request, 'home.html', {
      'movimientos': movimientos,
   })


def agregar_movimiento(request):
   afps = Afp.objects.all()
   epss = Eps.objects.all()
   ccostos = CentroCosto.objects.all()
   incapacidades = ClaseIncapacidad.objects.all()
   estados_incapacidades = EstadoIncapacidad.objects.all()

   context = {
      'afps': afps,
      'epss': epss,
      'incapacidades': incapacidades,
      'ccostos': ccostos,
      'estados_incapacidades': estados_incapacidades,
   }

   return render(request, 'add-form.html', context)


def buscar_personas(request):
   query = request.GET.get('query')
   if query:
      try:
         docto_empleado = int(query)
         empleados = Empleado.objects.filter(docto_empleado__icontains=docto_empleado)
      except ValueError:
         empleados = Empleado.objects.filter(nombre__icontains=query)
   else:
      empleados = []

   return render(request, 'search-results.html', {'empleados': empleados})


def buscar_personas_movimientos(request):
   query = request.GET.get('query')
   if query:
      try:
         docto_empleado = int(query)
         movimientos = Movimiento.objects.select_related('empleado').filter(
             empleado__docto_empleado__icontains=docto_empleado
         )
      except ValueError:
         movimientos = Movimiento.objects.select_related('empleado').filter(
            empleado__nombre__icontains=query
         )
   else:
      movimientos = Movimiento.objects.select_related('empleado').all()

   return render(request, 'resultados-personas-movimientos.html', {'movimientos': movimientos})


def buscar_conceptos(request):
   query = request.GET.get('query')
   if query:
      try:
         codigo = int(query)
         conceptos = Concepto.objects.filter(codigo__icontains=codigo)
      except ValueError:
         conceptos = Concepto.objects.filter(nombre__icontains=query)
   else:
      conceptos = []

   return render(request, 'resultados-conceptos.html', {'conceptos': conceptos})


def buscar_incapacidades(request):
   query = request.GET.get('query')
   if query:
      incapacidades = ClaseIncapacidad.objects.filter(nombre__icontains=query)
   else:
      incapacidades = []

   return render(request, 'resultados-conceptos.html', {'incapacidades': incapacidades})


def buscar_diagnosticos(request):
   query = request.GET.get('query')
   if query:
      try:
         codigo = int(query)
         diagnosticos = Diagnostico.objects.filter(codigo__icontains=codigo)
      except ValueError:
         diagnosticos = Diagnostico.objects.filter(nombre__icontains=query)
   else:
      diagnosticos = []

   return render(request, 'resultados-diagnosticos.html', {'diagnosticos': diagnosticos})
