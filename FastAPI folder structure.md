fast-api/
│
├── app/
│   ├── __init__.py
│   ├── main.py              👈 Entry point for the FastAPI app
│
│   ├── routers/             🔹 Route handlers / API endpoints
│   │   ├── __init__.py
│   │   └── example.py
│
│   ├── models/              🔹 Pydantic data models (Request/Response schemas)
│   │   ├── __init__.py
│   │   └── example.py
│
│   ├── services/            🔸 Business logic layer (PUT YOUR CORE LOGIC HERE)
│   │   └── __init__.py
│
│   ├── db/                  🔹 Database connection/config & queries (ORM or raw SQL)
│   │   ├── __init__.py
│   │   └── database.py
│
│   ├── core/                🔹 Configuration, constants, settings
│   │   ├── __init__.py
│   │   └── config.py
│
│   └── utils/               🔹 Helper functions (e.g., common formatting, parsing)
│       ├── __init__.py
│       └── helpers.py
