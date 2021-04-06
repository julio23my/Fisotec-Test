# Fisotec-Test


## Requisitos
Para realizar la siguiente tarea, el usuario deberá tener en cuenta los siguientes
requisitos:
1. Base de datos PostgreSQL: Debe tener instalada el gestor de base de datos
PostgreSQL, recomendando para ello la versión 10.4.
2. Componente geoespacial Postgis: Integrado con PostgreSQL en la instalación en su
versión 2.4
3. Python 3.7

## Ejercicio
Una vez instalado el gestor de base de datos, se restaurará la base de datos incluida en
el envío, que contiene dos esquemas:
• administracion: mantiene datos del usuario.
• alcaudete_desarrollo_gissmart_energy: contiene los datos del proyecto, que incluyen
varias capas (vial, centro mando, luminaria y módulo de medida).


#### Ejercicio 1

Se creará una función para validar la conexión del usuario, añadiendo a la tabla sesión
la conexión realizada.


#### Ejercicio 2

Se realizará una función que devolverá la información en elemento indicado. Para ello
se indicará la tabla y el id de la misma, devolviendo los datos de dicho elemento.

#### Ejercicio 3

Se realizará un ejercicio que cambiará el campo vial de las capas de centro de mando,
luminaria y módulo de medida.
Para ello, en dicho campo colocará el id del vial (capa base_vial) más cercano a la
geometría del elemento.
Se requiere el uso de las funciones postgis para elaborar la consulta de UPDATE