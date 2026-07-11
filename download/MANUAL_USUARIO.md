# Manual de Usuario — Bitacora NOC

## 1. Introduccion

La **Bitacora NOC** es el sistema de registro operativo del Network Operations Center (NOC). Permite a los operadores de cada turno documentar toda la actividad diaria: pollings de servidores, backups, procesos batch, novedades del turno y el pase de turno.

El sistema funciona completamente en el navegador y sincroniza los datos automaticamente con GitHub, por lo que la informacion queda almacenada en la nube y es accesible desde cualquier dispositivo con conexion a internet.

**URL de acceso:** https://lecatexzonanorte.github.io/nocronograma/bitacora_noc_con_login.html

---

## 2. Inicio de Sesion

Al ingresar a la aplicacion, se muestra una pantalla de login con los campos **Usuario** y **Contrasena**.

### Pasos para iniciar sesion:
1. Escribir el nombre de usuario en mayusculas o minusculas (el sistema lo convierte automaticamente a mayusculas).
2. Escribir la contrasena correspondiente.
3. Hacer clic en **Ingresar** o presionar la tecla **Enter**.
4. Si las credenciales son correctas, se accede al sistema. Si no, se muestra un mensaje de error en rojo.

### Usuarios disponibles:

| Usuario | Contrasena | Rol | Turno |
|---------|-----------|-----|-------|
| OPERAMAÑANA | mañana1 | Operador | Mañana |
| OPERATARDE | tarde1 | Operador | Tarde |
| OPERANOCHE | noche1 | Operador | Noche |
| OPERAADMIN | nocadmin | Administrador | Admin |
| OPERAWU | 0p3r4ci0n35 | Administrador | Admin |
| ADMILOSN | admilosn | Administrador | Admin |
| NOCPRUEBA | pruebanoc | Administrador | Admin (pruebas) |

### Diferencia entre Operador y Administrador:
- **Operador:** Puede cargar datos del dia, agregar novedades y realizar el pase de turno. No puede modificar datos de un dia que ya fue cerrado por otro turno.
- **Administrador:** Tiene acceso total. Puede modificar datos de cualquier dia (incluso cerrados), acceder al dashboard con metricas, descargar reportes y eliminar items individualmente.

---

## 3. Interfaz Principal

Una vez iniciada la sesion, la pantalla principal contiene los siguientes elementos:

### 3.1 Header (barra superior)
- **Titulo:** "Bitacora NOC" con el icono de la aplicacion.
- **Indicador de sincronizacion:** Icono de rueda dentada que gira cuando hay datos sin sincronizar y se detiene cuando todo esta guardado.
- **Boton "Pase de Turno":** Boton amarrillo que cambia segun el turno del usuario (por ejemplo: "Pase de Turno Mañana", "Pase de Turno Tarde", "Pase de Turno Noche"). Los administradores ven "Pase de Turno" sin especificar turno.
- **Boton de notificaciones:** Campana con un numero rojo que indica notificaciones sin leer. Al hacer clic se despliega un panel con las notificaciones.
- **Boton de Dashboard** (solo Admin): Icono de cuadrados que abre el panel de metricas y estadisticas.
- **Barra de usuario:** Muestra el nombre del usuario, el turno (con badge de color) y el boton **Salir**.

### 3.2 Barra de navegacion de fecha
- **Flechas:** Botones para ir al dia anterior o siguiente.
- **Selector de fecha:** Hacer clic en la fecha abre un calendario para saltar a cualquier dia.
- **Boton "Hoy":** Vuelve rapidamente al dia actual.
- **Dia de la semana:** Se muestra a la derecha de la fecha (por ejemplo: "Lunes", "Martes").
- **Selector de tipo de dia:** Desplegable para cambiar entre "Diaria (L-V)", "Fin de Semana" o "BKP Mensual".

### 3.3 Barra de acciones rapidas
- **Buscador:** Permite filtrar servidores, backups o procesos por nombre. Es util cuando hay muchos items.
- **Boton "Copiar dia anterior":** Copia la estructura de pollings, backups y procesos del dia anterior para no tener que cargar todo de cero. Los horarios se limpian para que se completen manualmente.
- **Boton "Exportar CSV":** Descarga todos los datos del dia actual en formato CSV.

### 3.4 Tarjetas de estadisticas
Cuatro tarjetas en la parte superior que muestran un resumen rapido del dia:
- **Servidores:** Cantidad de servidores distintos con pollings cargados.
- **Pollings:** Proporcion de pollings completados (inicio y fin) sobre el total esperado.
- **Backups:** Cantidad total de backups registrados.
- **Procesos:** Proporcion de procesos en estado OK sobre el total.

