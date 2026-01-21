# SBC CRM - Guía de Usuario

## Introducción

Bienvenido a SBC CRM, el sistema de gestión de clientes diseñado específicamente para las necesidades de SBC Internationals en la industria turística.

## Índice

1. [Inicio Rápido](#inicio-rápido)
2. [Gestión de Clientes](#gestión-de-clientes)
3. [Gestión de Reservas](#gestión-de-reservas)
4. [Actividades Comerciales](#actividades-comerciales)
5. [Reportes y Análisis](#reportes-y-análisis)
6. [Consejos y Mejores Prácticas](#consejos-y-mejores-prácticas)

---

## Inicio Rápido

### Acceso al Sistema

1. Navegar a `https://tu-sitio.local`
2. Iniciar sesión con sus credenciales
3. El módulo SBC CRM aparecerá en el escritorio principal

### Navegación Principal

- **Escritorio**: Vista general con accesos rápidos
- **Clientes**: Lista de clientes turísticos
- **Reservas**: Gestión de reservas de paquetes
- **Actividades**: Calendario y lista de actividades comerciales
- **Reportes**: Análisis y estadísticas

---

## Gestión de Clientes

### Crear un Nuevo Cliente

1. Ir a **Cliente Turistico > Nuevo**
2. Completar la información básica:
   - **Nombre Empresa** (requerido, será el ID del cliente)
   - **Tipo de Cliente**: Hotel, Cadena Hotelera, Agencia, etc.
   - **Categoría**: Premium, Estándar, Potencial, Inactivo

3. **Contacto Principal** (requerido):
   - Nombre del contacto
   - Cargo
   - Email (validado automáticamente)
   - Teléfonos

4. **Ubicación**:
   - País (requerido)
   - Ciudad (requerido)
   - Provincia/Estado
   - Dirección completa
   - Código postal

5. **Información Comercial**:
   - Comisión estándar (%) - Por defecto: 15%
   - Método de pago preferido
   - Días de crédito - Por defecto: 30
   - Volumen anual estimado
   - Empleado asignado

6. **Contactos Adicionales** (opcional):
   - Agregar otros contactos relevantes en la empresa
   - Cada contacto puede tener nombre, cargo, email, teléfono

7. Guardar

### Características Especiales de Clientes

#### Categorización Automática
El sistema sugiere automáticamente la categoría basándose en:
- Volumen anual estimado > €100,000 = Premium
- Volumen anual estimado > €50,000 = Estándar
- Resto = Potencial

El sistema actualiza automáticamente categorías a "Inactivo" si no hay actividad en 12 meses.

#### Campo de Estrellas
Solo aparece para clientes tipo "Hotel" o "Cadena Hotelera".

#### Dashboard del Cliente
Al abrir un cliente existente, verá:
- Total de reservas
- Reservas completadas
- Valor total generado
- Comisiones totales

#### Acciones Disponibles

**Botones en el formulario:**
- **Ver Reservas**: Lista todas las reservas del cliente
- **Ver Actividades**: Muestra actividades relacionadas
- **Nueva Reserva**: Crea una reserva pre-llenada con datos del cliente
- **Nueva Actividad**: Crea una actividad para este cliente
- **Exportar Contactos**: Descarga CSV con todos los contactos
- **Marcar como Inactivo**: Cambia categoría a Inactivo

### Buscar Clientes

**Búsqueda rápida**: El sistema busca por:
- Nombre de empresa
- Contacto principal
- Email
- Ciudad

**Filtros avanzados**:
- Por país
- Por categoría
- Por tipo de cliente
- Por empleado asignado

---

## Gestión de Reservas

### Crear una Nueva Reserva

1. Ir a **Reserva Paquete > Nuevo**

2. **Información Principal**:
   - Serie: RSV-.YYYY.- (automático)
   - Título de la reserva (descriptivo)
   - Cliente (al seleccionar, auto-completa comisión y empleado)
   - Estado: Borrador, Pendiente, Confirmada, etc.
   - Fecha de reserva (hoy por defecto)
   - Empleado responsable

3. **Destino y Fechas**:
   - Destino (ciudad/lugar)
   - País destino
   - Ciudad
   - Fecha inicio
   - Fecha fin
   - **Número de noches** - Se calcula automáticamente

4. **Información de Pasajeros**:
   - Adultos (por defecto: 2)
   - Niños
   - Bebés
   - **Total personas** - Se calcula automáticamente
   - Nacionalidad predominante

5. **Detalles del Paquete**:
   - Tipo de paquete (Solo alojamiento, Pensión completa, etc.)
   - ☑ Incluye vuelo
   - ☑ Incluye traslados
   - Hotel reservado
   - Tipo de habitación
   - Número de habitaciones

6. **Servicios Adicionales** (opcional):
   - Clic en "Agregar fila"
   - Seleccionar servicio (Excursión, Guía, Alquiler coche, etc.)
   - Descripción
   - Cantidad
   - Precio unitario
   - **Total** - Se calcula automáticamente

7. **Información Financiera**:
   - Valor paquete base (requerido)
   - **Valor servicios adicionales** - Se calcula automáticamente
   - Descuento (%)
   - **Descuento (€)** - Se calcula automáticamente
   - **Valor total** - Se calcula automáticamente
   - Comisión (%) - Traída del cliente
   - **Comisión SBC** - Se calcula automáticamente

8. **Notas y Observaciones**:
   - Requisitos especiales del cliente
   - Notas internas (no visibles para cliente)

9. Guardar

### Estados de Reserva

- **Borrador**: Reserva en creación
- **Pendiente**: Esperando confirmación
- **Confirmada**: Reserva confirmada (al hacer Submit)
- **En Proceso**: Viaje en curso
- **Completada**: Viaje finalizado
- **Cancelada**: Reserva cancelada

### Submit de Reserva

Al hacer **Submit** en una reserva:
- El estado cambia automáticamente a "Confirmada"
- Se registra la fecha de confirmación
- La reserva queda bloqueada para edición (salvo campos permitidos)

### Características Especiales

#### Cálculos Automáticos
- **Noches**: Diferencia entre fecha inicio y fin
- **Total personas**: Suma de adultos, niños y bebés
- **Servicios adicionales**: Cantidad × Precio unitario
- **Descuento**: Subtotal × Porcentaje descuento
- **Total**: (Base + Servicios) - Descuento
- **Comisión**: Total × Porcentaje comisión

#### Validaciones
- Fecha fin debe ser posterior a fecha inicio
- Advertencia si fecha inicio es anterior a fecha reserva
- Todos los cálculos se actualizan en tiempo real

#### Acciones Disponibles

**Botones en el formulario:**
- **Duplicar Reserva**: Crea una copia con nuevo ID
- **Enviar Email**: Genera email de confirmación
- **Crear Actividad**: Crea actividad vinculada a esta reserva

### Modificar Reserva Submitted

Después de Submit, solo se pueden modificar:
- Estado
- Notas internas

Para otros cambios:
1. Cancel la reserva
2. Amend (crear versión enmendada)
3. Hacer cambios
4. Submit nuevamente

---

## Actividades Comerciales

### Crear una Nueva Actividad

1. Ir a **Actividad Comercial > Nuevo**

2. **Información Principal**:
   - Serie: ACT-.YYYY.- (automático)
   - Título (descriptivo)
   - Tipo de actividad:
     - Reunión
     - Evento Asistido
     - Llamada Comercial
     - Email
     - Acción Comercial
     - Seguimiento
     - Visita Cliente
     - Feria/Congreso
   - Estado: Programada, En Curso, Completada, etc.
   - Prioridad: Baja, Media, Alta, Urgente

3. **Cliente y Fechas**:
   - Cliente (opcional)
   - Reserva relacionada (opcional)
   - Fecha y hora (requerido)
   - Duración en minutos (por defecto: 60)
   - **Fecha fin** - Se calcula automáticamente

4. **Responsables**:
   - Empleado responsable (usuario actual por defecto)
   - Otros participantes (multi-select)

5. **Ubicación** (si aplica):
   - Solo visible para Reunión, Visita Cliente, Evento
   - Ubicación (nombre del lugar)
   - Dirección
   - Enlace videollamada (si ubicación es "Virtual" u "Online")

6. **Descripción**:
   - Agenda de la actividad
   - Temas a tratar
   - Editor de texto enriquecido

7. **Resultado y Seguimiento** (después de completar):
   - Solo visible cuando estado = "Completada"
   - Resultado: Exitoso, Parcialmente exitoso, etc.
   - Notas del resultado
   - Próximos pasos
   - ☑ Crear actividad de seguimiento
   - Fecha para seguimiento

8. Guardar

### Estados de Actividad

- **Programada**: Actividad planificada
- **En Curso**: En desarrollo
- **Completada**: Finalizada
- **Cancelada**: Cancelada
- **Pospuesta**: Reprogramada

### Seguimiento Automático

Al marcar ☑ **Crear actividad de seguimiento**:
1. Sistema sugiere fecha (7 días después por defecto)
2. Al guardar con estado "Completada"
3. Se crea automáticamente nueva actividad
4. Vinculada al mismo cliente/reserva
5. Con notas del resultado actual

### Vista de Calendario

Las actividades se pueden ver en:
- **Lista**: Vista tradicional
- **Calendario**: Vista de calendario mensual
- **Gantt**: Vista de línea de tiempo

### Recordatorios Automáticos

El sistema envía **emails diarios** con:
- Actividades de hoy
- Actividades de mañana
- A cada empleado responsable

### Acciones Disponibles

**Botones en el formulario:**
- **Marcar Completada**: Cambio rápido de estado
- **Crear Seguimiento**: Genera nueva actividad de seguimiento
- **Ver Reserva**: Si hay reserva vinculada
- **Ver Cliente**: Si hay cliente vinculado
- **Enviar Recordatorio**: Email manual de recordatorio
- **Agregar a Calendario**: Exporta a Google Calendar

---

## Reportes y Análisis

### Sales by Client (Ventas por Cliente)

**Acceso**: Reportes > Sales by Client

**Filtros disponibles:**
- Fecha desde / hasta
- Categoría de cliente
- Tipo de cliente
- Empleado asignado
- País

**Información mostrada:**
- Cliente
- Tipo y categoría
- Total reservas
- Reservas completadas
- Reservas canceladas
- Valor total (€)
- Comisión total (€)
- Promedio por reserva
- Tasa de conversión (%)

**Gráfico**: Top 10 clientes por valor total

### Sales by Destination (Ventas por Destino)

**Acceso**: Reportes > Sales by Destination

**Filtros disponibles:**
- Fecha desde / hasta
- País destino
- Cliente
- Estado

**Información mostrada:**
- Destino
- País
- Total reservas
- Total personas
- Total noches
- Valor total (€)
- Comisión (€)
- Promedio por persona (€)

**Gráfico**: Top 10 destinos

### Activity Dashboard (Dashboard de Actividades)

**Acceso**: Reportes > Activity Dashboard

**Filtros disponibles:**
- Fecha desde / hasta
- Empleado responsable
- Cliente
- Tipo de actividad
- Estado
- Prioridad
- Mostrar todas (incluye pasadas)

**Resumen superior:**
- Total actividades
- Programadas
- En curso
- Completadas
- Canceladas

**Gráfico**: Distribución por tipo de actividad

### Exportar Reportes

Todos los reportes permiten:
- **Excel**: Exportar a .xlsx
- **CSV**: Exportar a .csv
- **PDF**: Generar PDF
- **Print**: Imprimir directamente

---

## Consejos y Mejores Prácticas

### Para Máxima Eficiencia

#### Al crear clientes:
1. ✅ Complete todos los campos de contacto
2. ✅ Agregue contactos adicionales desde el inicio
3. ✅ Configure la comisión estándar correcta
4. ✅ Asigne un empleado responsable

#### Al crear reservas:
1. ✅ Use títulos descriptivos ("Mallorca 7N - Hotel Sol")
2. ✅ Verifique las fechas cuidadosamente
3. ✅ Agregue todos los servicios adicionales
4. ✅ Incluya requisitos especiales del cliente
5. ✅ Submit solo cuando esté confirmada

#### Al gestionar actividades:
1. ✅ Sea específico en los títulos
2. ✅ Configure recordatorios
3. ✅ Complete resultados al finalizar
4. ✅ Use seguimientos para no perder oportunidades
5. ✅ Vincule a clientes y reservas cuando sea relevante

### Flujos de Trabajo Recomendados

#### Proceso de Venta:
```
1. Crear/Verificar Cliente
2. Primera Actividad (Llamada/Reunión)
3. Crear Reserva en estado "Borrador"
4. Actividad de seguimiento
5. Confirmar Reserva (Submit)
6. Actividades durante el proceso
7. Marcar Reserva como "Completada"
8. Actividad de satisfacción post-venta
```

#### Proceso de Seguimiento:
```
1. Actividad inicial
2. Completar actividad con resultado
3. ☑ Crear seguimiento automático
4. Recibir recordatorio 7 días después
5. Realizar seguimiento
6. Repetir según sea necesario
```

### Atajos de Teclado

- **Ctrl + K**: Búsqueda global
- **Ctrl + G**: Ir a (doctype/página)
- **Ctrl + S**: Guardar documento actual
- **Ctrl + Shift + S**: Submit documento

### Personalización

#### Agregar campos personalizados:
Customization > Custom Field > New

#### Crear reportes personalizados:
Report Builder o Query Report

#### Automatizaciones adicionales:
Server Script o Client Script

---

## Soporte

### Recursos Adicionales
- Manual de instalación: INSTALLATION_GUIDE.md
- Documentación técnica: TECHNICAL_DOCS.md

### Contacto
- Email: sbcinternational@protonmail.com
- Feedback: Use el botón de feedback en cualquier formulario

### Actualizaciones
El sistema se actualiza regularmente con:
- Nuevas funcionalidades
- Mejoras de rendimiento
- Corrección de errores

---

**Versión del documento**: 1.0  
**Última actualización**: Enero 2025  
**SBC Internationals** - Todos los derechos reservados
