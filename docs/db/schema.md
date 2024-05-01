# Esquema Base de Datos

Este esquema es generado con [dbdiagram.io](https://dbdiagram.io/d) solo es copiar y pegar el codigo [Aqui](https://dbdiagram.io/d)

```sql
Table empleados {
  docto_empleado varchar(25) [primary key]
  nombre_empleado varchar(100)
  genero smallint [note: '1: Femenino, 0: Masculino']
  fecha_nacimiento date [note: 'fecha de nacimiento del empleado']
  fecha_ingreso date 
  estado smallint [note: '0= activo, 1=Retirado']
  id_eps varchar(20) [note: 'EPS del empleado']
  id_afp varchar(20) [note: 'Fondo de pensión del empleado']
  nit_arl varchar(20) [note: 'Nit ARL del empleado']
  nombre_arl varchar(60) 
}

Table empleados_ccostos { 
  id integer [primary key]
  docto_empleado varchar(25) 
  id_ccosto char(15)
}

Table eps {
  id_eps varchar(20) [primary key]
  nit_eps varchar(20)
  nombre_eps varchar(60)
}

Table afp {
  id_afp varchar(20) [primary key]
  nit_afp varchar(20)
  nombre_afp varchar(60)
}

Table diagnosticos {
  id_diagnostico varchar(20) [primary key]
  diagnostico varchar(60)
}

Table conceptos {
  id_concepto varchar(20) [primary key]
  concepto varchar(60)
}

Table ccosto {
  id_ccosto char(15) [primary key]
  ccosto varchar(40)
}

Table clase_incapacidad {
  id_clase_inc integer [primary key]
  clase_incapacidad varchar(40)
}

Table estado_incapacidad {
  id_estado integer [primary key]
  estado varchar(40)
}

Table movimiento { 
  id_mvto integer [primary key]
  cod_incapacidad varchar(20)
  docto_empleado varchar(25)
  id_ccosto char(15)
  serie varchar(20)
  fecha_recepcion date
  id_eps varchar(20)
  id_afp varchar(20)
  id_clase_inc integer
  fecha_inicio date
  fecha_fin date
  id_concepto varchar(20)
  id_diagnostico varchar(20)
  prorroga integer
  dias integer
  salario money
  calendario varchar(20)
  valor_cia money
  cuenta_cobrar money
  fecha_pago integer
  pagado_entidad money
  pendiente_entidad money
  llevada_gasto money
  mayor_valor money
  cpto_472 money
  id_estado integer
  fecha_estado date
  genera_pago integer

}

Table fechas_distribucion {
  id_distribucion integer [primary key]
  id_mvto integer
  fecha_i_real date
  fecha_f_real date
  cuenta_cobrar money
}

Ref: empleados.id_afp > afp.id_afp

Ref: empleados.id_eps > eps.id_eps

Ref: empleados_ccostos.docto_empleado > empleados.docto_empleado

Ref: empleados_ccostos.id_ccosto > ccosto.id_ccosto

Ref: movimiento.docto_empleado > empleados.docto_empleado

Ref: movimiento.id_ccosto > ccosto.id_ccosto

Ref: movimiento.id_eps > eps.id_eps

Ref: movimiento.id_afp > afp.id_afp

Ref: movimiento.id_clase_inc > clase_incapacidad.id_clase_inc

Ref: movimiento.id_concepto > conceptos.id_concepto

Ref: movimiento.id_diagnostico > diagnosticos.id_diagnostico

Ref: movimiento.id_estado > estado_incapacidad.id_estado

REf: movimiento.id_mvto < fechas_distribucion.id_mvto
```
