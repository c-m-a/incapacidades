from django.db import models

# Create your models here.
class GenderField(models.SmallIntegerField):
    FEMALE = 1
    MALE = 0

    CHOICES = (
        (FEMALE, 'Femenino'),
        (MALE, 'Masculino'),
    )

    def __init__(self, *args, **kwargs):
        kwargs['choices'] = self.CHOICES
        super().__init__(*args, **kwargs)


class StatusField(models.SmallIntegerField):
    ACTIVE = 0
    INACTIVE = 1

    CHOICES = (
        (ACTIVE, 'Activo'),
        (INACTIVE, 'Retirado'),
    )

    def __init__(self, *args, **kwargs):
        kwargs['choices'] = self.CHOICES
        super().__init__(*args, **kwargs)


class Afp(models.Model):
    nit = models.CharField(max_length=32, unique=True)
    nombre = models.CharField(max_length=64)
    creado = models.DateTimeField(auto_now_add=True, editable=False)


class CentroCosto(models.Model):
    nombre = models.CharField(max_length=64, unique=True)

    class Meta:
        db_table = 'ccostos'


class ClaseIncapacidad(models.Model):
    nombre = models.CharField(max_length=64)
    creado = models.DateTimeField(auto_now_add=True, editable=False)

    class Meta:
        db_table = 'clases_incapacidades'


class Concepto(models.Model):
    nombre = models.CharField(max_length=64)
    creado = models.DateTimeField(auto_now_add=True, editable=False)

    class Meta:
        db_table = 'conceptos'


class Diagnostico(models.Model):
    nombre = models.CharField(max_length=64)
    creado = models.DateTimeField(auto_now_add=True, editable=False)

    class Meta:
        db_table: 'diagnosticos'


class Eps(models.Model):
    nit = models.CharField(max_length=32, unique=True)
    nombre = models.CharField(max_length=64)
    creado = models.DateTimeField(auto_now_add=True, editable=False)


class Empleado(models.Model):
    docto_empleado = models.CharField(
        max_length=64,
        unique=True,
    )
    nombre = models.CharField(max_length=128)
    genero = GenderField(
        help_text='1: Femenino, 0: Masculino',
        db_comment='Campo para el genero de la persona. 1: Femenino, 0: Masculino'
    )
    fecha_nacimiento = models.DateTimeField()
    fecha_ingreso = models.DateTimeField()
    estado = StatusField()
    arl_nit = models.CharField(max_length=32)
    arl_nombre = models.CharField(max_length=64)
    creado = models.DateTimeField(auto_now_add=True, editable=False)
    actualizado = models.DateTimeField(auto_now=True, editable=False)

    eps = models.ForeignKey(
        'Eps',
        db_column='eps_id',
        on_delete=models.PROTECT,
    )
    afp = models.ForeignKey(
        'Afp',
        db_column='afp_id',
        on_delete=models.PROTECT,
    )

    centro_costos = models.ManyToManyField(
        'CentroCosto',
        related_name='ccostos_asignados',
    )


class EstadoIncapacidad(models.Model):
    nombre = models.CharField(max_length=64)
    creado = models.DateTimeField(auto_now_add=True, editable=False)


class FechaDistribucion(models.Model):
    fecha_inicial_real = models.DateTimeField()
    fecha_final_real = models.DateTimeField()
    cuenta_cobrar = models.DecimalField(decimal_places=2, max_digits=8)
    creado = models.DateTimeField(auto_now_add=True, editable=False)
    actualizado = models.DateTimeField(auto_now=True, editable=False)

    movimiento = models.ForeignKey('Movimiento', on_delete=models.CASCADE) 

    class Meta:
        db_table = 'fechas_distribucion'


class Movimiento(models.Model):
    cod_incapacidad = models.CharField(max_length=32, unique=True)
    serie = models.CharField(max_length=32, unique=True)
    fecha_recepcion = models.DateTimeField()
    fecha_inicio = models.DateTimeField()
    fecha_fin = models.DateTimeField()
    prorroga = models.SmallIntegerField()
    dias = models.SmallIntegerField()
    salario = models.DecimalField(decimal_places=2, max_digits=8)
    calendario = models.CharField(max_length=32)
    valor_cia = models.DecimalField(decimal_places=2, max_digits=8)
    cuenta_cobrar = models.DecimalField(decimal_places=2, max_digits=8)
    pagado_entidad = models.DecimalField(decimal_places=2, max_digits=8)
    llevada_gasto = models.DecimalField(decimal_places=2, max_digits=8)
    mayor_valor = models.DecimalField(decimal_places=2, max_digits=8)
    cpto_472 = models.DecimalField(decimal_places=2, max_digits=8)
    fecha_pago = models.DecimalField(decimal_places=2, max_digits=8)
    fecha_estado = models.DecimalField(decimal_places=2, max_digits=8)
    genera_pago = models.IntegerField()

    empleado = models.ForeignKey(
        'Empleado',
        db_column='empleado_id',
        on_delete=models.PROTECT,
    ) 
    eps = models.ForeignKey(
        'Eps',
        db_column='eps_id',
        on_delete=models.PROTECT,
    ) 
    afp = models.ForeignKey(
        'Afp',
        db_column='afp_id',
        on_delete=models.PROTECT,
    ) 
    diagnostico = models.ForeignKey(
        'Diagnostico',
        db_column='diagnostico_id',
        on_delete=models.PROTECT,
    ) 
    centro_costo = models.ForeignKey(
        'CentroCosto',
        db_column='ccosto_id',
        on_delete=models.PROTECT,
    )
    concepto = models.ForeignKey(
        'Concepto',
        db_column='concepto_id',
        on_delete=models.PROTECT
    ) 


    class Meta:
        db_table = 'movimientos'

