# NOC Bitacora

Sistema web de bitacora para el Centro de Operaciones de Red (NOC).

## Archivos

| Archivo | Descripcion |
|---------|-------------|
| `bitacora_noc_con_login.html` | App principal (HTML+CSS+JS) |
| `data/` | Datos diarios como JSON (`YYYY-MM-DD.json`) |

## Datos

Los datos se almacenan automaticamente en `data/`. Cada archivo JSON contiene:

- **Pollings** - Inicio/fin de polling por servidor y region
- **Backups** - Control de backups diarios y mensuales
- **Procesos** - Estado de procesos batch (AFIP, Bancor, Metrogas, etc.)
- **Timeline** - Notas del operador con marca de tiempo
- **Cierres de Turno** - Novedades al cierre de cada turno
- **Notificaciones** - Alertas y novedades

## Usuarios

| Usuario | Rol | Turno |
|---------|-----|-------|
| OPERANOCHE | Operador | Noche |
| OPERAMAÑANA | Operador | Manana |
| OPERATARDE | Operador | Tarde |
| OPERAWU | Admin | Soporte |
| OPERAADMIN | Admin | Administracion |

## Regiones

Argentina - Peru - Panama - Chile - Mexico

## Como usar

1. Abrir `bitacora_noc_con_login.html` en el navegador
2. Iniciar sesion con usuario y contrasena
3. Navegar por fechas y registrar operaciones
4. Los datos se sincronizan automaticamente con este repositorio