### 3.5 Pestanas (Tabs)
Tres pestanas para navegar entre las secciones principales:
- **Pollings:** Muestra los servidores agrupados por region/pais.
- **Backups:** Muestra la lista de backups con sus horarios y duracion.
- **Procesos:** Muestra la lista de procesos con su estado.

---

## 4. Registro de Pollings

### Que son los pollings?
Los pollings son verificaciones periodicas que se realizan sobre los servidores de cada pais. Para cada servidor se registra la **hora de inicio** y la **hora de fin** del polling.

### Como cargar un polling:
1. Navegar a la pestana **Pollings**.
2. Hacer clic en el boton **+ Agregar** (solo visible si el dia no esta cerrado).
3. En el modal que se abre, seleccionar el servidor del desplegable. El sistema muestra el pais/region automaticamente.
4. Se pueden agregar los campos de **Inicio** y **Fin** directamente, o hacer clic en "Agregar" y luego editar cada uno.
5. Hacer clic en **Guardar**.

### Servidores disponibles por region:
- **Argentina:** Depu Gran Base, Argentina P$, Argentina P1, Argentina P2
- **Peru:** Peru D1, Peru D2, Peru D3, Peru Aserviban MT, Peru OC, Peru X30
- **Panama:** Panama D1, Panama MT, Panama OC, Panama A. Propias, Panama Mas Me Dan
- **Chile:** Chile MT, Chile OP, Chile Vigo, Chile OC, Chile Cencosud, Chile Los Heroes, Chile CencoPay
- **Mexico:** Mexico - SIE - M1, Mexico - GDE - M2
- **Regional:** (sin asignacion de pais especifica)

### Editar o eliminar un polling:
- Cada servidor tiene iconos de **lapiz** (editar) y **papelera** (eliminar) a la derecha.
- Los administradores pueden editar y eliminar incluso en dias cerrados.
- Si un polling tiene la nota "SIN AC", se muestra en rojo para identificarlo rapidamente.

### Duracion de polling:
Si se cargan hora de inicio y hora de fin, el sistema calcula automaticamente la duracion y la muestra junto al servidor.

---

## 5. Registro de Backups

### Que son los backups?
Los backups son copias de seguridad de los servidores del NOC. Se registra el servidor, el job, las fechas y horas de inicio/fin, y el estado.

### Como cargar un backup:
1. Navegar a la pestana **Backups**.
2. Hacer clic en el boton **+ Agregar**.
3. Completar los campos del formulario:
   - **Servidor:** Seleccionar de la lista (Regional, Pinot, Semillon, Merlot, REGDRS, etc.).
   - **JOB:** Seleccionar el tipo de job (BKPDIARIO, BKPDIARIOU, BKPMIMIX, OP.21).
   - **Fecha inicio / Hora inicio:** Cuando comenzo el backup.
   - **Fecha fin / Hora fin:** Cuando finalizo el backup.
   - **Estado:** Seleccionar entre "OK" o "Error".
   - **Duracion:** Se calcula automaticamente al completar inicio y fin. No es necesario escribirla a mano.
4. Hacer clic en **Guardar**.

### Soporte de backup que cruza medianoche:
El sistema soporta correctamente backups que comienzan un dia y terminan al dia siguiente. Por ejemplo, un backup que empieza el lunes a las 22:00 y termina el martes a las 06:00. Para esto es importante completar tanto la **fecha** como la **hora** en los campos de inicio y fin.

### Editar o eliminar un backup:
- Cada backup tiene iconos de **lapiz** (editar) y **papelera** (eliminar).
- Los administradores pueden editar y eliminar incluso en dias cerrados.

---

## 6. Registro de Procesos

### Que son los procesos?
Los procesos son tareas batch que se ejecutan diariamente en el NOC. Se registran con su estado (OK o Error).

### Procesos fijos predefinidos:
1. Tarjeta Naranja
2. EPE
3. BANCOR
4. Rentas de Cordoba
5. AFIP 72
6. AFIP 24
7. AFIP 48
8. Cierre AFIP
9. Montaje de cintas

### Como cargar el estado de un proceso:
1. Navegar a la pestana **Procesos**.
2. Hacer clic en el boton **+ Agregar**.
3. Seleccionar el proceso del desplegable (o escribir uno personalizado).
4. Seleccionar el estado: **OK** o **Error**.
5. Hacer clic en **Guardar**.

### Procesos personalizados:
Si necesita registrar un proceso que no esta en la lista predefinida, puede escribir el nombre directamente en el campo "Proceso" del formulario.

### Editar o eliminar un proceso:
- Cada proceso tiene iconos de **lapiz** (editar) y **papelera** (eliminar).
- Los administradores pueden editar y eliminar incluso en dias cerrados.

---

## 7. Novedades del Turno (Timeline)

