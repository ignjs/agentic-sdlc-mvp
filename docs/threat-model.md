# Threat Model

## Activos
- Repositorio de código
- Intento del usuario
- Configuración de entorno
- Secretos y credenciales
- API generada

## Amenazas
- Prompt injection
- Inyección de comandos o SQL
- Fuga de secretos
- Control de acceso débil
- Archivos no validados

## Mitigaciones
- Sanitización de entradas
- Validación de modelos Pydantic
- Políticas de allowlist/denylist
- Escaneo estático y container scanning
- Revisión manual de cambios críticos
