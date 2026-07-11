# Bitacora NOC — Sistema de Registro Operativo

## Descripcion

Sistema web para el registro operativo del NOC (Network Operations Center) de Semantix. Permite a los operadores de cada turno registrar toda la actividad diaria: pollings de servidores, backups, procesos batch, novedades de turno y pase de turno.

La aplicacion es un archivo HTML unico sin dependencias externas, con almacenamiento en la nube via GitHub Contents API y sincronizacion automatica.

**URL:** https://lecatexzonanorte.github.io/nocronograma/bitacora_noc_con_login.html

## Usuarios y Cuentas

Cada operador tiene su propia cuenta individual con su nombre real, lo que permite un registro de auditoria completo (quien cargo que y cuando).

### Operadores

| Usuario | Password por defecto | Nombre Completo | Turnos Disponibles |
|---------|---------------------|-----------------|-------------------|
| STORREZ | Atos.123$ | Sebastian Torrez | Manana, Tarde, Noche (selector) |
| DDIPINO | Atos.123$ | Daniel Di Pino | Manana (solo findes de semana) |
| FGODOY | Atos.123$ | Fulgencio Godoy | Tarde (L-V) |
| HNUNEZ | Atos.123$ | Humberto Nunez | Tarde (findes de semana) |
| HMAGARINOS | Atos.123$ | Hugo Magarinos | Noche (L-V) |
| GCASTELLANI | Atos.123$ | Gustavo Castellani | Noche (findes de semana) |
| ARIVERO | Atos.123$ | Anibal Rivero | Noche (viernes) + Manana, Tarde, Noche (selector) |
| OBALDOMIR | Atos.123$ | Omar Baldomir | Manana, Tarde (selector) |

### Administradores

| Usuario | Password | Nombre |
|---------|----------|--------|
| OPERAADMIN | nocadmin | Admin principal |
| OPERAWU | 0p3r4ci0n35 | Cliente (consulta) |

> **Nota:** Los administradores pueden cambiar y blanquear contraseñas de cualquier usuario desde el menu Admin (sincronizado via GitHub, funciona en todos los navegadores).

## Funcionalidades

### Login y Sesiones
- Pantalla de login con tema dark/tech navy
- Cuentas individuales por operador (audit trail por usuario)
- Deteccion automatica de turno segun hora del dia y dia de la semana
- **Selector de turno** para operadores con multiples turnos asignados (Torrez, Rivero, Baldomir): al iniciar sesion se muestra un dialogo para elegir que turno van a trabajar
- Sesion persistente en el navegador (recargar no pide login de nuevo)

### Registro de datos por dia
- **Pollings:** Registro de inicio y fin de cada polling por servidor, agrupados por pais (Argentina, Peru, Panama, Chile, Mexico)
- **Backups:** Control de backups con fecha y hora de inicio/fin, duracion calculada automaticamente (soporta backup que cruza medianoche), JOB y estado
- **Procesos:** Checklist con 9 procesos fijos (Tarjeta Naranja, EPE, BANCOR, Rentas de Cordoba, AFIP 72/24/48, Cierre AFIP, Montaje de cintas) con estados OK/Error, mas procesos personalizados
- **Novedades del turno:** Timeline cronologico con nombre de operador y hora (se pueden agregar incluso en dias cerrados)
- **Copia de dia anterior:** Copia la estructura del dia previo con horarios limpios

### Pase de turno (OBLIGATORIO)
- Boton en el header con el nombre del turno del usuario ("Pase de Turno MANANA", etc.)
- Formulario con novedades obligatorias y checks de conformidad
- Al realizar el pase, el dia queda **bloqueado** para operadores (solo admin puede modificar)
- Notificacion automatica para los turnos entrantes
- Advertencia al intentar salir sin hacer el pase

### Dashboard administrativo (solo Admin)
- Metricas y estadisticas por periodo (semanal, mensual, anual, historico)
- Descarga de reportes en HTML (general, pases de turno, por dia especifico)
- Accesible desde el menu hamburguesa Admin

### Administracion de usuarios (solo Admin)
- **Blanquear/cambiar contraseñas:** Desde el menu Admin se pueden cambiar las contraseñas de todos los usuarios. Los cambios se sincronizan con GitHub y funcionan en Chrome, Firefox y Edge (todos los navegadores)
- **Historial de auditoria:** Registro de pases de turno y reaperturas de dias con fecha, hora, usuario y detalle

### Otras funcionalidades
- Navegacion por fecha con calendario integrado
- Busqueda de servidores y procesos
- Exportacion a CSV
- Importacion de datos desde XLSX (solo Admin)
- Panel de notificaciones con badge de no leidas
- Sincronizacion automatica con GitHub (indicador de estado en el header)
- Tema dark por defecto con colores navy/purpura/teal

## Archivos del Repositorio

| Archivo | Descripcion |
|---------|-------------|
| `bitacora_noc_con_login.html` | Aplicacion completa (archivo unico, sin dependencias) |
| `MANUAL_USUARIO.pdf` | Manual de usuario detallado |
| `README.md` | Este archivo |
| `data/*.json` | Datos de cada dia (generados automaticamente) |
| `data/passwords.json` | Overrides de contraseñas (generado automaticamente) |

## Arquitectura

- Aplicacion de un solo archivo HTML (sin dependencias externas, sin build tools)
- Almacenamiento: GitHub Contents API
- Cada dia se guarda como un archivo JSON en `data/`
- Sincronizacion automatica con debounce de 500ms
- Cache de SHA para evitar GET antes de PUT
- Token de acceso embebido (ofuscado como array de char codes)

## Manual de Usuario

El manual de usuario completo esta disponible en: [MANUAL_USUARIO.pdf](./MANUAL_USUARIO.pdf)