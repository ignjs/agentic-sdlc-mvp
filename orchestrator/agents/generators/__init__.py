from orchestrator.agents.generators.angular_template import scaffold_angular_frontend
from orchestrator.agents.generators.go_template import scaffold_go_microservice
from orchestrator.agents.generators.liquid_template import scaffold_liquid_landing
from orchestrator.agents.generators.python_template import scaffold_python_microservice
from orchestrator.agents.generators.react_template import scaffold_react_frontend
from orchestrator.agents.generators.spring_template import scaffold_spring_boot_microservice

__all__ = [
    "scaffold_angular_frontend",
    "scaffold_go_microservice",
    "scaffold_liquid_landing",
    "scaffold_python_microservice",
    "scaffold_react_frontend",
    "scaffold_spring_boot_microservice",
]
