# QA Automation Project

Real-time QA automation testing with Flask, Playwright & Dashboard

## Quick Start (3 Terminals)

Terminal 1:
```bash
python app.py
```

Terminal 2:
```bash
python dashboard.py
```

Terminal 3:
```bash
rm -rf allure-results && mkdir allure-results
pytest test_full_app.py test_claude_v2.py test_advanced_working.py -v --alluredir=allure-results
```

Watch: http://localhost:5002

## Tests: 30/30 ✅

- test_full_app.py: 15 tests
- test_claude_v2.py: 5 tests
- test_advanced_working.py: 10 tests

## Stack

Flask | Playwright | Pytest | Allure | GitHub

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Create `.env`:
## API

- POST /api/register
- POST /api/login
- GET /api/products
- GET /api/cart/<user_id>
- POST /api/cart
- DELETE /api/cart/<item_id>
- POST /api/checkout/<user_id>

## Dashboard

- Real-time stats
- Pass/Fail filters
- 5s auto-refresh
- Flat design

Author: Baruh Shakarov
