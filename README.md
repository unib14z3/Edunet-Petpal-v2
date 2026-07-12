# Petpal
Database will not work upon hosting because it was setup using ngrok tunnel and is unique to every localhost 

Petpal is a prototype pet-care dashboard with a lightweight knowledge API. The dashboard presents a pet's daily care information, while the API stores and searches pet-care knowledge records in SQLite.

## Features

- Static pet-owner dashboard for events, health, nutrition, and daily alerts.
- SQLite-backed knowledge base with starter pet-care records.
- JSON API for health checks, listing/searching knowledge, and adding records.
- Optional API-key protection using the `X-API-Key` request header.
- IBM Watson Orchestrate chat-widget configuration in the dashboard.

## Technology

- Python 3.10 or later (only standard-library modules are used)
- SQLite
- HTML, CSS, and vanilla JavaScript

## Project structure

```text
.
├── index.html                 # Static Petpal dashboard
├── server.py                  # HTTP server and API routes
├── knowledge_api.py           # SQLite access and knowledge operations
├── database.env               # Local server configuration (do not commit secrets)
├── ibm-credentials.env        # Local IBM configuration (do not commit secrets)
└── tests/
    └── test_knowledge_api.py  # Knowledge API tests
```

## Security first

This project must not store real credentials in version control. If a secret has been added to an environment file or shared publicly, revoke and rotate it immediately.

Before running the application:

1. Set `PETPAL_API_KEY` to a long, random value.
2. Keep `database.env` and `ibm-credentials.env` local to your machine.
3. Add environment files, `petpal.db`, and `.venv/` to `.gitignore` before publishing the project.
4. Use HTTPS and restrict CORS to trusted origins before exposing the API publicly.

## Setup

Clone the project, then create a local `database.env` file:

```env
PETPAL_DB_PATH=petpal.db
PETPAL_HOST=0.0.0.0
PETPAL_PORT=8080
PETPAL_API_KEY=replace-with-a-long-random-secret
```

Start the server from the project root:

```bash
python server.py
```

The server creates the SQLite database and adds starter knowledge items on its first run. Open the dashboard at:

```text
http://localhost:8080/
```

## API

All `/api/` routes require the `X-API-Key` header when `PETPAL_API_KEY` is set.

### Check service health

```bash
curl -H "X-API-Key: $PETPAL_API_KEY" \
  http://localhost:8080/api/health
```

Example response:

```json
{
  "database": "petpal.db",
  "records": 3,
  "status": "ready"
}
```

### List knowledge items

```bash
curl -H "X-API-Key: $PETPAL_API_KEY" \
  "http://localhost:8080/api/knowledge?limit=10"
```

### Search knowledge items

```bash
curl -H "X-API-Key: $PETPAL_API_KEY" \
  "http://localhost:8080/api/knowledge?query=vaccination"
```

### Create a knowledge item

```bash
curl -X POST http://localhost:8080/api/knowledge \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $PETPAL_API_KEY" \
  --data '{
    "title": "Vaccination schedule",
    "content": "Follow a vaccination plan provided by a qualified veterinarian.",
    "tags": "health,vaccines",
    "source": "manual"
  }'
```

The `title` and `content` fields are required. `tags` and `source` are optional.

## Tests

Run the tests with explicit discovery:

```bash
python -m unittest discover -s tests -v
```

## Development notes

- The dashboard currently uses sample data and is not yet connected to the knowledge API.
- `knowledge_api.py` uses parameterized SQLite queries and initializes the schema automatically.
- The service is intended for local development and demonstrations. For production, use a managed database, a production-grade web server, authentication with proper identity management, request validation, rate limiting, logging, backups, and restricted CORS.
- If using a tunnel such as ngrok, ensure that it forwards to the same port as `PETPAL_PORT` or to a verified reverse proxy.

## IBM Watson Orchestrate

The dashboard loads the Watson Orchestrate chat widget through configuration embedded in `index.html`. Keep any IBM API keys in a local secret manager or non-committed environment file. Do not place private keys in frontend code, because browser-delivered code is public.

## License

No license has been specified for this project yet. Add a license file before distributing or open-sourcing it.
