from datetime import datetime
import json
import pandas as pd
from django.contrib import messages
from django.shortcuts import redirect, render, get_object_or_404
from .models import Afp, CentroCosto, ClaseIncapacidad, Concepto, Diagnostico, Empleado, Eps, EstadoIncapacidad, FechaDistribucion, Movimiento

ARL_NIT = '890903790'
ARL_NOMBRE = 'Compania Suramericana de Riesgos Profesionales'

MAPPER = {
   'eps_codigo': 'EPS',
   'afp_codigo': 'AFP',
}

EMPLEADO_MAPPER = {
   'nombre': 'Nombre',
   'docto_empleado': 'Documento',
   'genero': 'Genero',
   'fecha_nacimiento': 'Fecha_Nacimiento',
   'fecha_ingreso': 'Fecha_Ingreso',
   'arl_nit': 'ARL',
   'arl_nombre': 'Nombre_ARL',
   'estado': 'Estado',
}

MOVIMIENTO_MAPPER = {
   'Serie incapacidad': 'serie',
   'FECHA RECEPCION': 'fecha_ingreso',
   'Ccosto': 'costos_id',
   'Clase_incapacidad': 'clase_incapacidad_nombre',
   'No.incapacidad': 'cod_incapacidad',
   'EstadoIncapacidad': 'estado_incapacidad_id',
   'Concepto': 'concepto_id',
   'Código diagnóstico': 'diagnostico_codigo',
   'Notas': 'observaciones',
   'FECHA INICIO REAL TNL': 'fecha_inicio',
   'FECHA FINAL REAL TNL': 'fecha_fin',
   'Dias Amortiz': 'dias',
   'Es prorroga': 'prorroga',
   'Valor IBC': 'salario',
}

FECHAS_DIST_MAPPER = {
   'Valor Cia. 3 Dias': 'empresa_dias',
   'Valor TNL': 'entidad_dias',
   'Fecha Inicial': 'fecha_inicial',
   'Fecha Final': 'fecha_final',
}

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
      fechas_distribucion = request.POST.get('fechas_distribucion')
      fechas_distribucion = json.loads(fechas_distribucion)
      afp_id = request.POST.get('afp')
      arl_nit = request.POST.get('arl_nit')
      arl_nombre = request.POST.get('arl_nombre')
      clase_incapacidad_id = request.POST.get('clase_incapacidad_id')
      cod_incapacidad = request.POST.get('cod_incapacidad')
      cpto_472 = request.POST.get('cpto_472')
      concepto_id = request.POST.get('concepto_id')
      cuenta_cobrar = request.POST.get('cuenta_cobrar')
      diagnostico_id = request.POST.get('diagnostico_id')
      dias = request.POST.get('dias')
      docto_empleado = request.POST.get('docto_empleado')
      eps_id = request.POST.get('eps')
      estado = request.POST.get('estado')
      estado_incapacidad_id = request.POST.get('estado_incapacidad_id')
      genera_pago = True if request.POST.get('genera_pago') else False
      fecha_ingreso = request.POST.get('fecha_ingreso')
      fecha_inicio = request.POST.get('fecha_inicio')
      fecha_fin = request.POST.get('fecha_fin')
      fecha_nacimiento = request.POST.get('fecha_nacimiento')
      fecha_recepcion = request.POST.get('fecha_recepcion')
      genero = request.POST.get('genero')
      movimiento_centro_costos_id = request.POST.get('movimiento_centro_costos_id')
      nombre = request.POST.get('nombre')
      prorroga = True if request.POST.get('prorroga') else False
      observaciones = request.POST.get('observaciones')
      serie = request.POST.get('serie')
      valor_cia = request.POST.get('valor_cia')

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
            cpto_472=cpto_472,
            serie=serie,
            fecha_recepcion=fecha_recepcion,
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin,
            prorroga=prorroga,
            dias=dias,
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

         for distribucion in fechas_distribucion:
            fecha_distribucion = FechaDistribucion(
               fecha_inicial=distribucion['fechaInicio'],
               fecha_final=distribucion['fechaFin'],
               salario=distribucion['salario'],
               total_dias=distribucion['totalDias'],
               empresa_dias=distribucion['empresaDias'],
               empresa_valor=distribucion['empresaValor'],
               entidad_dias=distribucion['entidadDias'],
               entidad_valor=distribucion['entidadValor'],
               movimiento=movimiento, 
            )
            fecha_distribucion.save()

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


