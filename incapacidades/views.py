from django.shortcuts import render
from .models import Afp, CentroCosto, ClaseIncapacidad, Empleado, Eps, Movimiento

# Create your views here.
def inicio(request):
   records = Movimiento.objects.all()
   return render(request, 'home.html', {
      'records': records,
   })


def agregar_movimiento(request):
   afps = Afp.objects.all()
   epss = Eps.objects.all()
   ccostos = CentroCosto.objects.all()
   incapacidades = ClaseIncapacidad.objects.all()

   context = {
      'afps': afps,
      'epss': epss,
      'incapacidades': incapacidades,
      'ccostos': ccostos,
   }

   return render(request, 'add-form.html', context)


def buscar_persona(request):
   query = request.GET.get('query')
   if query:
      try:
         dcto_empleado = int(query)
         empleados = Empleado.objects.filter(docto_empleado__icontains=dcto_empleado)
      except ValueError:
         empleados = Empleado.objects.filter(nombre__icontains=query)
   else:
      empleados = []

   return render(request, 'search-results.html', {'empleados': empleados})


