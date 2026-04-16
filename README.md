# Document Intelligence API

Extract structured data from business documents in seconds.

Upload a PDF → specify document type → get back clean JSON.

Supports **contracts** and **invoices**. More document types coming soon.

## Quick start

```bash
# Extract from a contract
curl -X POST https://your-url.onrender.com/extract?document_type=contract \
  -H "X-API-Key: your_api_key" \
  -F "file=@contract.pdf"

# Extract from an invoice
curl -X POST https://your-url.onrender.com/extract?document_type=invoice \
  -H "X-API-Key: your_api_key" \
  -F "file=@invoice.pdf"
```

## Contract response example

```json
{
  "id": "b6704b6d-...",
  "document_type": "contract",
  "result": {
    "parties": ["Acme Technologies s.r.o.", "DevPro Solutions s.r.o."],
    "contract_value": "1,500 EUR/week",
    "start_date": "2026-03-01",
    "end_date": "2027-02-28",
    "payment_terms": "Monthly invoicing, Net 30 days",
    "governing_law": "Czech Republic",
    "orders": [
      {
        "order_number": "WO-2026-001",
        "client": "Acme Technologies s.r.o.",
        "role": "Senior Backend Developer",
        "rate": "1,500 EUR/week",
        "start_date": "2026-03-01",
        "end_date": "2026-08-31",
        "payment_terms": "Monthly invoicing, Net 30 days",
        "location": "Remote / Prague office"
      }
    ],
    "risk_flags": [
      "Penalty of 50,000 EUR for unauthorized disclosure.",
      "IP ownership transfers to Client upon payment."
    ]
  }
}
```

## Invoice response example

```json
{
  "id": "a1b2c3d4-...",
  "document_type": "invoice",
  "result": {
    "invoice_number": "INV-2026-042",
    "issue_date": "2026-03-01",
    "due_date": "2026-03-31",
    "supplier": {
      "name": "DevPro Solutions s.r.o.",
      "address": "Narodni 15, 110 00 Prague 1",
      "company_id": "87654321",
      "vat_id": "CZ87654321",
      "iban": "CZ65 0800 0000 1920 0014 5399"
    },
    "client": {
      "name": "Acme Technologies s.r.o.",
      "address": "Wenceslas Square 1, 110 00 Prague 1",
      "company_id": "12345678",
      "vat_id": "CZ12345678"
    },
    "line_items": [
      {
        "description": "Backend development — March 2026",
        "quantity": "4",
        "unit": "weeks",
        "unit_price": "1,500 EUR",
        "total": "6,000 EUR"
      }
    ],
    "subtotal": "6,000 EUR",
    "vat_rate": "21%",
    "vat_amount": "1,260 EUR",
    "total_amount": "7,260 EUR",
    "currency": "EUR",
    "payment_method": "bank transfer",
    "variable_symbol": "20260042",
    "notes": null,
    "flags": []
  }
}
```

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/extract?document_type=contract` | Extract from contract PDF |
| `POST` | `/extract?document_type=invoice` | Extract from invoice PDF |
| `GET` | `/result/{id}` | Retrieve past extraction by ID |
| `GET` | `/health` | Health check |

## Authentication

```
X-API-Key: your_api_key
```

## Supported document types

| Type | Description |
|------|-------------|
| `contract` | Service agreements, framework contracts, work orders |
| `invoice` | Tax invoices, pro-forma invoices, credit notes |

## Run locally

```bash
cp .env.example .env
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Run with Docker

```bash
docker build -t document-api .
docker run -p 8000:8000 \
  -e OPENAI_API_KEY=your_key \
  -e DATABASE_URL=your_db_url \
  document-api
```

## Stack

- [FastAPI](https://fastapi.tiangolo.com/)
- [PyMuPDF](https://pymupdf.readthedocs.io/)
- [OpenAI GPT-4o](https://platform.openai.com/docs/)
- [PostgreSQL / Neon](https://neon.tech/)
- Docker + Render

## Known limitations

- Scanned PDFs (image-based) are not supported — text layer required.
- Handwritten invoices are not supported.
