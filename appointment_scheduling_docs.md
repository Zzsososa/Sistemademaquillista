# Documentación de Gestión de Citas

Este documento proporciona información detallada sobre la implementación de la funcionalidad de gestión de citas en la aplicación Lucero Glam Studio.

## Características Implementadas

### Programación de Citas
- Interfaz intuitiva para seleccionar cliente, servicio, fecha y hora
- Validación de disponibilidad en tiempo real
- Cálculo automático de duración basado en el servicio seleccionado
- Opción para añadir depósito inicial
- Campo para notas adicionales

### Calendario Visual
- Vista de calendario mensual con citas marcadas
- Vista diaria con desglose por horas
- Código de colores para diferentes estados de citas (programada, completada, cancelada)
- Filtros para ver citas por cliente o tipo de servicio

### Notificaciones y Recordatorios
- Sistema de recordatorios automáticos para próximas citas
- Notificaciones de cambios en citas (reprogramación, cancelación)
- Alertas para el administrador sobre citas próximas

### Estadísticas de Citas
- Gráficos de distribución de citas por día de la semana
- Métricas clave: total de citas, citas próximas, citas en los últimos 30 días
- Información sobre servicios más solicitados
- Análisis de clientes frecuentes

## Implementación Técnica

La gestión de citas se implementa mediante las siguientes funciones principales:

```python
# Crear nueva cita
def add_appointment(client_id, service_id, appointment_date, deposit_amount, notes=""):
    # Validación de disponibilidad
    # Registro en base de datos
    # Retorno de ID de cita

# Actualizar cita existente
def update_appointment(appointment_id, client_id, service_id, appointment_date, deposit_amount, notes, status):
    # Validación de cambios
    # Actualización en base de datos

# Obtener estadísticas de citas
def get_appointment_statistics():
    # Cálculo de métricas
    # Generación de datos para gráficos
    # Análisis de tendencias
```

## Integración con Otras Funcionalidades

La gestión de citas está integrada con:
- Gestión de clientes: para seleccionar y asociar clientes a las citas
- Gestión de servicios: para seleccionar servicios y calcular duración y precios
- Facturación: para generar facturas automáticamente al completar citas

## Próximas Mejoras

- Implementación de recordatorios por SMS o email
- Opción para que los clientes programen citas online
- Sistema de calificación post-servicio
