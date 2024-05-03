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
    codigo = models.CharField(
        max_length=32,
        verbose_name='Codigo AFP',
        help_text='Escribe el codigo de la AFP...',
    )
    nit = models.CharField(
        max_length=32,
        unique=True,
        verbose_name='NIT',
        help_text='Escribe el NIT de la AFP..'
    )
    nombre = models.CharField(
        max_length=64,
        verbose_name='Nombre de la entidad',
        help_text='Escribe el nombre de la AFP...'
    )
    creado = models.DateTimeField(auto_now_add=True, editable=False)

    class Meta:
        verbose_name = 'AFP'
        verbose_name_plural = 'AFPs'

    def __str__(self):
        return self.nombre


class CentroCosto(models.Model):
    codigo = models.CharField(
        max_length=16,
        null=True,
        verbose_name='Codigo del centro de costos',
        help_text='Escribe el codigo de centro de costos...',
    )
    nombre = models.CharField(
        max_length=64,
        unique=True,
        help_text='Escribe el nombre del centro de costos...',
    )

    class Meta:
        verbose_name = 'Centro de Costo'
        verbose_name_plural = 'Centros de Costos'
        db_table = 'ccostos'

    def __str__(self):
        return self.nombre


class ClaseIncapacidad(models.Model):
    nombre = models.CharField(
        max_length=64,
        verbose_name='Nombre de la incapacidad',
        help_text='Escribe la incapacidad',
    )
    creado = models.DateTimeField(auto_now_add=True, editable=False)

    class Meta:
        verbose_name = 'Clase de Incapacidad'
        verbose_name_plural = 'Clases de Incapacidades'
        db_table = 'clases_incapacidades'

    def __str__(self):
        return self.nombre


class Concepto(models.Model):
    codigo = models.CharField(
        max_length=3,
        verbose_name='Codigo del concepto',
        help_text='Escribe el codigo del concepto...'
    )
    nombre = models.CharField(
        max_length=64,
        help_text='Escribe el nombre del concepto...'
    )
    creado = models.DateTimeField(auto_now_add=True, editable=False)

    class Meta:
        db_table = 'conceptos'

    def __str__(self):
        return self.nombre


class Diagnostico(models.Model):
    codigo = models.CharField(
        max_length=16,
        verbose_name='Codigo del diagnostico',
        help_text='Escribe el codigo del diagnostico...'
    )
    nombre = models.CharField(
        max_length=64,
        help_text='Escribe el nombre del diagnostico...'
    )
    creado = models.DateTimeField(auto_now_add=True, editable=False)

    class Meta:
        db_table: 'diagnosticos'

    def __str__(self):
        return self.nombre


class Eps(models.Model):
    codigo = models.CharField(
        max_length=32,
        verbose_name='Codigo de la EPS',
        help_text='Escribe el codigo de la EPS...',
    )
    nit = models.CharField(
        max_length=32,
        unique=True,
        help_text='Escribe el NIT de la EPS...',
    )
    nombre = models.CharField(
        max_length=64,
        help_text='Escribe el nombre de la EPS...',
    )
    creado = models.DateTimeField(auto_now_add=True, editable=False)

    class Meta:
        verbose_name = 'EPS'
        verbose_name_plural = 'EPSs'

    def __str__(self):
        return self.nombre


class Empleado(models.Model):
    docto_empleado = models.CharField(
        max_length=64,
        unique=True,
        verbose_name='Numero de documento',
        help_text='Escribe el numero de documento...',
    )
    nombre = models.CharField(
        max_length=128,
        verbose_name='Nombres completos',
    )
    genero = GenderField(
        help_text='1: Femenino, 0: Masculino',
        db_comment='Campo para el genero de la persona. 1: Femenino, 0: Masculino'
    )
    fecha_nacimiento = models.DateField(
        verbose_name='Fecha de nacimiento',
        help_text='Escribe o selecciona la fecha de nacimiento...',
    )
    fecha_ingreso = models.DateField(
        verbose_name='Fecha de ingreso',
        help_text='Escribe o selecciona la fecha de ingreso...',
    )
    estado = StatusField()
    arl_nit = models.CharField(
        max_length=32,
        verbose_name='NIT de la ARL',
        help_text='Escribe el NIT de la ARL...',
    )
    arl_nombre = models.CharField(
        max_length=64,
        verbose_name='Nombre de la ARL',
        help_text='Escribe el nombre de la ARL...'
    )
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

    def __str__(self):
        return self.nombre


class EstadoIncapacidad(models.Model):
    nombre = models.CharField(
        max_length=64,
        help_text='Escribe el estado de la incapacidad...',
    )
    creado = models.DateTimeField(auto_now_add=True, editable=False)

    class Meta:
        verbose_name = 'Estado de Incapacidad'
        verbose_name_plural = 'Estados de Incapacidades'

    def __str__(self):
        return self.nombre


class FechaDistribucion(models.Model):
    fecha_inicial = models.DateField(
        verbose_name='Fecha inicial real',
        help_text='Escribe o selecciona la fecha inicial...',
    )
    fecha_final = models.DateField(
        verbose_name='Fecha final real',
        help_text='Escribe o selecciona la fecha final...',
    )
    cuenta_cobrar = models.DecimalField(
        decimal_places=2,
        max_digits=8,
        verbose_name='Cuenta x cobrar',
        help_text='Escribe el valor de la cuenta x cobrar...',
    )
    creado = models.DateTimeField(auto_now_add=True, editable=False)
    actualizado = models.DateTimeField(auto_now=True, editable=False)

    movimiento = models.ForeignKey('Movimiento', on_delete=models.CASCADE) 

    class Meta:
        verbose_name = 'Fechas de Distribucion'
        verbose_name_plural = 'Fechas de Distribucion'
        db_table = 'fechas_distribucion'


class Movimiento(models.Model):
    cod_incapacidad = models.CharField(
        max_length=32,
        unique=True,
        verbose_name='Codigo de la incapacidad',
        help_text='Escribe el codigo de la incapacidad',
    )
    serie = models.CharField(
        max_length=32,
        unique=True,
        help_text='Escribe el numero de serie',
    )
    fecha_recepcion = models.DateTimeField()
    fecha_inicio = models.DateTimeField()
    fecha_fin = models.DateTimeField()
    prorroga = models.SmallIntegerField()
    dias = models.SmallIntegerField()
    salario = models.DecimalField(decimal_places=2, max_digits=10)
    calendario = models.CharField(max_length=32)
    valor_cia = models.DecimalField(decimal_places=2, max_digits=8)
    cuenta_cobrar = models.DecimalField(decimal_places=2, max_digits=8)
    pagado_entidad = models.DecimalField(decimal_places=2, max_digits=8)
    llevada_gasto = models.DecimalField(decimal_places=2, max_digits=8)
    mayor_valor = models.DecimalField(decimal_places=2, max_digits=8)
    cpto_472 = models.DecimalField(decimal_places=2, max_digits=8)
    fecha_pago = models.DateField()
    fecha_estado = models.DateField()
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
        on_delete=models.PROTECT,
    )
    incapacidad = models.ForeignKey(
        'ClaseIncapacidad',
        db_column='incapacidad_id',
        on_delete=models.PROTECT,
    )


    class Meta:
        db_table = 'movimientos'

