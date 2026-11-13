from __future__ import annotations

from pathlib import Path

from orchestrator.agents.generators.common import write_if_missing


def scaffold_liquid_landing(project_root: Path) -> None:
    web_root = project_root / "apps" / "liquid-landing"

    write_if_missing(
        web_root / "index.html",
        """<!doctype html>
<html lang="es">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>Portada Liquid</title>
    <link rel="stylesheet" href="styles.css" />
  </head>
  <body>
    <main class="page">
      <section class="hero">
        <div class="liquid liquid-a"></div>
        <div class="liquid liquid-b"></div>
        <div class="hero-content">
          <p class="eyebrow">Plantilla Generica</p>
          <h1>Portada con estilo Liquid</h1>
          <p class="subtitle">Una base visual moderna para prototipos y demos de producto.</p>
          <a class="cta" href="#beneficios">Explorar</a>
        </div>
      </section>
      <section id="beneficios" class="benefits">
        <article class="card"><h2>Diseno fluido</h2><p>Composicion organica con degradados y formas suaves.</p></article>
        <article class="card"><h2>Responsive</h2><p>Visualizacion adaptada para desktop y mobile.</p></article>
        <article class="card"><h2>Extensible</h2><p>Estructura simple para evolucionar a landing completa.</p></article>
      </section>
    </main>
    <footer class="footer"><a href="#">Inicio</a><a href="#">Caracteristicas</a><a href="#">Contacto</a></footer>
  </body>
</html>
""",
    )

    write_if_missing(
        web_root / "styles.css",
        """:root { --bg: #f4f7ff; --text: #1a2440; --accent: #1e6eff; --card: rgba(255, 255, 255, 0.75); }
* { box-sizing: border-box; }
body { margin: 0; font-family: "Trebuchet MS", "Segoe UI", sans-serif; color: var(--text); background: radial-gradient(circle at 15% 20%, #d9e7ff 0, #f4f7ff 45%), radial-gradient(circle at 80% 5%, #d2ffef 0, rgba(210, 255, 239, 0) 40%); }
.page { max-width: 1080px; margin: 0 auto; padding: 2rem 1rem 3rem; }
.hero { position: relative; min-height: 48vh; border-radius: 24px; overflow: hidden; background: linear-gradient(130deg, #f7fbff 0%, #eef5ff 50%, #eefdf8 100%); box-shadow: 0 20px 40px rgba(24, 47, 102, 0.12); }
.hero-content { position: relative; z-index: 2; padding: 3rem 2rem; }
.eyebrow { text-transform: uppercase; letter-spacing: 0.12em; font-size: 0.78rem; color: #4d6db0; }
h1 { margin: 0.35rem 0 0.6rem; font-size: clamp(2rem, 6vw, 3.5rem); }
.subtitle { max-width: 42ch; line-height: 1.6; }
.cta { display: inline-block; margin-top: 1.2rem; text-decoration: none; background: var(--accent); color: #fff; padding: 0.75rem 1.2rem; border-radius: 999px; }
.liquid { position: absolute; border-radius: 58% 42% 62% 38% / 41% 47% 53% 59%; filter: blur(1px); }
.liquid-a { width: 300px; height: 300px; right: -70px; top: -30px; background: linear-gradient(180deg, rgba(40, 122, 255, 0.45), rgba(125, 240, 200, 0.55)); }
.liquid-b { width: 220px; height: 220px; right: 120px; bottom: -80px; background: linear-gradient(180deg, rgba(86, 199, 255, 0.45), rgba(30, 110, 255, 0.25)); }
.benefits { display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 1rem; margin-top: 1.5rem; }
.card { background: var(--card); border: 1px solid rgba(74, 101, 163, 0.12); border-radius: 16px; padding: 1rem; }
.footer { max-width: 1080px; margin: 0 auto 1.5rem; padding: 0 1rem; display: flex; gap: 1rem; }
.footer a { color: #33569c; text-decoration: none; }
@media (max-width: 720px) { .hero-content { padding: 2.2rem 1.2rem; } }
""",
    )
