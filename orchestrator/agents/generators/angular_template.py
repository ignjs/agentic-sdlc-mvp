from __future__ import annotations

from pathlib import Path

from orchestrator.agents.generators.common import write_if_missing


def scaffold_angular_frontend(project_root: Path) -> None:
    app_root = project_root / "apps" / "angular-frontend"

    write_if_missing(
        app_root / "package.json",
        """{
  "name": "angular-frontend",
  "private": true,
  "version": "0.1.0",
  "scripts": {
    "start": "ng serve --host 0.0.0.0 --port 4200",
    "build": "ng build"
  },
  "dependencies": {
    "@angular/animations": "^18.2.4",
    "@angular/common": "^18.2.4",
    "@angular/compiler": "^18.2.4",
    "@angular/core": "^18.2.4",
    "@angular/forms": "^18.2.4",
    "@angular/platform-browser": "^18.2.4",
    "@angular/platform-browser-dynamic": "^18.2.4",
    "@angular/router": "^18.2.4",
    "rxjs": "^7.8.1",
    "zone.js": "^0.14.8"
  },
  "devDependencies": {
    "@angular-devkit/build-angular": "^18.2.4",
    "@angular/cli": "^18.2.4",
    "@angular/compiler-cli": "^18.2.4",
    "typescript": "^5.5.4"
  }
}
""",
    )

    write_if_missing(
        app_root / "angular.json",
        """{
  "$schema": "./node_modules/@angular/cli/lib/config/schema.json",
  "version": 1,
  "projects": {
    "angular-frontend": {
      "projectType": "application",
      "root": "",
      "sourceRoot": "src",
      "architect": {
        "build": {
          "builder": "@angular-devkit/build-angular:application",
          "options": {
            "outputPath": "dist/angular-frontend",
            "index": "src/index.html",
            "browser": "src/main.ts",
            "polyfills": ["zone.js"],
            "tsConfig": "tsconfig.app.json",
            "styles": ["src/styles.css"],
            "assets": ["src/assets"]
          }
        },
        "serve": {
          "builder": "@angular-devkit/build-angular:dev-server",
          "options": {
            "buildTarget": "angular-frontend:build"
          }
        }
      }
    }
  }
}
""",
    )

    write_if_missing(
        app_root / "tsconfig.json",
        """{
  "compilerOptions": {
    "target": "ES2022",
    "module": "ES2022",
    "moduleResolution": "bundler",
    "strict": true,
    "skipLibCheck": true,
    "baseUrl": "./"
  }
}
""",
    )

    write_if_missing(
        app_root / "tsconfig.app.json",
        """{
  "extends": "./tsconfig.json",
  "compilerOptions": {
    "types": []
  },
  "files": ["src/main.ts"],
  "include": ["src/**/*.d.ts"]
}
""",
    )

    write_if_missing(
        app_root / "src" / "index.html",
        """<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>Angular Frontend</title>
  </head>
  <body>
    <app-root></app-root>
  </body>
</html>
""",
    )

    write_if_missing(
        app_root / "src" / "main.ts",
        """import { bootstrapApplication } from '@angular/platform-browser';
import { Component } from '@angular/core';

@Component({
  selector: 'app-root',
  standalone: true,
  template: `
    <main class="page">
      <section class="card">
        <p class="eyebrow">Angular Base Template</p>
        <h1>Angular Frontend Starter</h1>
        <p>Secure defaults, clean structure, and modern Angular baseline.</p>
      </section>
    </main>
  `,
})
class AppComponent {}

bootstrapApplication(AppComponent).catch((err) => console.error(err));
""",
    )

    write_if_missing(
        app_root / "src" / "styles.css",
        """:root {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  color: #172554;
  background: radial-gradient(circle at 20% 0%, #e0e7ff 0%, #f8fafc 60%);
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
  border: 1px solid #d5dffd;
  border-radius: 16px;
  padding: 2rem;
  box-shadow: 0 18px 45px rgba(23, 37, 84, 0.08);
}

.eyebrow {
  text-transform: uppercase;
  letter-spacing: 0.12em;
  font-size: 0.75rem;
  color: #4f46e5;
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
COPY --from=build /app/dist/angular-frontend/browser /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
""",
    )

    write_if_missing(
        app_root / "README.md",
        """# Angular Frontend Template

## Best practices included
- Angular standalone bootstrap for simple startup.
- Strict TypeScript configuration.
- Clear app structure and isolated global styles.
- Docker multi-stage build for production static delivery.
""",
    )