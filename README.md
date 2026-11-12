# SDLC Agéntico Seguro

Este proyecto implementa un MVP de SDLC agéntico con seguridad integrada, siguiendo una arquitectura agnóstica, abierta y portable. El objetivo es combinar orquestación de agentes, validación de riesgos, generación segura de código, análisis estático, pruebas automatizadas y auditoría ética previa al despliegue.

## Objetivo

Crear un flujo de delivery de software en el que cada fase es validada por agentes especializados, con reglas de seguridad y control de calidad que impidan la entrega de artefactos vulnerables.

## Fases cubiertas

1. Especificación y modelado de amenazas
2. Generación segura de código
3. Validación, SAST y testing guiado por agentes
4. Hacking ético autónomo en entorno aislado
5. Integración, parcheo y despliegue seguro

## Estructura principal

- `orchestrator/`: motor de orquestación y micro-agentes
- `apps/template-service/`: ejemplo de aplicación segura generada
- `security/`: reglas, scripts y políticas de seguridad
- `docs/`: documentación de arquitectura y ejecución
- `docker-compose.yml`: despliegue del entorno base

## Inicio rápido

```bash
cd /Users/ignacio/projects/agentic-sdlc-mvp
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
python -m orchestrator.main --intent intent.md
```

## Ejecutar la infraestructura local

```bash
cd /Users/ignacio/projects/agentic-sdlc-mvp
docker compose up --build
```

## Validaciones de seguridad

```bash
bash security/scripts/run_sast.sh
bash security/scripts/run_dependency_scan.sh
bash security/scripts/run_fuzz.sh
```

## Principios de diseño

- Open source first
- Sin vendor lock-in
- Docker como entorno de ejecución
- Validación de entrada anti-prompt injection
- Sandboxing para auditoría ofensiva
- Artefactos y reportes trazables

## Criterios de éxito del MVP

- 0 vulnerabilidades críticas en el artefacto final
- 100% de entradas sanitizadas
- 80%+ de cobertura en tests clave
- Pipelines bloqueados ante severidades críticas
- Generación de código segura con validación de riesgos

## Licencia

MIT
