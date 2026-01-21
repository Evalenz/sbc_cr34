# SBC CRM - Guía de Instalación

## Descripción General

SBC CRM es un sistema de gestión de relaciones con clientes personalizado para SBC Internationals, diseñado específicamente para la industria turística.

## Características Principales

### Gestión de Clientes
- Información completa de clientes turísticos (hoteles, agencias, touroperadores)
- Contactos múltiples por cliente
- Categorización automática (Premium, Estándar, Potencial, Inactivo)
- Seguimiento de volumen anual y comisiones

### Gestión de Reservas
- Sistema completo de paquetes turísticos
- Cálculos automáticos (noches, personas, totales, comisiones)
- Servicios adicionales configurables
- Control de estados y workflow
- Sistema de descuentos

### Actividades Comerciales
- Gestión de reuniones, llamadas, eventos
- Sistema de seguimiento automático
- Calendario integrado
- Recordatorios automáticos
- Vinculación con clientes y reservas

### Reportes
- Ventas por cliente
- Ventas por destino
- Dashboard de actividades
- Análisis de tendencias

## Requisitos

- Frappe Framework v14+ o v15+
- ERPNext v14+ o v15+ (opcional pero recomendado)
- Python 3.8+
- MariaDB 10.3+

## Instalación

### 1. Preparación del Entorno

```bash
# Ir al directorio de bench
cd /path/to/frappe-bench

# Obtener la aplicación
bench get-app https://github.com/tu-usuario/sbc_cr34
```

### 2. Instalar en un Sitio

```bash
# Instalar la app en tu sitio
bench --site tu-sitio.local install-app sbc_cr34

# Migrar
bench --site tu-sitio.local migrate

# Reiniciar bench
bench restart
```

### 3. Configuración Inicial

1. Acceder al sistema como Administrator
2. Ir a **Setup > Users and Permissions > Role**
3. Verificar que existen los roles:
   - Sales Master Manager
   - Sales User

4. Asignar roles a usuarios correspondientes

## Estructura de DocTypes

### Cliente Turistico
DocType principal para gestión de clientes con:
- Información básica (nombre, tipo, categoría)
- Contacto principal
- Contactos adicionales (tabla hija)
- Ubicación
- Información comercial (comisiones, métodos de pago)
- Redes sociales y web

### Reserva Paquete
DocType submittable para reservas con:
- Información de cliente
- Destino y fechas
- Pasajeros
- Detalles del paquete
- Servicios adicionales (tabla hija)
- Cálculos financieros automáticos
- Notas y requisitos

### Actividad Comercial
DocType para tracking de actividades con:
- Tipo de actividad
- Cliente relacionado
- Reserva relacionada (opcional)
- Fechas y duración
- Ubicación
- Resultados y seguimiento

## Ubicación de Archivos

Una vez instalado, los archivos se ubicarán en:

```
frappe-bench/
└── apps/
    └── sbc_cr34/
        ├── sbc_cr34/
        │   ├── sbc_crm/
        │   │   ├── doctype/
        │   │   │   ├── cliente_turistico/
        │   │   │   ├── cliente_contacto_adicional/
        │   │   │   ├── reserva_paquete/
        │   │   │   ├── servicio_adicional_reserva/
        │   │   │   └── actividad_comercial/
        │   │   └── report/
        │   ├── public/
        │   │   └── js/
        │   ├── hooks.py
        │   └── tasks.py
        └── setup.py
```

## Configuración de DocTypes

### Para crear manualmente los DocTypes:

1. **Cliente Turistico**
   - Ir a Customization > DocType > New
   - Copiar contenido de `doctypes/cliente_turistico.json`
   - Guardar

2. **Cliente Contacto Adicional** (Child Table)
   - Crear como istable=1
   - Copiar contenido de `doctypes/cliente_contacto_adicional.json`

3. **Reserva Paquete**
   - Crear como is_submittable=1
   - Copiar contenido de `doctypes/reserva_paquete.json`

4. **Servicio Adicional Reserva** (Child Table)
   - Crear como istable=1
   - Copiar contenido de `doctypes/servicio_adicional_reserva.json`

5. **Actividad Comercial**
   - Copiar contenido de `doctypes/actividad_comercial.json`

## Instalación de Scripts

### Server Scripts (Python Controllers)

Ubicar en: `apps/sbc_cr34/sbc_cr34/sbc_crm/doctype/[doctype_name]/[doctype_name].py`

