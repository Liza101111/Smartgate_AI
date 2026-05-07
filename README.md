# SmartGate AI Backend

AI backend for SmartGate heat pump monitoring. Listens for questions over MQTT, fetches the latest heat pump status from the database, and returns a natural language answer via the Groq LLM.

## Project structure

```
smartgate/
├── ai_tools/
│   ├── ai_client.py        # Groq LLM wrapper
│   ├── db.py               # MariaDB connection
│   ├── heatpump_mapping.py # Full number → heatpump ID
│   └── status_tool.py      # Fetch latest heatpump_status row
├── mqtt_services/
│   └── mqtt_ai_service.py  # MQTT listener and AI responder
├── prompts/
│   └── system_prompt.txt   # System prompt with SmartGate domain rules
├── tests/
│   ├── test_db.py          # Test database connection
│   ├── test_grop.py        # Test Groq AI client
│   └── test_ai_status.py   # Test full AI status flow
├── config.env              # Environment variables 
└── pyproject.toml          # Editable install config
```

## Setup

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install -e .
```

Copy and fill in `config.env`:

```env
GROQ_API_KEY=
DB_HOST=
DB_PORT=
DB_USER=
DB_PASSWORD=
DB_NAME=
MQTT_HOST=
MQTT_PORT=
```

## Running

```bash
python mqtt_services/mqtt_ai_service.py
```

## MQTT topics

| Topic | Direction | Description |
|-------|-----------|-------------|
| `sct/heatpump/{full_number}/ai/question` | Subscribe | Incoming user question |
| `sct/heatpump/{full_number}/ai/answer`   | Publish   | AI response |

`full_number` is the SmartGate unit identifier, e.g. `EST_001`.

## Testing

```bash
python tests/test_db.py
python tests/test_ai_status.py
```
