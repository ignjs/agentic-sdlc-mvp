from __future__ import annotations

from pathlib import Path

from orchestrator.agents.generators.common import write_if_missing


def scaffold_react_frontend(project_root: Path) -> None:
    app_root = project_root / "apps" / "react-frontend"

    write_if_missing(
        app_root / "package.json",
        """{
  "name": "react-frontend",
  "private": true,
  "version": "0.1.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview"
  },
  "dependencies": {
    "react": "^18.3.1",
    "react-dom": "^18.3.1"
  },
  "devDependencies": {
    "@vitejs/plugin-react": "^4.3.2",
    "vite": "^5.4.2"
  }
}
""",
    )

    write_if_missing(
        app_root / "index.html",
        """<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>React Frontend</title>
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/main.jsx"></script>
  </body>
</html>
""",
    )

    write_if_missing(
        app_root / "vite.config.js",
        """import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  server: {
    host: '0.0.0.0',
    port: 5173,
  },
});
""",
    )

    write_if_missing(
        app_root / "src" / "main.jsx",
        """import React from 'react';
import { createRoot } from 'react-dom/client';
import App from './App.jsx';
import './styles.css';

createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
""",
    )

    write_if_missing(
        app_root / "src" / "App.jsx",
        """export default function App() {
  return (
    <main className="page">
      <section className="card">
        <p className="eyebrow">React Base Template</p>
        <h1>React Micro-Frontend Starter</h1>
        <p>Secure defaults, simple structure, and fast local iteration.</p>
      </section>
    </main>
  );
}
""",
    )

    write_if_missing(
        app_root / "src" / "styles.css",
        """:root {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  color: #16213e;
  background: radial-gradient(circle at top right, #dbeafe, #f8fafc 60%);
}

* {
  box-sizing: border-box;
}

body {
  margin: 0;
}

.page {
  min-height: 100vh;
  display: grid;
  place-items: center;
  padding: 2rem;
}

.card {
  width: min(720px, 92vw);
  background: #ffffff;
  border: 1px solid #d7e0ef;
  border-radius: 16px;
  padding: 2rem;
  box-shadow: 0 18px 45px rgba(22, 33, 62, 0.08);
}

.eyebrow {
  text-transform: uppercase;
  letter-spacing: 0.12em;
  font-size: 0.75rem;
  color: #3b82f6;
}
""",
    )

    write_if_missing(
        app_root / "Dockerfile",
        """FROM node:20-alpine AS build
WORKDIR /app
COPY package.json ./
RUN npm install
COPY . .
RUN npm run build

FROM nginx:1.27-alpine
COPY --from=build /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
""",
    )

    write_if_missing(
        app_root / "README.md",
        """# React Frontend Template

## Best practices included
- Vite + React baseline with fast startup.
- Dedicated src structure and isolated styles.
- Docker multi-stage build for static serving.
- Minimal, extendable UI foundation.
""",
    )