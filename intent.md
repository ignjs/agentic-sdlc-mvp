# Intento del Proyecto

## Objetivo
Crear una API segura para gestionar usuarios y documentos con autenticación, validación de entrada y auditoría.

## Requisitos funcionales
- Registro y autenticación de usuarios
- Listado y visualización de documentos
- Control de acceso por rol
- Registro de eventos de auditoría
- API REST con validación Pydantic

## Restricciones
- Debe usar Python y FastAPI
- Debe ser ejecutable con Docker Compose
- Debe evitar secret leakage y uso inseguro de archivos
- Debe incluir pruebas de seguridad

## Consideraciones de seguridad
- Proteger rutas de acceso por rol
- Validar entradas y longitud de archivos
- Evitar SQL injection y XSS
- Manejar errores sin exponer trazas sensibles

## Suposiciones
- Los usuarios se autentican con token JWT
- Los archivos no pueden superar 10 MB
- El almacenamiento de documentos es local en un directorio seguro
