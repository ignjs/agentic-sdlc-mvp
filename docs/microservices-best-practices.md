# Buenas Practicas para Plantillas de Microservicios

## Transversales
- Exponer `healthz` para probes de liveness/readiness.
- Definir timeouts de red y limites de entrada desde el inicio.
- Ejecutar contenedores como usuario no root.
- Externalizar configuracion por variables de entorno.
- Centralizar logs estructurados y evitar secretos en logs.
- Incluir una capa minima de validacion de entrada y tests base.

## Spring Boot
- Usar Java LTS (21) y Spring Boot 3.
- Habilitar Actuator para health/info.
- Mantener separacion por capas (controller/service/repository) al escalar.
- Activar validacion con Bean Validation.
- Aislar configuracion por perfiles (`dev`, `prod`).

## Python (FastAPI)
- Modelar contratos con Pydantic.
- Mantener dependencias de seguridad por endpoint.
- Añadir tests de smoke y auth al scaffold.
- Mantener contenedor minimalista y sin privilegios.
- Separar settings/configuracion del codigo de dominio.

## Go
- Aplicar `http.Server` con `ReadTimeout`, `WriteTimeout` e `IdleTimeout`.
- Implementar shutdown graceful por senales.
- Preferir binario estatico y runtime distroless en Docker.
- Organizar por `cmd/` e `internal/` para encapsular dominio.
- Mantener handlers pequenos y sin logica de negocio pesada.
