# Petpal — Presentation Content

## Slide 1 — Title

**Petpal: Smart Pet Care Management Platform**

Centralising pet health, daily-care routines, reminders, and trusted pet-care knowledge in one easy-to-use dashboard.

**Presented by:** [Your Name]  
**Project:** Petpal  
**Date:** [Presentation Date]

---

## Slide 2 — Problem Statement

Pet owners often manage vaccination dates, medication schedules, feeding routines, exercise, grooming, medical history, and veterinary appointments through separate apps, paper records, messages, or memory. This fragmented approach makes it easy to miss important care tasks, lose medical information, and make decisions without quick access to reliable pet-care guidance.

There is a need for a simple, centralised platform that helps owners track a pet's daily routine and health information while providing a searchable knowledge base and conversational assistance.

---

## Slide 3 — Proposed Solution

Petpal is a web-based pet-care dashboard designed to give pet owners one view of their pet's well-being.

- Displays pet profile information and health status.
- Tracks daily activities such as walks, meals, water intake, playtime, and medication.
- Shows upcoming vaccinations, grooming sessions, health check-ups, and other events.
- Stores and searches pet-care knowledge records through a secure API.
- Integrates an IBM Watson Orchestrate chat widget for conversational support.

---

## Slide 4 — Objectives

- Reduce missed pet-care activities and appointments.
- Make daily health and routine information easy to understand.
- Maintain a searchable source of pet-care knowledge.
- Provide a foundation for personalised reminders and AI-assisted support.
- Build a lightweight system that is easy to develop, test, and extend.

---

## Slide 5 — Key Features

- Pet profile: breed, age, sex, weight, veterinarian, and care tags.
- Daily dashboard: walks, meals, hydration, medication, and playtime progress.
- Event monitoring: vaccinations, grooming, check-ups, treatments, and meetups.
- Alerts: checklist-style reminders for time-sensitive care tasks.
- Health tracker: visual progress indicators and vaccination status.
- Knowledge API: create, list, and search pet-care information.
- Chat assistant: IBM Watson Orchestrate widget embedded in the dashboard.

---

## Slide 6 — System Architecture

```text
                         ┌───────────────────────────┐
                         │        Pet Owner          │
                         │     Web Browser/User      │
                         └─────────────┬─────────────┘
                                       │ HTTPS
              ┌────────────────────────┴────────────────────────┐
              │                                                 │
┌─────────────▼─────────────┐                     ┌─────────────▼─────────────┐
│  Petpal Dashboard          │                     │ IBM Watson Orchestrate    │
│  index.html                │                     │ Chat Widget / Agent       │
│  HTML + CSS + JavaScript   │                     └───────────────────────────┘
└─────────────┬─────────────┘
              │ HTTP / JSON API
┌─────────────▼─────────────┐
│  Petpal Python Server      │
│  server.py                 │
│  - Static-page delivery    │
│  - API-key validation      │
│  - Knowledge API routes    │
└─────────────┬─────────────┘
              │ Python function calls
┌─────────────▼─────────────┐
│  Knowledge Service         │
│  knowledge_api.py          │
│  - Create/list/search      │
│  - Database initialisation │
└─────────────┬─────────────┘
              │ SQLite queries
┌─────────────▼─────────────┐
│  SQLite Database           │
│  petpal.db                 │
│  knowledge_items table     │
└───────────────────────────┘
```

**Architecture explanation:** The browser loads the Petpal dashboard from the Python server. The server exposes authenticated JSON endpoints for knowledge records and delegates data operations to the knowledge service. The knowledge service stores data locally in SQLite. The dashboard also loads the IBM Watson Orchestrate chat widget for AI-assisted conversations.

---

## Slide 7 — Technology Stack

| Layer | Technology | Purpose |
|---|---|---|
| User interface | HTML, CSS, JavaScript | Responsive dashboard and client-side interactions |
| Backend | Python standard library | HTTP server and REST-style API routes |
| Data layer | SQLite | Local persistence for knowledge records |
| Authentication | API key (`X-API-Key`) | Protects API endpoints in the prototype |
| AI integration | IBM Watson Orchestrate | Conversational pet-care assistance |
| Public demonstration | ngrok or HTTPS tunnel | Optional secure external access during development |

---

## Slide 8 — API Workflow

```text
1. Client sends a request to /api/knowledge.
2. Python server validates the X-API-Key header.
3. Server selects the requested operation:
   - GET: list records or search by query
   - POST: validate and create a knowledge record
4. knowledge_api.py executes parameterised SQLite queries.
5. Server returns a JSON response to the client.
```

Example endpoints:

- `GET /api/health` — service and database status.
- `GET /api/knowledge?query=vaccination` — search knowledge records.
- `POST /api/knowledge` — create a knowledge record.

---

## Slide 9 — Current Development Status

Completed:

- Dashboard user interface and visual health tracker.
- SQLite schema creation and default knowledge seeding.
- Knowledge create, list, and search operations.
- API-key validation.
- Unit tests for database search and API-key logic.
- IBM chat-widget integration.

Current prototype limitations:

- Dashboard data is currently static and not yet connected to the API.
- Knowledge records do not yet support update or delete operations.
- The standard-library server and SQLite storage are intended for development, not production scale.

---

## Slide 10 — Security and Reliability Considerations

- Store secrets in a secret manager or uncommitted local environment files.
- Rotate any credential that has been exposed.
- Use strong API keys and HTTPS for all public access.
- Restrict CORS to approved frontend domains.
- Validate request size, field types, and pagination limits.
- Add request logging, rate limiting, backups, and monitoring.
- Use managed authentication and a production database before real-user deployment.

---

## Slide 11 — Future Enhancements

- Connect dashboard cards, events, and alerts to persistent API data.
- Add user accounts, multiple pets, roles, and pet ownership controls.
- Add CRUD operations for health records, events, medications, and reminders.
- Send push, email, or SMS reminders for vaccinations and medication.
- Add photo uploads, vet documents, and medical-history timelines.
- Introduce full-text search and AI-grounded answers based on approved knowledge.
- Deploy with a production web server, managed database, CI/CD, and observability.

---

## Slide 12 — Conclusion

Petpal demonstrates how a simple dashboard, structured pet-care data, and conversational AI can be combined to support responsible pet ownership. The current prototype establishes the core user experience and knowledge-service foundation, with a clear path toward a secure, multi-user, production-ready pet-care platform.

**Thank You**

Questions?
