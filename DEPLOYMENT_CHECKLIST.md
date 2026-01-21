# SBC CRM - Checklist de Despliegue

## Pre-instalación

### Requisitos del Sistema
- [ ] Frappe Framework v14+ o v15+ instalado
- [ ] Python 3.8+ disponible
- [ ] MariaDB 10.3+ configurado
- [ ] Node.js 14+ instalado
- [ ] Nginx/Apache configurado
- [ ] SSL/TLS certificados (para producción)

### Preparación del Servidor
- [ ] Memoria RAM suficiente (mínimo 2GB, recomendado 4GB+)
- [ ] Espacio en disco (mínimo 20GB libres)
- [ ] Backups automáticos configurados
- [ ] Monitoreo del servidor activo

## Instalación

### 1. Obtener la Aplicación
```bash
cd /path/to/frappe-bench
bench get-app https://github.com/tu-usuario/sbc_cr34
```
- [ ] App descargada correctamente
- [ ] Sin errores en console

### 2. Instalar en Sitio
```bash
bench --site tu-sitio.local install-app sbc_cr34
```
- [ ] Instalación completada
- [ ] Sin errores de dependencias

### 3. Migrar Base de Datos
```bash
bench --site tu-sitio.local migrate
```
- [ ] Migración exitosa
- [ ] Todos los DocTypes creados

### 4. Configuración Inicial
```bash
bench --site tu-sitio.local set-config developer_mode 0  # Para producción
bench restart
```
- [ ] Configuración aplicada
- [ ] Servicios reiniciados

## Post-instalación

### Verificación de DocTypes
- [ ] Cliente Turistico creado
- [ ] Cliente Contacto Adicional creado
- [ ] Reserva Paquete creado
- [ ] Servicio Adicional Reserva creado
- [ ] Actividad Comercial creado

### Verificación de Scripts
- [ ] cliente_turistico.py funciona
- [ ] reserva_paquete.py funciona
- [ ] actividad_comercial.py funciona
- [ ] Cliente scripts cargados (*.js)

### Verificación de Reportes
- [ ] Sales by Client disponible
- [ ] Sales by Destination disponible
- [ ] Activity Dashboard disponible
- [ ] Reportes generan datos correctamente

### Verificación de Permisos
- [ ] Rol "Sales Master Manager" existe
- [ ] Rol "Sales User" existe
- [ ] Permisos asignados correctamente
- [ ] Usuarios pueden acceder a DocTypes

## Configuración de Usuarios

### Crear Roles
- [ ] Sales Master Manager configurado
- [ ] Sales User configurado

### Asignar Usuarios
- [ ] Administradores → Sales Master Manager
- [ ] Vendedores → Sales User
- [ ] Permisos verificados por usuario

### Configurar Defaults
```python
# Para cada usuario
frappe.db.set_value("User", "user@example.com", "role_profile_name", "Sales User")
```
- [ ] Role profiles asignados
- [ ] Defaults configurados

## Configuración de Email

### SMTP Settings
- [ ] Email Account configurado
- [ ] Credenciales SMTP correctas
- [ ] Puerto correcto (587 o 465)
- [ ] TLS/SSL habilitado

### Test de Email
```bash
bench --site tu-sitio.local send-test-email usuario@dominio.com
```
- [ ] Email de prueba recibido
- [ ] Formato correcto

### Notificaciones
- [ ] Recordatorios diarios activos
- [ ] Reporte semanal configurado
- [ ] Destinatarios correctos

## Configuración de Tareas Programadas

### Verificar Scheduler
```bash
bench --site tu-sitio.local enable-scheduler
bench doctor  # Verificar que scheduler está corriendo
```
- [ ] Scheduler habilitado
- [ ] Workers corriendo

### Tareas Configuradas
- [ ] send_daily_activity_reminder
- [ ] update_client_categories
- [ ] send_weekly_sales_report
- [ ] generate_monthly_analytics

### Test de Tareas
```bash
# Ejecutar manualmente para probar
bench --site tu-sitio.local execute sbc_cr34.tasks.send_daily_activity_reminder
```
- [ ] Tareas ejecutan sin error
- [ ] Resultados esperados obtenidos

## Datos de Prueba

### Cliente de Prueba
- [ ] Crear cliente de ejemplo
- [ ] Verificar campos se guardan
- [ ] Verificar validaciones

### Reserva de Prueba
- [ ] Crear reserva de ejemplo
- [ ] Verificar cálculos automáticos
- [ ] Submit exitoso
- [ ] Estado cambia correctamente

