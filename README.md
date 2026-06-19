# LLM Playwright Framework

An AI-powered test automation framework combining Playwright with Ollama LLM for intelligent test generation and failure analysis. Built against **[phptravels.net](https://phptravels.net)** — a real-world travel booking demo site similar to MakeMyTrip.

## Target Application

| Detail | Value |
|---|---|
| Site | https://phptravels.net |
| Type | Travel booking (flights, hotels, tours) |
| Demo user | user@phptravels.com / demouser |
| Demo admin | admin@phptravels.com / demoadmin |

## Project Structure

```
llm-playwright-framework/
├── tests/
│   ├── test_login.py        # Login, logout, invalid credential tests
│   ├── test_flights.py      # Flight search tests
│   ├── test_hotels.py       # Hotel search and detail tests
│   └── test_checkout.py     # Dashboard and booking tests
├── pages/
│   ├── home_page.py         # Homepage navigation
│   ├── login_page.py        # Login page POM
│   ├── flights_page.py      # Flight search POM
│   ├── hotels_page.py       # Hotel search POM
│   └── dashboard_page.py    # User account/dashboard POM
├── utils/
│   ├── llm_helper.py        # Ollama client for test gen & failure analysis
│   ├── logger.py            # File + console logger
│   └── config.py            # Env var + user data loader
├── prompts/
│   ├── test_case_generation.txt
│   └── failure_analysis.txt
├── testdata/
│   └── users.json           # Credentials per environment
├── reports/                 # HTML reports + failure screenshots
├── conftest.py
├── pytest.ini
├── requirements.txt
└── .env
```

## Setup

```bash
# 1. Install Ollama and pull a model
brew install ollama
ollama pull llama3
ollama serve

# 2. Install Python dependencies
pip install -r requirements.txt
playwright install chrome

# 3. Configure environment
cp .env .env.local
```

## Running Tests

```bash
# All tests (opens Chrome)
pytest

# Specific module
pytest tests/test_login.py
pytest tests/test_flights.py
pytest tests/test_hotels.py

# Headless mode
HEADLESS=true pytest
```

## LLM Features

### Generate Test Cases
```python
from utils.llm_helper import LLMHelper

llm = LLMHelper()
print(llm.generate_test_cases("Hotel search with check-in date validation"))
```

### Analyze Failures
```python
analysis = llm.analyze_failure("TimeoutError: locator('.hotel-item') exceeded 30000ms")
print(analysis)
```

## Environment Variables

| Variable | Description | Default |
|---|---|---|
| `OLLAMA_MODEL` | Ollama model name | `llama3` |
| `OLLAMA_HOST` | Ollama server URL | `http://localhost:11434` |
| `BASE_URL` | App base URL | `https://phptravels.net` |
| `TEST_ENV` | Credentials to load from users.json | `staging` |
| `HEADLESS` | Run browser headless | `false` |
| `SLOW_MO` | Slow down actions (ms) | `500` |
| `DEFAULT_TIMEOUT` | Playwright timeout (ms) | `30000` |
