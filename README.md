# SBC CRM

Sistema de Gestión de Relaciones con Clientes personalizado para SBC Internationals

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![Frappe](https://img.shields.io/badge/frappe-v14%2B-orange.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## 🎯 Descripción

SBC CRM es un sistema completo de gestión diseñado específicamente para la industria turística, enfocado en:

- Gestión integral de clientes turísticos (hoteles, agencias, touroperadores)
- Administración de reservas de paquetes turísticos
- Seguimiento de actividades comerciales
- Análisis y reportes de ventas

## ✨ Características Principales

### 📋 Gestión de Clientes
- ✅ Información completa del cliente
- ✅ Múltiples contactos por cliente
- ✅ Categorización automática (Premium, Estándar, Potencial, Inactivo)
- ✅ Dashboard con métricas clave
- ✅ Exportación de contactos

### 🎫 Gestión de Reservas
- ✅ Paquetes turísticos completos
- ✅ Cálculos automáticos (noches, totales, comisiones)
- ✅ Servicios adicionales configurables
- ✅ Sistema de descuentos
- ✅ Control de estados (Borrador → Confirmada → Completada)
- ✅ Workflow con Submit/Cancel

### 📅 Actividades Comerciales
- ✅ Gestión de reuniones, llamadas, visitas
- ✅ Sistema de seguimiento automático
- ✅ Vista de calendario
- ✅ Recordatorios por email
- ✅ Vinculación con clientes y reservas
- ✅ Exportación a Google Calendar

### 📊 Reportes y Análisis
- ✅ Ventas por cliente
- ✅ Ventas por destino
- ✅ Dashboard de actividades
- ✅ Gráficos interactivos
- ✅ Exportación a Excel/CSV/PDF

### ⚡ Automatizaciones
- ✅ Recordatorios diarios de actividades
- ✅ Actualización automática de categorías
- ✅ Reporte semanal de ventas
- ✅ Análisis mensual

## 🚀 Instalación Rápida

```bash
# Obtener la aplicación
cd /path/to/frappe-bench
bench get-app https://github.com/tu-usuario/sbc_cr34

# Instalar en un sitio
bench --site tu-sitio.local install-app sbc_cr34

# Migrar
bench --site tu-sitio.local migrate

# Reiniciar
bench restart
```

Ver [INSTALLATION_GUIDE.md](INSTALLATION_GUIDE.md) para instrucciones detalladas.

## 📖 Documentación

- **[Guía de Instalación](INSTALLATION_GUIDE.md)**: Instalación paso a paso
- **[Guía de Usuario](USER_GUIDE.md)**: Manual completo de uso
- **[Documentación Técnica](TECHNICAL_DOCS.md)**: Detalles técnicos para desarrolladores

## 📦 Estructura del Proyecto

```
sbc_crm_complete/
├── doctypes/                   # Definiciones JSON de DocTypes
│   ├── cliente_turistico.json
│   ├── cliente_contacto_adicional.json
│   ├── reserva_paquete.json
│   ├── servicio_adicional_reserva.json
│   └── actividad_comercial.json
│
├── server_scripts/            # Controladores Python
│   ├── cliente_turistico.py
│   ├── reserva_paquete.py
│   ├── actividad_comercial.py
│   ├── tasks.py
│   ├── notifications.py
│   └── install.py
│
├── client_scripts/            # Scripts JavaScript
│   ├── cliente_turistico.js
│   ├── reserva_paquete.js
│   └── actividad_comercial.js
│
├── reports/                   # Reportes personalizados
│   ├── sales_by_client.py
│   ├── sales_by_destination.py
│   └── activity_dashboard.py
│
├── hooks/                     # Configuración
│   └── hooks.py
│
├── INSTALLATION_GUIDE.md
├── USER_GUIDE.md
└── README.md
```

## 🔧 Requisitos

- Frappe Framework v14+ o v15+
- Python 3.8+
- MariaDB 10.3+
- Node.js 14+

## 💡 Uso Rápido

### Crear un Cliente

```python
# Via web UI
1. Ir a Cliente Turistico > Nuevo
2. Ingresar Nombre Empresa
3. Seleccionar Tipo y Categoría
4. Completar Contacto Principal
5. Guardar

# Via código
client = frappe.get_doc({
    "doctype": "Cliente Turistico",
    "nombre_empresa": "Hotel Paradise",
    "tipo_cliente": "Hotel",
    "categoria": "Premium",
    "contacto_principal": "Juan Pérez",
    "email": "juan@hotelparadise.com",
    "pais": "Spain",
    "ciudad": "Barcelona"
})
client.insert()
```

### Crear una Reserva

```python
# Via web UI
1. Ir a Reserva Paquete > Nuevo
2. Seleccionar Cliente
3. Ingresar Destino y Fechas
4. Agregar Pasajeros
5. Configurar Paquete
6. Submit cuando esté confirmada

# Via código
reserva = frappe.get_doc({
    "doctype": "Reserva Paquete",
    "titulo_reserva": "Mallorca 7 Noches",
    "cliente": "Hotel Paradise",
    "destino": "Palma de Mallorca",
    "pais_destino": "Spain",
    "fecha_inicio": "2025-06-01",
    "fecha_fin": "2025-06-08",
    "num_adultos": 2,
    "valor_paquete_base": 1200
})
reserva.insert()
reserva.submit()
```

### Crear una Actividad

```python
# Via web UI
1. Ir a Actividad Comercial > Nuevo
2. Ingresar Título
3. Seleccionar Tipo
4. Vincular Cliente/Reserva
5. Programar Fecha
6. Guardar

# Via código
actividad = frappe.get_doc({
    "doctype": "Actividad Comercial",
    "titulo": "Reunión con Hotel Paradise",
    "tipo_actividad": "Reunión",
    "cliente": "Hotel Paradise",
    "fecha_hora": "2025-02-01 10:00:00",
    "duracion_minutos": 60
})
actividad.insert()
```

## 🎨 Capturas de Pantalla

### Dashboard de Cliente
```
┌─────────────────────────────────────────┐
│ Hotel Paradise                          │
│ ★★★★ - Premium                         │
├─────────────────────────────────────────┤
│ 📊 Estadísticas                         │
│   Total Reservas: 15                    │
│   Completadas: 12                       │
│   Valor Total: €25,000                  │
│   Comisiones: €3,750                    │
└─────────────────────────────────────────┘
```

### Formulario de Reserva
```
┌─────────────────────────────────────────┐
│ Reserva: RSV-2025-00001                 │
│ Cliente: Hotel Paradise                 │
│ Estado: ● Confirmada                    │
├─────────────────────────────────────────┤
│ Destino: Palma de Mallorca              │
│ Fechas: 01/06/2025 - 08/06/2025         │
│ Noches: 7 (automático)                  │
│                                         │
│ Pasajeros:                              │
│   Adultos: 2                            │
│   Total: 2 (automático)                 │
│                                         │
│ Valor Total: €1,200.00                  │
│ Comisión: €180.00 (15%)                 │
└─────────────────────────────────────────┘
```

## 🔐 Roles y Permisos

### Sales Master Manager
- ✅ Acceso completo a todos los DocTypes
- ✅ Submit/Cancel de reservas
- ✅ Eliminar registros
- ✅ Todos los reportes
- ✅ Configuración del sistema

### Sales User
- ✅ Crear/Editar clientes
- ✅ Crear/Editar/Submit reservas
- ✅ Crear/Editar actividades
- ✅ Ver reportes
- ❌ Eliminar registros

## 📈 Cálculos Automáticos

El sistema calcula automáticamente:

| Campo | Cálculo |
|-------|---------|
| Número de Noches | `fecha_fin - fecha_inicio` |
| Total Personas | `adultos + niños + bebés` |
| Total Servicios | `Σ(cantidad × precio_unitario)` |
| Descuento | `(base + servicios) × descuento%` |
| Valor Total | `(base + servicios) - descuento` |
| Comisión | `valor_total × comisión%` |
| Fecha Fin Actividad | `fecha_hora + duración_minutos` |

## ⏰ Tareas Programadas

| Frecuencia | Tarea | Descripción |
|------------|-------|-------------|
| Diario | Recordatorios de Actividades | Email con actividades del día |
| Diario | Actualizar Categorías | Clasifica clientes por actividad |
| Semanal | Reporte de Ventas | Email a managers con estadísticas |
| Mensual | Análisis | Genera métricas mensuales |

## 🔌 API y Webhooks

### Métodos Whitelisted

```python
# Obtener información de cliente
frappe.call({
    method: 'sbc_cr34.sbc_crm.doctype.cliente_turistico.cliente_turistico.get_client_summary',
    args: { client_name: 'Hotel Paradise' }
})

# Duplicar reserva
frappe.call({
    method: 'sbc_cr34.sbc_crm.doctype.reserva_paquete.reserva_paquete.duplicate_reservation',
    args: { source_name: 'RSV-2025-00001' }
})

# Marcar actividad como completada
frappe.call({
    method: 'sbc_cr34.sbc_crm.doctype.actividad_comercial.actividad_comercial.mark_as_completed',
    args: { activity_name: 'ACT-2025-00001' }
})
```

## 🛠️ Desarrollo

### Configurar Entorno de Desarrollo

```bash
# Clonar repo
git clone https://github.com/tu-usuario/sbc_cr34
cd sbc_cr34

# Instalar en modo desarrollo
bench get-app .
bench --site dev.local install-app sbc_cr34

# Habilitar developer mode
bench --site dev.local set-config developer_mode 1

# Watch para cambios
bench watch
```

### Agregar Nuevos Campos

```python
# Crear Custom Field
frappe.get_doc({
    "doctype": "Custom Field",
    "dt": "Cliente Turistico",
    "fieldname": "custom_field_name",
    "label": "Custom Field",
    "fieldtype": "Data"
}).insert()
```

### Crear Nuevo Reporte

```python
# En reports/mi_reporte.py
def execute(filters=None):
    columns = get_columns()
    data = get_data(filters)
    return columns, data

def get_columns():
    return [{"label": "Campo", "fieldtype": "Data"}]

def get_data(filters):
    return frappe.db.sql("SELECT ...", as_dict=1)
```

## 🧪 Testing

```bash
# Ejecutar tests
bench --site test.local run-tests --app sbc_cr34

# Test específico
bench --site test.local run-tests --app sbc_cr34 --module sbc_crm.doctype.reserva_paquete.test_reserva_paquete
```

## 📝 Changelog

### v1.0.0 (Enero 2025)
- ✨ Release inicial
- ✅ Gestión completa de clientes
- ✅ Sistema de reservas
- ✅ Actividades comerciales
- ✅ Reportes básicos
- ✅ Automatizaciones
- ✅ Notificaciones

## 🤝 Contribuir

Las contribuciones son bienvenidas! Por favor:

1. Fork el proyecto
2. Crear branch (`git checkout -b feature/AmazingFeature`)
3. Commit cambios (`git commit -m 'Add AmazingFeature'`)
4. Push al branch (`git push origin feature/AmazingFeature`)
5. Abrir Pull Request

## 📄 Licencia

Este proyecto está licenciado bajo MIT License - ver [LICENSE](LICENSE) para detalles.

## 👥 Autores

- **SBC Internationals** - *Desarrollo inicial*

## 🙏 Agradecimientos

- Frappe Framework team
- ERPNext community
- Todos los contribuidores

## 📞 Soporte

- **Email**: sbcinternational@protonmail.com
- **Issues**: [GitHub Issues](https://github.com/tu-usuario/sbc_cr34/issues)
- **Documentación**: Ver carpeta `docs/`

## 🗺️ Roadmap

### v1.1 (Próximo)
- [ ] Dashboard interactivo mejorado
- [ ] Integración con WhatsApp Business
- [ ] App móvil
- [ ] API REST completa

### v1.2 (Futuro)
- [ ] Machine Learning para predicciones
- [ ] Integración con sistemas de reserva
- [ ] Multi-idioma completo
- [ ] Portal de clientes

---

**Desarrollado con ❤️ por SBC Internationals**

**© 2024-2025 SBC Internationals. Todos los derechos reservados.**