def cargar_pagos(request):
   return render(request, 'cargar-pagos.html')


def cargar_incapacidades(request):
   msg = ''
   if request.method == 'POST':
      file = request.FILES['file']
      try:
         df = pd.read_excel(file)
         docto_empleado_ant = 0
         nuevo_empleado = {}

         for index, row in df.iterrows():
            docto_empleado = row[EMPLEADO_MAPPER['docto_empleado']]

            for db_field, excel_field in EMPLEADO_MAPPER.items():
               value = row[excel_field] 

               if isinstance(value, str):
                  value = value.strip()

               if db_field == 'fecha_nacimiento' or db_field == 'fecha_ingreso':
                  value = value.split(' ')[0]

               nuevo_empleado[db_field] = value

            eps_codigo = row['EPS'].strip()
            afp_codigo = row['AFP'].strip()

            eps = Eps.objects.get(codigo=eps_codigo)
            afp = Afp.objects.get(codigo=afp_codigo)

            nuevo_empleado['eps'] = eps
            nuevo_empleado['afp'] = afp

            if nuevo_empleado['docto_empleado'] != docto_empleado_ant:
               try:
                  # Verificar si el empleado existe
                  empleado, created = Empleado.objects.get_or_create(
                     docto_empleado=docto_empleado,
                     defaults=nuevo_empleado,
                  )

               except Empleado.DoesNotExist:
                  msg = f"Empleado con documento {docto_empleado} no existe y no pudo ser creado."
                  messages.error(request, msg)
               except Exception as e:
                  msg = f"Error al procesar la fila {index + 1}: {e}"
                  messages.error(request, msg)

         return redirect('/')

      except Exception as e:
         msg = f"Error al cargar el archivo: {e}"
         messages.error(request, msg)

   return render(request, 'cargar-archivo.html', {'msg': msg})

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


