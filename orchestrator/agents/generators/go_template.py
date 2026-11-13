from __future__ import annotations

from pathlib import Path

from orchestrator.agents.generators.common import write_if_missing


def scaffold_go_microservice(project_root: Path) -> None:
    service_root = project_root / "apps" / "go-microservice"

    write_if_missing(
        service_root / "go.mod",
        """module github.com/example/go-microservice

go 1.22
""",
    )

    write_if_missing(
        service_root / "cmd" / "service" / "main.go",
        """package main

import (
    "context"
    "log"
    "net/http"
    "os"
    "os/signal"
    "syscall"
    "time"
)

func main() {
    mux := http.NewServeMux()
    mux.HandleFunc("/healthz", func(w http.ResponseWriter, r *http.Request) {
        w.Header().Set("Content-Type", "application/json")
        _, _ = w.Write([]byte(`{"status":"ok"}`))
    })

    server := &http.Server{
        Addr:              ":8080",
        Handler:           mux,
        ReadTimeout:       5 * time.Second,
        ReadHeaderTimeout: 3 * time.Second,
        WriteTimeout:      10 * time.Second,
        IdleTimeout:       30 * time.Second,
    }

    go func() {
        log.Println("go-microservice listening on :8080")
        if err := server.ListenAndServe(); err != nil && err != http.ErrServerClosed {
            log.Fatalf("server error: %v", err)
        }
    }()

    quit := make(chan os.Signal, 1)
    signal.Notify(quit, syscall.SIGINT, syscall.SIGTERM)
    <-quit

    ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
    defer cancel()

    if err := server.Shutdown(ctx); err != nil {
        log.Printf("shutdown error: %v", err)
    }
}
""",
    )

    write_if_missing(
        service_root / "Dockerfile",
        """FROM golang:1.22-alpine AS build
WORKDIR /src
COPY go.mod ./
RUN go mod download
COPY . .
RUN CGO_ENABLED=0 GOOS=linux GOARCH=amd64 go build -o service ./cmd/service

FROM gcr.io/distroless/static-debian12
WORKDIR /app
COPY --from=build /src/service ./service
EXPOSE 8080
USER nonroot:nonroot
ENTRYPOINT ["/app/service"]
""",
    )

    write_if_missing(
        service_root / "README.md",
        """# Go Microservice Template

## Best practices included
- `/healthz` endpoint for liveness/readiness.
- Server timeouts enabled to mitigate slowloris.
- Graceful shutdown on SIGTERM/SIGINT.
- Multi-stage Docker build with distroless runtime.
""",
    )
