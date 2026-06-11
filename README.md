# controle-remedios

Terminal application for managing patients, medicines, and medicine stock with per-entry consumption based on daily dose.

## Requirements

- Python 3.11+
- SQLAlchemy 2.x

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run

From the project root:

```bash
python -m app.main
```

## Architecture

```
app/
├── main.py
├── database.py
├── i18n/
├── models/
├── services/
├── controllers/
└── views/
```

- **Models**: SQLAlchemy ORM entities (`Patient`, `Medicine`, `StockEntry`, `Metadata`)
- **Controllers**: database operations and validation
- **Views**: terminal UI with route-based navigation
- **Services**: domain logic (stock calculation)

## Stock calculation

Each stock entry decays independently:

```
remaining = max(0, quantity - daily_dose × days_since_entry)
current_stock = sum(remaining for each entry)
```

Example: entry 60 days ago with 30 units, entry 30 days ago with 45 units, daily dose 1 unit/day → `0 + 15 = 15` units today.

## i18n

Locales live in `app/i18n/locales/` (`en.json`, `pt-br.json`). Default language is `en`, persisted in the `metadata` table. Change language from the main menu at runtime.

## Manual test checklist

1. Add a patient
2. Select the patient and add a medicine (dose + unit)
3. Add stock entries with custom dates
4. List current stock and verify decay calculation
5. Soft-delete a medicine (hidden from selection and stock list)
6. Remove a patient (hard delete with cascade)
7. Change language to `pt-br` and confirm UI updates
