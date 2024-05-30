from datetime import datetime
import json
import logging
import pandas as pd
import re
from django.contrib import messages
from django.shortcuts import redirect, render, get_object_or_404
from .models import Afp, CentroCosto, ClaseIncapacidad, Concepto, Diagnostico, Empleado, Eps, EstadoIncapacidad, FechaDistribucion, Movimiento, GenderField, StatusField
from .utils import generate_series_with_date

logger = logging.getLogger(__name__)

# Set the option to opt-in to the future behavior
pd.set_option('future.no_silent_downcasting', True)

ARL_NIT = '890903790'
ARL_NOMBRE = 'Compania Suramericana de Riesgos Profesionales'

MAPPER = {
   'afp_codigo': 'afp',
   'centro_costos_codigo': 'ccostos',
   'clase_incapacidad_nombre': 'incapacidad_nombre',
   'concepto_codigo': 'concepto',
   'diagnostico_codigo': 'diagnostico_codigo',
   'eps_codigo': 'eps',
   'estado_incapacidad_codigo': 'estado_incapacidad',
   'salario': 'salario',
}

EMPLEADO_MAPPER = {
   'docto_empleado': 'documento',
   'genero': 'genero',
   'fecha_nacimiento': 'fecha_nacimiento',
   'fecha_ingreso': 'fecha_ingreso',
   'nombre': 'nombre',
   'arl_nit': 'arl',
   'arl_nombre': 'nombre_arl',
   'estado': 'estado',
}

MOVIMIENTO_MAPPER = {
   'cod_incapacidad': 'cod_incapacidad',
   'dias': 'm_dias',
   'fecha_inicio': 'm_fecha_inicio',
   'fecha_fin': 'm_fecha_fin',
   'fecha_recepcion': 'fecha_recepcion',
   'genera_pago': 'genera_pago',
   'observaciones': 'observaciones',
   'prorroga': 'prorroga',
   'serie': 'serie',
   'valor_cia': 'm_valor_cia',
   'cuenta_cobrar': 'm_cuenta_cobrar',
}

