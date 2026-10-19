# playwright

FastAPI + Playwright (Chromium) service. Renders HTML to PNG/PDF. Other services call it over HTTP.

## Endpoints

| Method | Path | Body | Returns |
| :--- | :--- | :--- | :--- |
| GET | `/health` | - | `{"status": "ok"}` |
| POST | `/render` | `{"html": str, "format": "png"\|"pdf", "width": 1200, "height": 800, "full_page": true}` | image/png or application/pdf |

## Getting started (local)

```bash
docker network create traefik-network
cd playwright
docker compose up --build
```

- From host: `http://localhost:8100` (host port 8100, bound to 127.0.0.1; 8000 is used by telegram compose)

## Quick check from other containers in network

```bash
curl localhost:8100/health
curl -X POST localhost:8100/render -H 'content-type: application/json' \
  -d '{"html":"<h1 style=\"color:red\">Napitki</h1>"}' -o out.png
```

## Notes

- Pinned `playwright==1.64.0` must match image tag `v1.64.0-noble`.
- Service has no auth. Do NOT publish via Traefik. Keep internal on `traefik-network` with no router labels, no host ports.
- Each request launches a new browser (simple, ~1s overhead). Reuse one browser in app lifespan if volume grows.