1. **reserva_paquete.py** - Controlador de Reserva Paquete
2. **actividad_comercial.py** - Controlador de Actividad Comercial
3. **cliente_turistico.py** - Controlador de Cliente Turístico

### Client Scripts (JavaScript)

Ubicar en: `apps/sbc_cr34/sbc_cr34/public/js/`

1. **reserva_paquete.js**
2. **actividad_comercial.js**
3. **cliente_turistico.js**

Registrar en hooks.py:
```python
doctype_js = {
    "Cliente Turistico": "public/js/cliente_turistico.js",
    "Reserva Paquete": "public/js/reserva_paquete.js",
    "Actividad Comercial": "public/js/actividad_comercial.js"
}
```

### Scheduled Tasks

Ubicar en: `apps/sbc_cr34/sbc_cr34/tasks.py`

Las tareas programadas incluyen:
- **Diario**: Recordatorios de actividades, actualización de categorías
- **Semanal**: Reporte de ventas
- **Mensual**: Análisis y métricas

## Configuración de Reportes

### Reportes Incluidos:

1. **Sales by Client** (`reports/sales_by_client.py`)
   - Análisis de ventas por cliente
   - Gráficos de top clientes
   
2. **Sales by Destination** (`reports/sales_by_destination.py`)
   - Análisis por destino turístico
   - Métricas de ocupación

3. **Activity Dashboard** (`reports/activity_dashboard.py`)
   - Dashboard de actividades comerciales
   - Resumen de estados

Para instalar:
```bash
# Crear directorio de reportes
mkdir -p apps/sbc_cr34/sbc_cr34/sbc_crm/report/[report_name]

# Copiar archivos .py y .json
```

## Permisos

### Configuración de Permisos por Rol:

**Sales Master Manager:**
- CRUD completo en todos los DocTypes
- Puede Submit/Cancel reservas
- Acceso a todos los reportes

**Sales User:**
- CRUD en clientes y actividades
- CRUD y Submit en reservas
- Acceso a reportes
- Sin permisos de Delete

## Flujo de Trabajo Típico

### 1. Alta de Cliente
```
Crear Cliente Turistico > Completar información > 
Agregar contactos adicionales > Guardar
```

### 2. Crear Reserva
```
Crear Reserva Paquete > Seleccionar cliente (auto-rellena comisión) >
Ingresar destino y fechas (calcula noches) >
Ingresar pasajeros (calcula total) >
Agregar servicios adicionales >
Aplicar descuentos > Submit
```

### 3. Gestión de Actividades
```
Crear Actividad Comercial > Vincular a cliente/reserva >
Programar fecha > Completar actividad >
Crear seguimiento automático
```

## Características Avanzadas

### Cálculos Automáticos
- Número de noches entre fechas
- Total de personas (adultos + niños + bebés)
- Totales de servicios adicionales
- Descuentos por porcentaje
- Comisiones SBC

### Validaciones
- Fechas lógicas (fin > inicio)
- Emails válidos
- Campos requeridos según tipo

### Integraciones
- Sistema de notificaciones
- Envío de emails
- Calendario Google (exportación)
- Exportación CSV de contactos

## Tareas Programadas

### Configuración de Cron
Las tareas programadas se ejecutan automáticamente:

```python
scheduler_events = {
    "daily": [
        "sbc_cr34.tasks.send_daily_activity_reminder",
        "sbc_cr34.tasks.update_client_categories"
    ],
    "weekly": [
        "sbc_cr34.tasks.send_weekly_sales_report"
    ],
    "monthly": [
        "sbc_cr34.tasks.generate_monthly_analytics"
    ]
}
```

## Troubleshooting

### Error: DocType no encontrado
```bash
bench --site tu-sitio.local migrate
bench --site tu-sitio.local clear-cache
```

### Error: Permisos
```bash
bench --site tu-sitio.local set-admin-password [nueva-contraseña]
```

### Error: Scripts no cargan
```bash
bench build
bench restart
```

## Mantenimiento

### Backup Regular
```bash
bench --site tu-sitio.local backup --with-files
```

### Actualización
```bash
cd apps/sbc_cr34
git pull
cd ../..
bench --site tu-sitio.local migrate
bench restart
```

## Soporte

Para soporte técnico:
- Email: sbcinternational@protonmail.com
- Documentación: [Wiki del proyecto]

## Licencia

MIT License - Ver LICENSE.txt

## Créditos

Desarrollado por SBC Internationals
Copyright (c) 2024