### Que son las novedades?
Las novedades son notas cronologicas que los operadores van registrando durante su turno. Sirven para documentar incidencias, tareas realizadas, observaciones o cualquier evento relevante.

### Como agregar una novedad:
1. En la seccion **"Novedades de Turno"** (debajo de las pestañas), hacer clic en el boton **+ Agregar Novedad**.
2. Escribir el texto de la novedad en el campo que aparece.
3. El sistema registra automaticamente el operador y la hora.
4. Hacer clic en **Guardar**.

### Caracteristicas importantes:
- Las novedades se pueden agregar **incluso en dias cerrados** (no quedan bloqueadas).
- Se muestran en orden cronologico con el nombre del operador y la hora.
- Se pueden eliminar individualmente con el boton de papelera.

---

## 8. Pase de Turno (OBLIGATORIO)

### Que es el pase de turno?
El pase de turno es el formulario obligatorio que cada operador debe completar al finalizar su turno. Contiene un resumen de las novedades y la conformidad de que las tareas del turno fueron completadas.

### Como realizar el pase de turno:
1. Hacer clic en el boton **"Pase de Turno [Turno]"** en el header (por ejemplo: "Pase de Turno Mañana").
2. Se abre un modal con los siguientes campos:
   - **Operador:** Seleccionar el nombre del operador que realiza el pase.
   - **Novedades (obligatorio):** Escribir un detalle de lo ocurrido durante el turno, incidencias, tareas pendientes, etc.
   - **Checkboxes de conformidad:** Confirmar que los pollings, backups y procesos estan completos.
3. Hacer clic en **Confirmar Pase**.

### Que sucede despues del pase de turno:
- El dia queda **bloqueado** para los operadores de otros turnos. Solo los administradores pueden modificar datos de un dia cerrado.
- Se genera una **notificacion automatica** que aparece en la campana de los operadores de los turnos entrantes.
- Si el operador intenta **salir del sistema** sin haber hecho el pase de turno, se muestra un mensaje de advertencia pidiendo confirmacion.

### Administradores y el pase de turno:
Los administradores pueden realizar el pase de turno igual que cualquier operador, pero el boton dice simplemente "Pase de Turno" sin especificar un turno en particular. Ademas, los administradores pueden modificar datos de dias que ya tienen pase de turno realizado.

---

## 9. Bloqueo de Dia Cerrado

Cuando un operador realiza el pase de turno, el dia queda cerrado. Esto significa:

### Para los operadores:
- No se pueden agregar, editar ni eliminar pollings, backups ni procesos.
- No se pueden cambiar los botones de agregar ni editar.
- **Si intentan modificar algo**, se muestra un modal centrado que dice "DIA CERRADO — Este dia ya tiene pase de turno. Solo un administrador puede modificar los datos."
- Las **novedades del turno** si se pueden seguir agregando (no quedan bloqueadas).
- El boton de **Copiar dia anterior** tampoco funciona en dias cerrados.

### Para los administradores:
- Pueden modificar todo sin restriccion: agregar, editar y eliminar pollings, backups y procesos.
- Se muestra un banner amarillo "DIA CERRADO" como recordatorio, pero no se bloquea la edicion.
- Los botones de edicion y eliminacion aparecen normalmente.

---

## 10. Dashboard Administrativo

El dashboard esta disponible unicamente para usuarios con rol **Administrador**.

### Como acceder:
Hacer clic en el icono de cuadrados (Dashboard) en el header.

### Contenido del dashboard:
- **Selector de periodo:** Permite filtrar por semana, mes, anio o historico completo.
- **Metricas generales:** Total de dias con datos, pollings completados, backups realizados, tasa de error de procesos.
- **Tabla de detalles por dia:** Muestra cada dia con su tipo, cantidad de pollings, backups, procesos y estados.

### Reportes descargables:
Desde el dashboard se pueden descargar tres tipos de reportes en formato HTML:
1. **Reporte General del Dashboard:** Resumen del periodo seleccionado con todas las metricas.
2. **Pases de Turno:** Listado historico de todos los pases de turno realizados, ordenados por fecha.
3. **Reporte por Dia:** Seleccionando una fecha especifica, se descarga un reporte detallado con todos los datos de ese dia (pollings, backups, procesos, novedades y pases de turno).

Para descargar el reporte por dia, usar el **selector de fecha** que esta al lado del boton "Descargar Dia" dentro del dashboard.

---

## 11. Notificaciones

### Como funcionan:
- Cuando un operador realiza el pase de turno, se genera una notificacion para los turnos entrantes.
- La campana en el header muestra un numero rojo con las notificaciones sin leer.
- Hacer clic en la campana despliega un panel con todas las notificaciones.
- El boton **"Marcar leidas"** marca todas como leidas y quita el numero rojo.