FECHAS_DIST_MAPPER = {
   'fecha_inicial': 'fd_fecha_inicial',
   'fecha_final': 'fd_fecha_final',
   'calendario': 'calendario',
   'empresa_dias': 'empresa_dias',
   'empresa_valor': 'empresa_valor',
   'entidad_dias': 'entidad_dias',
   'entidad_valor': 'entidad_valor',
   'salario': 'salario',
   'total_dias': 'fd_total_dias',
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
      errors = []
      try:
         df = pd.read_excel(file)
         docto_empleado_ant = 0
         nuevo_empleado = {}
         nuevo_movimiento = {}

         df = df.fillna({
            MAPPER['estado_incapacidad_codigo']: 1,
            MAPPER['diagnostico_codigo']: 9999,
            MOVIMIENTO_MAPPER['serie']: -1,
            MOVIMIENTO_MAPPER['dias']: 0,
            MOVIMIENTO_MAPPER['cod_incapacidad']: -1,
            MOVIMIENTO_MAPPER['genera_pago']: False,
            MOVIMIENTO_MAPPER['observaciones']: '',
            FECHAS_DIST_MAPPER['empresa_dias']: 0,
            FECHAS_DIST_MAPPER['empresa_valor']: 0,
            FECHAS_DIST_MAPPER['entidad_dias']: 0,
            FECHAS_DIST_MAPPER['entidad_valor']: 0,
         })

         # Inferring objects to avoid future warning
         df = df.infer_objects(copy=False)

         for index, row in df.iterrows():
            docto_empleado = str(row[EMPLEADO_MAPPER['docto_empleado']]).strip()

            for db_field, excel_field in EMPLEADO_MAPPER.items():
               value = row[excel_field] 

               if isinstance(value, str):
                  value = value.strip()

               if db_field == 'nombre':
                  value = value.title()
                  value = re.sub(r'\s+', ' ', value)

               if db_field == 'fecha_nacimiento' or db_field == 'fecha_ingreso':
                  value = pd.to_datetime(value.split(' ')[0]).date()

               if db_field == 'arl_nit':
                  value = str(value)

               nuevo_empleado[db_field] = value

            for db_field, excel_field in MOVIMIENTO_MAPPER.items():
               value = row[excel_field]

               if isinstance(value, str):
                  value = value.strip()

               if db_field == 'dias':
                  value = int(value)

               if db_field == 'prorroga':
                  value = True if value == 'Si' else False

               if db_field == 'serie':
                  value = str(int(value))

               if db_field == 'fecha_inicio' or \
                  db_field == 'fecha_fin' or \
                  db_field == 'fecha_recepcion':
                  value = pd.to_datetime(value).date() if pd.notna(value) else None

               if db_field == 'observaciones':
                  value = value.lower() if pd.notna(value) else None

               nuevo_movimiento[db_field] = value

            afp_codigo = str(row[MAPPER['afp_codigo']]).strip()
            clase_incapacidad_nombre = str(row[MAPPER['clase_incapacidad_nombre']]).strip()
            centro_costos_codigo = str(row[MAPPER['centro_costos_codigo']]).zfill(6)
            concepto_codigo = str(row[MAPPER['concepto_codigo']]).zfill(3)
            eps_codigo = row[MAPPER['eps_codigo']].strip()
            diagnostico_codigo = row[MAPPER['diagnostico_codigo']]
            estado_incapacidad_codigo = int(row[MAPPER['estado_incapacidad_codigo']])

            afp = Afp.objects.get(codigo=afp_codigo)
            clase_incapacidad = ClaseIncapacidad.objects.get(nombre=clase_incapacidad_nombre)
            centro_costo = CentroCosto.objects.get(codigo=centro_costos_codigo)
            concepto = Concepto.objects.get(codigo=concepto_codigo)
            diagnostico = Diagnostico.objects.get(codigo=diagnostico_codigo)
            estado_incapacidad = EstadoIncapacidad.objects.get(codigo=estado_incapacidad_codigo)
            eps = Eps.objects.get(codigo=eps_codigo)

            nuevo_empleado['afp'] = afp
            nuevo_empleado['eps'] = eps

            nuevo_movimiento['afp'] = afp
            nuevo_movimiento['eps'] = eps
            nuevo_movimiento['concepto'] = concepto
            nuevo_movimiento['diagnostico'] = diagnostico
            nuevo_movimiento['incapacidad'] = clase_incapacidad
            nuevo_movimiento['estado_incapacidad'] = estado_incapacidad
            nuevo_movimiento['centro_costo'] = centro_costo

            if nuevo_empleado['docto_empleado'] != docto_empleado_ant:
               try:
                  # Verificar si el empleado existe
                  docto_empleado = nuevo_empleado['docto_empleado']
                  nuevo_empleado['genero'] = GenderField.MALE if nuevo_empleado['genero'] == 0 else GenderField.FEMALE
                  nuevo_empleado['estado'] = StatusField.ACTIVE if nuevo_empleado['estado'] == 0 else StatusField.INACTIVE
                  del nuevo_empleado['docto_empleado']

                  empleado, created = Empleado.objects.get_or_create(
                     docto_empleado=docto_empleado,
                     defaults=nuevo_empleado
                  )

                  serie = int(nuevo_movimiento['serie'])
                  serie = serie if serie > 0 else generate_series_with_date()

                  del nuevo_movimiento['serie']

                  nuevo_movimiento['empleado'] = empleado

                  movimiento, created = Movimiento.objects.get_or_create(
                     serie=serie,
                     defaults=nuevo_movimiento,
                  )

                  nueva_fecha_distribucion = {
                     'movimiento': movimiento,
                     'salario': row[FECHAS_DIST_MAPPER['salario']],
                     'total_dias': int(row[FECHAS_DIST_MAPPER['total_dias']]),
                     'fecha_inicial': row[FECHAS_DIST_MAPPER['fecha_inicial']],
                     'fecha_final': row[FECHAS_DIST_MAPPER['fecha_final']],
                     'empresa_dias': row[FECHAS_DIST_MAPPER['empresa_dias']],
                     'empresa_valor': row[FECHAS_DIST_MAPPER['empresa_valor']],
                     'entidad_dias': row[FECHAS_DIST_MAPPER['entidad_dias']],
                     'entidad_valor': row[FECHAS_DIST_MAPPER['entidad_valor']],
                  }

                  fecha_distribucion = FechaDistribucion.objects.create(**nueva_fecha_distribucion) 

               except Empleado.DoesNotExist:
                  msg = f"Empleado con documento {docto_empleado} no existe y no pudo ser creado."
                  messages.error(request, msg)
               except Movimiento.DoesNotExist:
                  msg = f"Movimiento con la serie {docto_empleado} no existe y no pudo ser creado."
                  messages.error(request, msg)
               except Exception as e:
                  error_msg = f"Error al procesar la fila {index + 1}: {str(e)}"
                  logger.error(error_msg)
                  errors.append(error_msg)
                  # messages.error(request, msg)
            # 
            # messages.success(request, "Datos cargados exitosamente.")

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
