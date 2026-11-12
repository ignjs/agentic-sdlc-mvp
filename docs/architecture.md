# Arquitectura del MVP

El proyecto se compone de cuatro bloques principales:

1. Orquestador de agentes
2. Validación de entrada y guardrails de seguridad
3. Aplicación de ejemplo segura
4. Pipelines de validación y escaneo

## Orquestador

El motor principal se encuentra en `orchestrator/` y coordina la ejecución de agentes especializados.

## Guardrails

Se realiza sanitización de intent.md antes de ejecutar los agentes para impedir prompt injection y payloads maliciosos.

## Aplicación

La aplicación ejemplo es una API FastAPI, ejecutada con Docker Compose y pensada para simular un entorno de entrega segura.

## CI/CD

Los scripts de seguridad se ejecutan como pasos del pipeline, bloqueando la entrega si la severidad crítica excede el threshold configurado.
