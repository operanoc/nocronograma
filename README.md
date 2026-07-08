# NOC Bitacora

Sistema web de bitacora para el Centro de Operaciones de Red (NOC).
App de un solo archivo HTML con sincronizacion automatica via GitHub API.

## Archivos

| Archivo | Descripcion |
|---------|-------------|
| `bitacora_noc_con_login.html` | App principal (HTML+CSS+JS) |
| `data/` | Datos diarios como JSON (`YYYY-MM-DD.json`) |

## Funcionalidades

- **Login por turno** — 5 usuarios (Noche, Manana, Tarde, Admin, WU)
- **Pollings** — Registro de inicio/fin de polling por servidor con duracion automatica
- **Backups** — Control de backups diarios y mensuales con estados
- **Procesos** — Seguimiento de procesos batch (AFIP, Bancor, Metrogas, etc.)
- **Timeline** — Notas del operador con fecha, hora y nombre automatico segun turno
- **Cierre de Turno (OBLIGATORIO)** — Novedades al finalizar turno con checks de pollings/backups/procesos. Advertencia al login y al salir si no se completo
- **Notificaciones** — Alertas y novedades del turno
- **Dashboard Admin** — Estadisticas semanal/mensual/anual/historico con graficos de barras
- **Descarga de Reportes** — Reportes HTML descargables por periodo o por dia especifico (calendario)
- **Modo oscuro** — Toggle de tema claro/oscuro
- **Sincronizacion GitHub** — Todos los datos se guardan automaticamente en el repo via GitHub Contents API. localStorage como fallback offline
- **Indicador de sync** — Icono en el header muestra estado de sincronizacion (guardando/ok/error)

## Usuarios

| Usuario | Rol | Turno |
|---------|-----|-------|
| OPERANOCHE | Operador | Noche |
| OPERAMANANA | Operador | Manana |
| OPERATARDE | Operador | Tarde |
| OPERAWU | Admin | Soporte |
| OPERAADMIN | Admin | Administracion |

## Regiones

- Argentina
- Peru
- Panama
- Chile
- Mexico

## Como usar

1. Abrir `bitacora_noc_con_login.html` en el navegador (o via GitHub Pages)
2. Ingresar usuario, contrasena y token de GitHub
3. El token se guarda en la sesion del navegador (no en el archivo)
4. Registrar operaciones en las pestanas (Pollings, Backups, Procesos)
5. **Completar el Cierre de Turno antes de salir** (obligatorio)
6. Los datos se sincronizan automaticamente con este repositorio

## Deploy

La app se sirve via GitHub Pages:
`https://lecatexzonanorte.github.io/nocronograma/bitacora_noc_con_login.html`

Cada actualizacion del archivo HTML se refleja automaticamente al hacer push a la rama `main`.
