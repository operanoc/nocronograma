# Bitacora NOC — Sistema de Registro Operativo

## Descripcion

Sistema web para el registro operativo del NOC (Network Operations Center). Permite a los operadores de cada turno registrar toda la actividad diaria: pollings de servidores, backups, procesos batch, novedades de turno y pase de turno.

## Acceso

**URL:** https://lecatexzonanorte.github.io/nocronograma/bitacora_noc_con_login.html

### Usuarios

| Usuario | Password | Rol | Turno |
|---------|----------|-----|-------|
| OPERAMAÑANA | mañana1 | Operador | Mañana |
| OPERATARDE | tarde1 | Operador | Tarde |
| OPERANOCHE | noche1 | Operador | Noche |
| OPERAADMIN | nocadmin | Administrador | Admin |
| OPERAWU | 0p3r4ci0n35 | Administrador | Admin |
| ADMILOSN | admilosn | Administrador | Admin |
| NOCPRUEBA | pruebanoc | Administrador | Admin (pruebas) |

## Funcionalidades

### Registro de datos por dia
- **Pollings:** Registro de inicio y fin de cada polling por servidor, agrupados por pais (Argentina, Peru, Panama, Chile, Mexico)
- **Backups:** Control de backups con **fecha y hora de inicio/fin**, duracion calculada automaticamente (soporta backup que cruza medianoche, ej: lunes 22hs a martes 06hs), JOB y estado
- **Procesos:** Checklist con 9 procesos fijos (Tarjeta Naranja, EPE, BANCOR, Rentas de Cordoba, AFIP 72, AFIP 24, AFIP 48, Cierre AFIP, Montaje de cintas) con estados **OK / Error**, mas opcion de crear procesos personalizados
- **Novedades del turno:** Timeline cronologico de novedades por operador (se pueden agregar incluso en dias cerrados)
- **Copia de dia anterior:** Con un boton se copia la estructura del dia previo

### Pase de turno (OBLIGATORIO)
- El boton del header dice **"Pase de Turno Mañana"**, **"Pase de Turno Tarde"** o **"Pase de Turno Noche"** segun el turno del usuario
- Al finalizar cada turno, el operador debe completar el formulario con novedades y checks de conformidad
- El pase genera una notificacion automatica para los turnos entrantes
- Al intentar salir sin hacer el pase, el sistema lo advierte
- Los administradores ven el boton como **"Pase de Turno"** (sin turno especifico)

### Bloqueo de dia cerrado
- Cuando un turno realiza el pase de turno, **el dia queda bloqueado para operadores**
- Solo los usuarios con rol **Administrador** pueden modificar datos de un dia cerrado (agregar, editar, eliminar)
- Se muestra un banner amarillo "DIA CERRADO" y un modal centrado para operadores
- Los botones de agregar, editar y eliminar se ocultan para operadores
- Las novedades del timeline se pueden seguir agregando en dias cerrados

### Dashboard administrativo (solo Admin)
- Metricas y estadisticas por periodo (semanal, mensual, anual, historico)
- Descarga de reportes en HTML:
  - Reporte general del dashboard
  - Reporte de pases de turno
  - Reporte por dia especifico (con selector de fecha, funciona incluso sin datos)

### Otras funcionalidades
- Navegacion por fecha con calendario integrado
- Busqueda de servidores y procesos
- Exportacion a CSV
- Modo oscuro/claro
- Panel de notificaciones con badge de no leidas
- Sincronizacion automatica con GitHub (almacenamiento en la nube)
- Indicador de estado de sincronizacion en el header
- Colores institucionales Semantix (violeta #6A0DAD, teal #00E5B8, azul #4A90E2)

## Manual de Usuario

El manual de usuario completo esta disponible en: [MANUAL_USUARIO.md](./MANUAL_USUARIO.md)

## Archivos del Repositorio

| Archivo | Descripcion |
|---------|-------------|
| `bitacora_noc_con_login.html` | Aplicacion completa (archivo unico, sin dependencias) |
| `MANUAL_USUARIO.md` | Manual de usuario detallado |
| `README.md` | Este archivo |
| `data/*.json` | Datos de cada dia (generados automaticamente) |

## Arquitectura

- Aplicacion de un solo archivo HTML (sin dependencias externas, sin build tools)
- Almacenamiento: GitHub Contents API
- Cada dia se guarda como un archivo JSON en `data/`
- Sincronizacion automatica con debounce de 500ms
- Cache de SHA para evitar GET antes de PUT
- Token de acceso embebido (ofuscado como array de char codes)