### Que genera notificaciones:
- **Pase de turno:** Cada vez que un operador confirma el pase, se notifica a los demas turnos.
- **Novedades del timeline:** Cuando se agrega una nota al timeline.

---

## 12. Otras Funcionalidades

### Copiar dia anterior:
El boton **"Copiar dia anterior"** copia toda la estructura del dia previo (pollings, backups, procesos) al dia actual. Los horarios se limpian para que se completen manualmente. Es util para dias con la misma estructura operativa.

### Exportar a CSV:
El boton **"Exportar CSV"** descarga un archivo con todos los datos del dia actual en formato de valores separados por comas. Se puede abrir con Excel, Google Sheets o cualquier hoja de calculo.

### Modo oscuro/claro:
El icono de sol/luna en el header permite alternar entre el tema claro y el tema oscuro. La preferencia se guarda automaticamente en el navegador.

### Navegacion por fecha:
- Las flechas permiten moverse dia a dia.
- Hacer clic en la fecha abre un calendario para saltar directamente a cualquier fecha.
- El boton "Hoy" vuelve al dia actual.

### Busqueda:
El campo de busqueda en la barra de acciones rapidas filtra los items mostrados en la pestana activa. Escribe parte del nombre de un servidor, backup o proceso para filtrar rapidamente.

---

## 13. Sincronizacion con GitHub

### Como funciona:
- Los datos se guardan automaticamente en el navegador (localStorage) y tambien se sincronizan con GitHub.
- El **indicador de sincronizacion** (icono de engranaje) gira cuando hay cambios pendientes de subir y se detiene cuando todo esta sincronizado.
- Cada dia se guarda como un archivo JSON separado en la carpeta `data/` del repositorio de GitHub.
- La sincronizacion tiene un retraso de 500ms (debounce) para no hacer demasiadas peticiones mientras se escribe.

### Que hacer si la sincronizacion falla:
- Verificar la conexion a internet.
- Recargar la pagina (los datos se mantienen en el navegador).
- Si el problema persiste, contactar al administrador del sistema.

---

## 14. Resolucion de Problemas Comunes

### "No puedo editar nada, el dia esta cerrado"
Esto es normal. Cuando un turno completo el pase de turno, el dia se bloquea. Solo un **administrador** puede modificar datos en un dia cerrado. Contactar a un administrador si es necesario hacer correcciones.

### "No encuentro el boton de agregar"
Los botones de agregar solo se muestran si el dia no esta cerrado. Si el dia esta cerrado y usted es operador, no podra agregar datos. Si usted es administrador, los botones deberian aparecer con normalidad.

### "Olvide hacer el pase de turno y ya me fui"
Inicie sesion nuevamente, navegue al dia correspondiente y realice el pase de turno. El sistema lo permitira mientras no se haya cerrado el dia desde otra cuenta.

### "Los datos no se ven en otra computadora"
Verifique que el indicador de sincronizacion no este girando. Si esta detenido, los datos estan en GitHub. Si el problema persiste, puede haber un problema de conexion o de cache del navegador.

### "Quiero corregir un dato de un dia anterior"
Si el dia no esta cerrado, puede navegar a la fecha y editarlo normalmente. Si el dia esta cerrado, necesita iniciar sesion como **administrador** para poder modificarlo.

---

## 15. Estructura de Datos

Cada dia se almacena como un objeto JSON con la siguiente estructura:

| Campo | Descripcion |
|-------|-------------|
| `date` | Fecha del dia (formato YYYY-MM-DD) |
| `dayType` | Tipo de dia: DIARIA, FIN_DE_SEMANA o BKP_MENSUAL |
| `pollings` | Array de pollings con servidor, region, fase (BEGINNING/ENDING), hora y nota |
| `backups` | Array de backups con nombre, job, fechas, horas, duracion y estado |
| `processes` | Array de procesos con nombre y estado (OK/Error) |
| `notes` | Notas generales del dia |
| `timeline` | Array de novedades con operador, texto y hora |
| `handovers` | Array de pases de turno con operador, turno, texto, hora y checks |
| `notifications` | Array de notificaciones para el panel de notificaciones |

---

## 16. Colores y Identificacion Visual

### Colores institucionales Semantix:
- **Violeta (#6A0DAD):** Color principal, usado para botones principales, links y acentos.
- **Teal (#00E5B8):** Color secundario, usado para indicar estado OK y elementos positivos.
- **Azul (#4A90E2):** Color terciario, usado para informacion y elementos neutros.

### Badges de estado:
- **OK:** Badge verde/violeta con tilde.
- **Error:** Badge rojo con equis.
- **Sin estado:** Badge gris.

### Colores de turno:
- **Mañana:** Azul claro.
- **Tarde:** Amarillo.
- **Noche:** Violeta.
- **Admin:** Violeta oscuro.