# Daily Content API

Public REST API that delivers daily and random content entries from a large structured dataset, with search, filtering, and statistics.

---

## 🚀 Features
- Deterministic daily content delivery based on date
- Random content retrieval
- Search and filtering by structured fields
- Pagination support
- Public REST API with OpenAPI documentation
- Modular and maintainable architecture

---

## 📊 Dataset Overview
- +30,000 structured content entries
- Hierarchical organization (category → section → item)
- Preprocessed for fast lookup and filtering

---

## 🛠 Tech Stack
- Python
- FastAPI
- Pydantic
- OpenAPI / Swagger

---

## 🌍 Live API
Base URL: https://daily-phrase.onrender.com/

Documentation: /docs

---

## 📌 Core Endpoints

| Method | Endpoint            | Description                     |
|------|---------------------|---------------------------------|
| GET  | `/`                 | API overview                     |
| GET  | `/api/daily-verse`        | Deterministic daily content      |
| GET  | `/api/random-verse`       | Random content                   |
| GET  | `/api/verses?book=Genesis`        | Filtered content list            |
| GET  | `/api/verse/Genesis/1/1`   | Specific content item            |
| GET  | `/api/stats`        | Dataset statistics               |

---

## 🧠 Architecture Overview
The API loads a structured dataset into memory at startup and exposes multiple query strategies, including deterministic date-based selection and filtered search.

The design emphasizes simplicity, fast response times, and clear separation of concerns.

---

## 🧪 Local Development

```bash
# Clone repository
git clone https://github.com/your-username/daily-content-api.git
cd daily-content-api

# Install dependencies
pip install -r requirements.txt

# Run development server
fastapi dev app/main.py
