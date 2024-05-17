from django.shortcuts import redirect, render, get_object_or_404
from .models import Afp, CentroCosto, ClaseIncapacidad, Concepto, Diagnostico, Empleado, Eps, EstadoIncapacidad, Movimiento

# Create your views here.
def inicio(request):
   movimientos = Movimiento.objects.select_related('empleado').all()
   return render(request, 'home.html', {
      'movimientos': movimientos,
   })


def agregar_movimiento(request):
   afps = Afp.objects.all().order_by('nombre')
   epss = Eps.objects.all().order_by('nombre')
   ccostos = CentroCosto.objects.all().order_by('nombre')
   conceptos = Concepto.objects.all().order_by('codigo')
   diagnosticos = Diagnostico.objects.all().order_by('codigo')
   incapacidades = ClaseIncapacidad.objects.all().order_by('nombre')
   estados_incapacidades = EstadoIncapacidad.objects.all().order_by('nombre')

   if request.method == 'POST':
      docto_empleado = request.POST.get('docto_empleado')
      serie = request.POST.get('serie')
      nombre = request.POST.get('nombre')
      fecha_nacimiento = request.POST.get('fecha_nacimiento')
      fecha_ingreso = request.POST.get('fecha_ingreso')
      estado = request.POST.get('estado')
      genero = request.POST.get('genero')
      eps_id = request.POST.get('eps')
      afp_id = request.POST.get('afp')
      arl_nit = request.POST.get('arl_nit')
      arl_nombre = request.POST.get('arl_nombre')
      fecha_recepcion = request.POST.get('fecha_recepcion')
      calendario = request.POST.get('calendario')
      movimiento_centro_costos_id = request.POST.get('movimiento_centro_costos_id')
      clase_incapacidad_id = request.POST.get('clase_incapacidad_id')
      cod_incapacidad = request.POST.get('cod_incapacidad')
      concepto_id = request.POST.get('concepto_id')
      diagnostico_id = request.POST.get('diagnostico_id')
      fecha_inicio = request.POST.get('fecha_inicio')
      fecha_fin = request.POST.get('fecha_fin')
      fecha_inicio_temp = '2024-05-02'
      fecha_fin_temp = '2024-05-02'
      dias = request.POST.get('dias')
      prorroga = False if request.POST.get('prorroga') == '' else True
      observaciones = request.POST.get('observaciones')
      salario = request.POST.get('salario')
      valor_cia = request.POST.get('valor_cia')
      cuenta_cobrar = request.POST.get('cuenta_cobrar')
      estado_incapacidad_id = request.POST.get('estado_incapacidad_id')
      genera_pago = False if request.POST.get('genera_pago') == '' else True
   
      existe_empleado = Empleado.objects.filter(docto_empleado=docto_empleado).exists()
      existe_movimiento = Movimiento.objects.filter(serie=serie).exists()
      error_empleado = 'Número de documento duplicado' if existe_empleado else None
      error_movimiento = 'Número de serie duplicado' if existe_movimiento else None
      registros_duplicados = existe_empleado or existe_movimiento

      if registros_duplicados:
         return render(request, 'add-form.html', {
            'error_empleado': error_empleado,
            'error_movimiento': error_movimiento,
            'afps': afps,
            'ccostos': ccostos,
            'conceptos': conceptos,
            'diagnosticos': diagnosticos,
            'epss': epss,
            'incapacidades': incapacidades,
            'estados_incapacidades': estados_incapacidades,
         })
      else:
         afp = Afp.objects.get(pk=afp_id)
         centro_costo = CentroCosto.objects.get(pk=movimiento_centro_costos_id)
         concepto = Concepto.objects.get(pk=concepto_id)
         diagnostico = Diagnostico.objects.get(pk=diagnostico_id)
         eps = Eps.objects.get(pk=eps_id)
         clase_incapacidad = ClaseIncapacidad.objects.get(pk=clase_incapacidad_id)
         estado_incapacidad = EstadoIncapacidad.objects.get(pk=estado_incapacidad_id)

         empleado = Empleado.objects.create(
            docto_empleado=docto_empleado,
            nombre=nombre,
            fecha_nacimiento=fecha_nacimiento,
            fecha_ingreso=fecha_ingreso,
            estado=estado,
            genero=genero,
            eps=eps,
            afp=afp,
            arl_nit=arl_nit,
            arl_nombre=arl_nombre,
         )

         movimiento = Movimiento.objects.create(
            cod_incapacidad=cod_incapacidad,
            serie=serie,
            fecha_recepcion=fecha_recepcion,
            fecha_inicio=fecha_inicio_temp,
            fecha_fin=fecha_fin_temp,
            prorroga=prorroga,
            dias=dias,
            salario=salario,
            calendario=calendario,
            valor_cia=valor_cia,
            cuenta_cobrar=cuenta_cobrar,
            genera_pago=genera_pago,
            observaciones=observaciones,
            empleado=empleado,
            eps=eps,
            afp=afp,
            diagnostico=diagnostico,
            centro_costo=centro_costo,
            concepto=concepto,
            incapacidad=clase_incapacidad,
            estado_incapacidad=estado_incapacidad,
         )

         return redirect('/')

   context = {
      'afps': afps,
      'ccostos': ccostos,
      'conceptos': conceptos,
      'diagnosticos': diagnosticos,
      'epss': epss,
      'incapacidades': incapacidades,
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


def empleado_detalles(request, id):
   # Obtener el empleado con el ID proporcionado
   afps = Afp.objects.all().order_by('nombre')
   empleado = get_object_or_404(Empleado, pk=id) 
   epss = Eps.objects.all().order_by('nombre')
   ccostos = CentroCosto.objects.all().order_by('nombre')
   incapacidades = ClaseIncapacidad.objects.all().order_by('nombre')
   estados_incapacidades = EstadoIncapacidad.objects.all().order_by('nombre')

   movimientos = Movimiento.objects.filter(empleado=empleado)

   context = {
      'afps': afps,
      'ccostos': ccostos,
      'empleado': empleado,
      'epss': epss,
      'estados_incapacidades': estados_incapacidades,
      'incapacidades': incapacidades,
      'movimientos': movimientos,
   }

   return render(request, 'empleado-detalles.html', context)


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


def editar_movimiento(request, empleado_id, movimiento_id):
   context = {}
   return render(request, 'movimiento-editar.html', context)