### Actividad de Prueba
- [ ] Crear actividad de ejemplo
- [ ] Verificar seguimiento automático
- [ ] Verificar recordatorios

### Reportes con Datos
- [ ] Ejecutar cada reporte
- [ ] Verificar datos mostrados
- [ ] Verificar gráficos

## Optimización

### Performance
```bash
# Clear cache
bench --site tu-sitio.local clear-cache

# Build assets
bench build

# Optimize database
bench --site tu-sitio.local mariadb
OPTIMIZE TABLE `tabCliente Turistico`;
OPTIMIZE TABLE `tabReserva Paquete`;
```
- [ ] Cache limpiado
- [ ] Assets compilados
- [ ] Base de datos optimizada

### Indexes
- [ ] Verificar índices en campos clave
- [ ] Agregar índices si es necesario

## Seguridad

### SSL/HTTPS
- [ ] Certificado SSL instalado
- [ ] HTTPS forzado
- [ ] Redirección HTTP → HTTPS

### Passwords
- [ ] Política de contraseñas fuerte
- [ ] Cambiar password de Administrator
- [ ] 2FA habilitado (recomendado)

### Permisos de Archivos
```bash
chmod 755 apps/sbc_cr34
chown -R frappe:frappe apps/sbc_cr34
```
- [ ] Permisos correctos
- [ ] Owner correcto

### Firewall
- [ ] Solo puertos necesarios abiertos
- [ ] SSH protegido
- [ ] Fail2ban configurado

## Backup y Recuperación

### Configurar Backups Automáticos
```bash
# En crontab
0 2 * * * cd /path/to/frappe-bench && bench --site tu-sitio.local backup --with-files
```
- [ ] Backup diario configurado
- [ ] Almacenamiento externo configurado
- [ ] Retención de backups definida (30 días)

### Test de Restore
```bash
# Probar restore de backup
bench --site restore-site.local restore --with-public-files [backup-file]
```
- [ ] Restore probado y exitoso

## Monitoreo

### Logs
- [ ] Logs rotados correctamente
- [ ] Nivel de log apropiado (INFO en prod)
- [ ] Errores siendo monitoreados

### Monitoring Tools
- [ ] Uptimerobot o similar configurado
- [ ] Alertas de caída configuradas
- [ ] Métricas de performance monitoreadas

## Documentación

### Para Usuarios
- [ ] USER_GUIDE.md accesible
- [ ] Capacitación de usuarios realizada
- [ ] FAQ creado

### Para IT
- [ ] INSTALLATION_GUIDE.md disponible
- [ ] Credenciales documentadas (seguras)
- [ ] Procedimientos de emergencia documentados

## Go-Live

### Pre-lanzamiento
- [ ] Todos los tests pasados
- [ ] Usuarios capacitados
- [ ] Datos de producción migrados (si aplica)

### Lanzamiento
- [ ] Comunicado a usuarios
- [ ] Soporte disponible
- [ ] Plan de rollback preparado

### Post-lanzamiento
- [ ] Monitorear primeras 24 horas
- [ ] Recopilar feedback de usuarios
- [ ] Resolver issues críticos inmediatamente

## Mantenimiento Continuo

### Semanal
- [ ] Revisar logs de errores
- [ ] Verificar backups
- [ ] Monitorear espacio en disco

### Mensual
- [ ] Actualizar dependencias
- [ ] Revisar performance
- [ ] Optimizar base de datos

### Trimestral
- [ ] Revisar seguridad
- [ ] Actualizar documentación
- [ ] Planear nuevas features

## Contactos de Soporte

### Técnico
- **Email**: admin@tuempresa.com
- **Teléfono**: +XX XXX XXX XXX
- **On-call**: [Número de emergencia]

### Proveedor
- **Email**: sbcinternational@protonmail.com
- **Soporte**: [URL del sistema de tickets]

## Notas Finales

### URLs Importantes
- **Producción**: https://tu-sitio.com
- **Staging**: https://staging.tu-sitio.com (si aplica)
- **Documentación**: https://docs.tu-sitio.com

### Credenciales (Guardar de forma segura)
- Ubicación: [Sistema de gestión de contraseñas]
- Última actualización: [Fecha]

---

**Checklist completado por**: _______________  
**Fecha**: _______________  
**Firma**: _______________

**Aprobado por**: _______________  
**Fecha**: _______________  
**Firma**: _______________
