from django.db import models

# Create your models here.
class EntityField(models.SmallIntegerField):
    ARL = 0
    EMPRESA = 1
    EPS = 2

    CHOICES = (
        (ARL, 'Arl'),
        (EMPRESA, 'Empresa'),
        (EPS, 'Eps'),
    )

    def __init__(self, *args, **kwargs):
        kwargs['choices'] = self.CHOICES
        super().__init__(*args, **kwargs)


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
        unique=True,
        verbose_name='Codigo AFP',
        help_text='Escribe el codigo de la AFP...',
    )
    nit = models.CharField(
        max_length=32,
        verbose_name='NIT',
        help_text='Escribe el NIT de la AFP..'
    )
    nombre = models.CharField(
        max_length=64,
        verbose_name='Nombre de la entidad',
        help_text='Escribe el nombre de la AFP...'
    )
    creado = models.DateTimeField(auto_now_add=True, editable=False, null=True, blank=True)
    actualizado = models.DateTimeField(auto_now=True, editable=False, null=True, blank=True)

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
    creado = models.DateTimeField(auto_now_add=True, editable=False, null=True, blank=True)
    actualizado = models.DateTimeField(auto_now=True, editable=False, null=True, blank=True)

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
    dias_empresa = models.SmallIntegerField(
        default=0,
        verbose_name='# dias asume empresa',
        help_text='Escribe el numero de dias que va a pagar la empresa',
    )
    creado = models.DateTimeField(auto_now_add=True, editable=False, null=True, blank=True)
    actualizado = models.DateTimeField(auto_now=True, editable=False, null=True, blank=True)

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
    responsable = EntityField(
        default=1,
        help_text='0: ARL, 1: Empresa y 2: EPS',
        db_comment='Campo para almacenar el responsable del pago de la incapacidad, si el responsable es la empresa cubrira los dos primeros dias, para el resto de los casos lo cubre la entidad.'
    )
    creado = models.DateTimeField(auto_now_add=True, editable=False, null=True, blank=True)
    actualizado = models.DateTimeField(auto_now=True, editable=False, null=True, blank=True)

    class Meta:
        db_table = 'conceptos'

    def __str__(self):
        return self.nombre


class Diagnostico(models.Model):
    codigo = models.CharField(
        max_length=16,
        unique=True,
        verbose_name='Codigo del diagnostico',
        help_text='Escribe el codigo del diagnostico...'
    )
    nombre = models.CharField(
        max_length=64,
        help_text='Escribe el nombre del diagnostico...'
    )
    creado = models.DateTimeField(auto_now_add=True, editable=False, null=True, blank=True)
    actualizado = models.DateTimeField(auto_now=True, editable=False, null=True, blank=True)

    class Meta:
        db_table: 'diagnosticos'

    def __str__(self):
        return self.nombre


class Eps(models.Model):
    codigo = models.CharField(
        max_length=32,
        unique=True,
        verbose_name='Codigo de la EPS',
        help_text='Escribe el codigo de la EPS...',
    )
    nit = models.CharField(
        max_length=32,
        help_text='Escribe el NIT de la EPS...',
    )
    nombre = models.CharField(
        max_length=64,
        help_text='Escribe el nombre de la EPS...',
    )
    creado = models.DateTimeField(auto_now_add=True, editable=False, null=True, blank=True)
    actualizado = models.DateTimeField(auto_now=True, editable=False, null=True, blank=True)

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
    creado = models.DateTimeField(auto_now_add=True, editable=False, null=True, blank=True)
    actualizado = models.DateTimeField(auto_now=True, editable=False, null=True, blank=True)

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

    def __str__(self):
        return self.nombre


class EstadoIncapacidad(models.Model):
    codigo = models.CharField(
        max_length=3,
        verbose_name='Codigo estado de incapacidad',
        help_text='Escribe el codigo del estado de incapacidad...',
        null=True,
        blank=True,
    )
    nombre = models.CharField(
        max_length=64,
        help_text='Escribe el estado de la incapacidad...',
    )
    creado = models.DateTimeField(auto_now_add=True, editable=False, null=True, blank=True)
    actualizado = models.DateTimeField(auto_now=True, editable=False, null=True, blank=True)

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
    calendario = models.CharField(max_length=32, null=True, blank=True)
    salario = models.DecimalField(decimal_places=2, max_digits=10, default=0)
    total_dias = models.IntegerField(default=0, null=True, blank=True)
    empresa_dias = models.IntegerField(default=0, null=True, blank=True)
    empresa_valor = models.DecimalField(
        decimal_places=2,
        max_digits=10,
        default=0,
        null=True,
        blank=True
    )
    entidad_dias = models.IntegerField(default=0, null=True, blank=True)
    entidad_valor = models.DecimalField(
        decimal_places=2,
        max_digits=10,
        default=0,
        null=True,
        blank=True
    )

    creado = models.DateTimeField(auto_now_add=True, editable=False, null=True, blank=True)
    actualizado = models.DateTimeField(auto_now=True, editable=False, null=True, blank=True)

    movimiento = models.ForeignKey(
        'Movimiento',
        related_name='fechas_distribucion',
        on_delete=models.CASCADE
    ) 

    class Meta:
        verbose_name = 'Fechas de Distribucion'
        verbose_name_plural = 'Fechas de Distribucion'
        db_table = 'fechas_distribucion'


class Movimiento(models.Model):
    cod_incapacidad = models.CharField(
        max_length=32,
        verbose_name='Codigo de la incapacidad',
        help_text='Escribe el codigo de la incapacidad',
        null=True,
        blank=True,
    )
    serie = models.CharField(
        max_length=32,
        unique=True,
        help_text='Escribe el numero de serie',
    )
    fecha_recepcion = models.DateField(auto_now_add=True)
    fecha_inicio = models.DateField(null=True, blank=True)
    fecha_fin = models.DateField(null=True, blank=True)
    prorroga = models.BooleanField(default=False)
    dias = models.SmallIntegerField(default=0)
    valor_cia = models.DecimalField(decimal_places=2, max_digits=10)
    cuenta_cobrar = models.DecimalField(decimal_places=2, max_digits=10)
    pagado_entidad = models.DecimalField(decimal_places=2, max_digits=10, null=True, blank=True)
    pendiente_entidad = models.DecimalField(
        decimal_places=2,
        max_digits=10,
        null=True,
        blank=True,
    )
    llevada_gasto = models.DecimalField(decimal_places=2, max_digits=10, null=True, blank=True)
    mayor_valor = models.DecimalField(decimal_places=2, max_digits=10, null=True, blank=True)
    cpto_472 = models.DecimalField(decimal_places=2, max_digits=10, null=True, blank=True)
    fecha_pago = models.DateField(null=True, blank=True)
    fecha_estado = models.DateField(null=True, blank=True)
    genera_pago = models.BooleanField(default=False)
    observaciones = models.TextField(max_length=500, null=True, blank=True)

    creado = models.DateTimeField(auto_now_add=True, editable=False, null=True, blank=True)
    actualizado = models.DateTimeField(auto_now=True, editable=False, null=True, blank=True)

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
        db_column='clase_inc_id',
        on_delete=models.PROTECT,
    )
    estado_incapacidad = models.ForeignKey(
        'EstadoIncapacidad',
        db_column='estado_inc_id',
        on_delete=models.PROTECT,
        default=0,
        verbose_name='Estado de incapacidad',
    )


    class Meta:
        db_table = 'movimientos'

