# Esquema Base de Datos

Este esquema es generado con [dbdiagram.io](https://dbdiagram.io/d) solo es copiar y pegar el codigo [Aqui](https://dbdiagram.io/d)

```sql
Table afp {
  id integer [primary key]
  nit varchar(32)
  nombre varchar(64)
  creado date
  actualizado date
}

Table ccosto {
  id integer [primary key]
  codigo varchar(16)
  nombre varchar(64)
  creado datetime
  actualizado datetime
}

Table clase_incapacidad {
  id integer [primary key]
  nombre varchar(64)
  dias_empresa smallint
  creado datetime
  actualizado datetime
}

Table conceptos {
  id integer [primary key]
  nombre varchar(64)
  responsable smallint [note: '0: ARL, 1: Empresa y 2: EPS']
  creado datetime
  actualizado datetime
}

Table diagnosticos {
  id integer [primary key]
  codigo varchar(16)
  nombre varchar(64)
  creado datetime
  actualizado datetime
}

Table eps {
  id integer [primary key]
  nit varchar(32)
  nombre varchar(64)
  creado datetime
  actualizado datetime
}

Table empleados {
  id integer [primary key]
  docto_empleado varchar(32)
  nombre_empleado varchar(128)
  genero smallint [note: '1: Femenino, 0: Masculino']
  fecha_nacimiento date [note: 'fecha de nacimiento del empleado']
  fecha_ingreso date 
  estado smallint [note: '0= activo, 1=Retirado']
  nit_arl varchar(32) [note: 'Nit ARL del empleado']
  nombre_arl varchar(64) 
  creado datetime
  actualizado datetime

  eps_id varchar(32) [note: 'EPS del empleado']
  afp_id varchar(32) [note: 'Fondo de pensión del empleado']
}

Table estado_incapacidad {
  id integer [primary key]
  nombre varchar(40)
  creado datetime
  actualizado datetime
}

Table fechas_distribucion {
  id integer [primary key]
  movimiento_id integer
  fecha_i_real date
  fecha_f_real date
  cuenta_cobrar double(10, 2)
}

Table empleados_ccostos { 
  id integer [primary key]
  docto_empleado varchar(32) 
  id_ccosto char(15)
  creado datetime
  actualizado datetime
}

Table movimiento { 
  id integer [primary key]
  cod_incapacidad varchar(32)
  docto_empleado varchar(32)
  ccosto_id integer
  serie varchar(20)
  fecha_recepcion date
  eps_id integer
  afp_id integer
  clase_incapacidad_id integer
  fecha_inicio date
  fecha_fin date
  concepto_id varchar(20)
  diagnostico_id varchar(20)
  prorroga boolean
  dias smallint
  salario double(10, 2)
  calendario varchar(32)
  fecha_pago double(10, 2)
  pagado_entidad double(10, 2)
  pendiente_entidad double(10, 2)
  llevada_gasto double(10, 2)
  mayor_valor double(10, 2)
  cpto_472 double(10, 2)
  estado_id integer
  fecha_estado date
  genera_pago boolean
}

Ref: empleados.afp_id > afp.id

Ref: empleados.eps_id > eps.id

Ref: empleados_ccostos.id > ccosto.id

Ref: movimiento.id > empleados.id

Ref: movimiento.ccosto_id > ccosto.id

Ref: movimiento.eps_id > eps.id

Ref: movimiento.afp_id > afp.id

Ref: movimiento.clase_incapacidad_id > clase_incapacidad.id

Ref: movimiento.concepto_id > conceptos.id

Ref: movimiento.diagnostico_id > diagnosticos.id

Ref: movimiento.clase_incapacidad_id > estado_incapacidad.id

REf: movimiento.id < fechas_distribucion.movimiento_id
```
