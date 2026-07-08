# Bitacora NOC - Sistema de Registro Operativo

## Descripcion

Sistema web para el registro operativo del NOC (Network Operations Center). Permite a los operadores de cada turno registrar toda la actividad diaria: pollings de servidores, backups, procesos batch, notas de turno y cierre de turno.

## Acceso

**URL:** https://lecatexzonanorte.github.io/nocronograma/bitacora_noc_con_login.html

### Usuarios

| Usuario | Password | Rol | Turno |
|---------|----------|-----|-------|
| OPERANOCHE | noche1 | Operador | Noche |
| OPERAMANANA | manana1 | Operador | Manana |
| OPERATARDE | tarde1 | Operador | Tarde |
| OPERAADMIN | nocadmin | Admin | Admin |
| OPERAWU | 0p3r4ci0n35 | Admin | Admin |
| NOCPRUEBA | pruebanoc | Admin | Admin (pruebas) |

## Funcionalidades

### Registro de datos por dia
- **Pollings:** Registro de inicio y fin de cada polling por servidor, agrupados por pais (Argentina, Peru, Panama, Chile, Mexico)
- **Backups:** Control de backups con **fecha y hora de inicio/fin**, duracion calculada automaticamente (soporta backup que cruza medianoche, ej: lunes 22hs a martes 06hs), JOB y estado
- **Procesos:** Checklist con 9 procesos fijos (Tarjeta Naranja, EPE, BANCOR, Rentas de Cordoba, AFIP 72, AFIP 24, AFIP 48, Cierre AFIP, Montaje de cintas) con estados **OK / Error**, mas opcion de crear procesos personalizados
- **Notas del turno:** Timeline cronologico de novedades por operador (se pueden agregar incluso en dias cerrados)
- **Copia de dia anterior:** Con un boton se copia la estructura del dia previo

### Cierre de turno (OBLIGATORIO)
- Al finalizar cada turno, el operador debe completar el formulario de cierre con novedades
- El cierre genera una notificacion automatica para los turnos entrantes
- Al intentar salir sin hacer el cierre, el sistema lo advierte

### Bloqueo de dia cerrado
- Cuando un turno realiza el cierre de turno, **el dia queda bloqueado para operadores**
- Solo los usuarios con rol **Admin** pueden modificar datos de un dia cerrado
- Se muestra un modal centrado indicando que el dia esta cerrado
- Los botones de agregar, editar y eliminar se ocultan para operadores
- Las notas del timeline se pueden seguir agregando en dias cerrados

### Dashboard administrativo (solo Admin)
- Metricas y estadisticas por periodo (semanal, mensual, anual, historico)
- Descarga de reportes en HTML:
  - Reporte general del dashboard
  - Reporte de cierres de turno
  - Reporte por dia especifico (con selector de fecha)

### Otras funcionalidades
- Navegacion por fecha con calendario integrado
- Busqueda de servidores y procesos
- Exportacion a CSV
- Modo oscuro/claro
- Sincronizacion automatica con GitHub (almacenamiento en la nube)
- Indicador de estado de sincronizacion en el header
- Colores institucionales Semantix (violeta #6A0DAD, teal #00E5B8, azul #4A90E2)

## Arquitectura

- Aplicacion de un solo archivo HTML (sin dependencias externas, sin build tools)
- Almacenamiento: GitHub Contents API
- Cada dia se guarda como un archivo JSON en `data/`
- Sincronizacion automatica con debounce de 500ms
- Cache de SHA para evitar GET antes de PUT
- Token de acceso embebido (ofuscado como array de char codes)
