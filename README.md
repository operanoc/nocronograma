# Bitacora NOC — Sistema de Registro Operativo

Sistema web para el registro operativo del NOC (Network Operations Center) de Semantix. Permite a los operadores de cada turno registrar toda la actividad diaria: pollings de servidores, backups, procesos batch, novedades de turno y pase de turno.

Aplicacion de un solo archivo HTML, sin dependencias de build, con almacenamiento en la nube via GitHub Contents API y sincronizacion automatica entre navegadores.

**URL:** https://operanoc.github.io/nocronograma/

## Usuarios

### Operadores

| Usuario | Nombre | Turnos |
|---------|--------|--------|
| STORREZ | Sebastian Torrez | Manana, Tarde, Noche |
| DDIPINO | Daniel Di Pino | Manana (findes de semana) |
| FGODOY | Fulgencio Godoy | Tarde (L-V) |
| HNUNEZ | Humberto Nunez | Tarde (findes de semana) |
| HMAGARINOS | Hugo Magarinos | Noche (L-V) |
| GCASTELLANI | Gustavo Castellani | Noche (findes de semana) |
| ARIVERO | Anibal Rivero | Noche (viernes) + backup |
| OBALDOMIR | Omar Baldomir | Manana, Tarde (backup) |

### Administradores

| Usuario | Rol |
|---------|-----|
| OPERAADMIN | Admin principal |
| OPERAWU | Cliente (consulta) |

## Funcionalidades

- **Pollings** — Registro de inicio/fin por servidor, agrupados por pais. Si no se cargan horarios se marca como "SIN AC"
- **Backups** — Control con fecha, hora, duracion automatica, JOB y estado
- **Procesos** — Checklist de procesos fijos + personalizados con estado OK/Error
- **Novedades** — Timeline cronologico con operador y hora
- **Pase de turno** — Obligatorio, bloquea el dia para operadores
- **Dashboard** — Metricas y reportes por periodo (solo Admin)
- **Sincronizacion** — Automatica via GitHub, funciona entre Chrome/Firefox/Edge
- **Calendario** — Navegacion por fecha con indicadores visuales
- **Busqueda** — Filtros de servidores y procesos
- **Exportar** — Descarga en CSV
- **Importar** — Carga desde XLSX (solo Admin)

## Archivos

```
nocronograma/
  index.html          — Aplicacion completa
  login-bg.png        — Fondo de login
  .gitignore
  README.md
  data/
    *.json            — Datos de cada dia (auto-generados)
    passwords.json    — Overrides de contrasenas
```

## Arquitectura

- Single HTML file, sin build tools
- GitHub Contents API para persistencia
- Sincronizacion con debounce de 500ms
- Cache de SHA para optimizar PUTs
- Token ofuscado como array de char codes