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
- `apps/template-service/`: plantilla base backend Python/FastAPI (generación por intent)
- `apps/go-microservice/`: plantilla base backend Go (generación por intent)
- `apps/springboot-microservice/`: plantilla base backend Spring Boot (generación por intent)
- `apps/react-frontend/`: plantilla base frontend React (generación por intent)
- `apps/angular-frontend/`: plantilla base frontend Angular (generación por intent)
- `apps/liquid-landing/`: plantilla base HTML/CSS estilo Liquid (generación por intent)
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

Para ejecutar controles tipo CI al final del flujo:

```bash
python -m orchestrator.main --intent intent.md --run-controls
```

### ¿Qué ejecuta `orchestrator.main`?

El comando ejecuta el flujo SDLC del MVP y devuelve un resumen JSON con resultados.

Pasos actuales del workflow:

1. Sanitización del intent de entrada.
2. Análisis de requerimientos funcionales.
3. Construcción de threat model base.
4. Generación de artefactos por activadores del intent.
5. Escaneo SAST ligero sobre `apps/template-service`.
6. Simulación red-team.
7. Construcción de plan de parcheo.

No incluido automáticamente en este comando:

- `docker compose up --build`
- scripts de `security/scripts/*`
- despliegue final de infraestructura

Controles opcionales con `--run-controls`:

1. `pytest -q`
2. `bash security/scripts/run_sast.sh`
3. `bash security/scripts/run_dependency_scan.sh`

### Resolución automática de carpeta local de proyecto

Al ejecutar el flujo con `intent.md`, el orquestador valida si la ruta de proyecto indicada existe como repo/workspace local.

- Si la ruta parece un repo válido (`.git`, `pyproject.toml` u `orchestrator/`), usa esa ruta.
- Si no existe un repo/workspace válido, crea una carpeta local ad hoc junto al intent (por ejemplo: `intent-repo/`) y genera allí los artefactos.

Puedes controlar esta validación con `--project-root`:

```bash
python -m orchestrator.main --intent intent.md --project-root /ruta/del/proyecto
```

La salida JSON del comando incluye:

- `project_root`: ruta final usada por el workflow
- `project_root_created`: `true/false` indicando si se creó carpeta ad hoc
- `execution_controls`: arreglo con resultados de controles (vacío si no se usa `--run-controls`)

Ejemplo resumido de cada control en `execution_controls`:

- `name`
- `command`
- `exit_code`
- `passed`
- `stdout`
- `stderr`

Ejemplo de salida JSON (resumida):

```json
{
	"project_root": "/Users/ignacio/projects/agentic-sdlc-mvp",
	"project_root_created": false,
	"execution_controls": [
		{
			"name": "tests",
			"command": "pytest -q",
			"exit_code": 0,
			"passed": true,
			"stdout": "3 passed in 0.36s",
			"stderr": ""
		},
		{
			"name": "sast",
			"command": "bash security/scripts/run_sast.sh",
			"exit_code": 0,
			"passed": true,
			"stdout": "...",
			"stderr": ""
		},
		{
			"name": "dependency_scan",
			"command": "bash security/scripts/run_dependency_scan.sh",
			"exit_code": 0,
			"passed": true,
			"stdout": "...",
			"stderr": ""
		}
	]
}
```

### Generación por intent de plantillas frontend

El `CodeGeneratorAgent` activa plantillas por palabras clave detectadas en el intent sanitizado.

- React: requiere `react` y alguna de estas palabras: `frontend`, `front-end`, `web`, `ui`, `landing`.
- Angular: requiere `angular` y alguna de estas palabras: `frontend`, `front-end`, `web`, `ui`, `landing`.

Ejemplo de intent para generar ambas:

```markdown
Crear frontend web con React y Angular para una portada UI.
```

Ejecución:

```bash
python -m orchestrator.main --intent intent_frontends.md
```

Salida esperada (en `project_root/apps`):

- `react-frontend/`
- `angular-frontend/`

### Generación por intent de plantillas backend y landing

- Python/FastAPI: se activa si el intent contiene `python` o `fastapi`, o bien señales de servicio como `microservicio`, `microservice`, `api`, `backend`.
- Go: requiere `go` o `golang` y además `microservicio`, `microservice` o `api`.
- Spring Boot: requiere `spring`, `springboot` o `spring boot` y además `microservicio`, `microservice` o `api`.
- HTML Liquid landing: requiere `html` + `liquid` y además `portada`, `landing` o `cover`.

### Tabla resumen de stacks y activadores

| Stack | Activador obligatorio | Activador adicional (cualquiera) | Salida generada |
|---|---|---|---|
| Python FastAPI | `python` o `fastapi` | Opcionalmente también activa por señales de servicio: `microservicio`, `microservice`, `api`, `backend` | `apps/template-service/` |
| Go microservice | `go` o `golang` | `microservicio`, `microservice`, `api` | `apps/go-microservice/` |
| Spring Boot microservice | `spring`, `springboot` o `spring boot` | `microservicio`, `microservice`, `api` | `apps/springboot-microservice/` |
| React frontend | `react` | `frontend`, `front-end`, `web`, `ui`, `landing` | `apps/react-frontend/` |
| Angular frontend | `angular` | `frontend`, `front-end`, `web`, `ui`, `landing` | `apps/angular-frontend/` |
| HTML Liquid landing | `html` + `liquid` | `portada`, `landing`, `cover` | `apps/liquid-landing/` |

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