def editar_movimiento(request, movimiento_id):
   afps = Afp.objects.all().order_by('nombre')
   epss = Eps.objects.all().order_by('nombre')
   ccostos = CentroCosto.objects.all().order_by('nombre')
   conceptos = Concepto.objects.all().order_by('codigo')
   diagnosticos = Diagnostico.objects.all().order_by('codigo')
   incapacidades = ClaseIncapacidad.objects.all().order_by('nombre')
   estados_incapacidades = EstadoIncapacidad.objects.all().order_by('nombre')

   if request.method == 'POST':
      movimiento = get_object_or_404(Movimiento, id=movimiento_id)

      afp_id = request.POST.get('afp_id')
      eps_id = request.POST.get('eps_id')
      docto_empleado = request.POST.get('docto_empleado')
      docto_empleado_ant = request.POST.get('docto_empleado_ant')
      docto_cambiado = docto_empleado != docto_empleado_ant
      serie = request.POST.get('serie')
      serie_ant = request.POST.get('serie_ant')
      serie_cambiada = serie != serie_ant
      movimiento_centro_costos_id = request.POST.get('movimiento_centro_costos_id')
      concepto_id = request.POST.get('concepto_id')
      diagnostico_id = request.POST.get('diagnostico_id')
      clase_incapacidad_id = request.POST.get('clase_incapacidad_id')
      estado_incapacidad_id = request.POST.get('estado_incapacidad_id')
      fechas_distribucion = request.POST.get('fechas_distribucion')
      fechas_distribucion = json.loads(fechas_distribucion)

      registros_duplicados = False
      existe_empleado = False
      existe_movimiento = False

      if docto_cambiado: 
         existe_empleado = Empleado.objects.filter(docto_empleado=docto_empleado).exists()

      if serie_cambiada:
         existe_movimiento = Movimiento.objects.filter(serie=serie).exists()

      error_empleado = 'Número de documento duplicado' if existe_empleado else None
      error_movimiento = 'Número de serie duplicado' if existe_movimiento else None
      registros_duplicados = existe_empleado or existe_movimiento

      if registros_duplicados:
         return render(request, 'movimiento-editar.html', {
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
         prorroga = True if request.POST.get('prorroga') else False
         genera_pago = True if request.POST.get('genera_pago') else False

         # Actualizar datos del movimiento
         movimiento.calendario = request.POST.get('calendario')
         movimiento.centro_costo = centro_costo
         movimiento.cod_incapacidad = request.POST.get('cod_incapacidad')
         movimiento.cuenta_cobrar = request.POST.get('cuenta_cobrar')
         movimiento.concepto = concepto
         movimiento.clase_incapacidad = clase_incapacidad
         movimiento.cpto_472 = request.POST.get('cpto_472')
         movimiento.diagnostico = diagnostico
         movimiento.estado_incapacidad = estado_incapacidad
         movimiento.fecha_recepcion = request.POST.get('fecha_recepcion')
         movimiento.fecha_pago = request.POST.get('fecha_pago')
         movimiento.genera_pago = genera_pago
         movimiento.llevada_gasto = request.POST.get('llevada_gasto')
         movimiento.mayor_valor = request.POST.get('mayor_valor')
         movimiento.observaciones = request.POST.get('observaciones')
         movimiento.pagado_entidad = request.POST.get('pagado_entidad')
         movimiento.pendiente_entidad = request.POST.get('pendiente_entidad')
         movimiento.prorroga = prorroga
         movimiento.serie = request.POST.get('serie')
         movimiento.valor_cia = request.POST.get('valor_cia')
         
         movimiento.save()

         for distribucion in fechas_distribucion:
            fecha = get_object_or_404(FechaDistribucion, id=distribucion['id'])
            fecha.calendario = distribucion['calendario']
            fecha.empresa_dias = distribucion['empresaDias']
            fecha.empresa_valor = distribucion['empresaValor']
            fecha.entidad_dias = distribucion['entidadDias']
            fecha.entidad_valor = distribucion['entidadValor']
            fecha.fecha_inicial = distribucion['fechaInicio']
            fecha.fecha_final = distribucion['fechaFin']
            fecha.movimiento = movimiento
            fecha.salario = distribucion['salario']
            fecha.total_dias = distribucion['totalDias']

            fecha.save()

         empleado = movimiento.empleado

         empleado.afp = afp
         empleado.docto_empleado = request.POST.get('docto_empleado')
         empleado.estado = request.POST.get('estado')
         empleado.eps = eps
         empleado.fecha_ingreso = request.POST.get('fecha_ingreso')
         empleado.fecha_nacimiento = request.POST.get('fecha_nacimiento')
         empleado.genero = request.POST.get('genero')
         empleado.nombre = request.POST.get('nombre')
         empleado.arl_nit = request.POST.get('arl_nit')
         empleado.arl_nombre = request.POST.get('arl_nombre')

         empleado.save()

      return redirect('/')

   movimiento = get_object_or_404(
      Movimiento.objects.select_related('empleado').prefetch_related('fechas_distribucion'),
      id=movimiento_id
   )

   context = {
      'afps': afps,
      'epss': epss,
      'ccostos': ccostos,
      'conceptos': conceptos,
      'diagnosticos': diagnosticos,
      'incapacidades': incapacidades,
      'estados_incapacidades': estados_incapacidades,
      'movimiento': movimiento,
   }

   return render(request, 'movimiento-editar.html', context)

