# invoice-ia-extractor
🤖 AI-powered pipeline that extracts structured data from energy-invoice PDFs into Excel. Built with Streamlit, LangChain + OpenAI (JSON mode), LLMWhisperer for OCR, Pydantic v2 for validation, and tenacity for resilient API calls. Parallel batch processing with cost &amp; token metrics.

## 🎯 What it does

**Invoice AI Extractor** automates a tedious manual process: reading dozens of energy-invoice PDFs (different layouts, formats, vendors) and copy-pasting every field into a spreadsheet.

Just upload your PDFs and download a clean Excel with:

- 📊 **Customer information** — NIS, name, address, sector
- 💸 **Invoice data** — number, dates, meter readings
- ⚡ **Energy charges** — generation, transmission, distribution
- 🧾 **Billing concepts** — fixed charges, energy, interest, subsidies
- 📈 **Consumption history** — monthly breakdown
- 💰 **Totals** — current period, grand total, outstanding balances

> ⏱️ **Real-world impact:** what used to take **~10 minutes per invoice** manually now takes **~15 seconds** — fully automated, with parallel processing for batches of 20+ files.

---

## ✨ Features

| Feature | How |
|---|---|
| 🤖 **Guaranteed JSON output** | OpenAI **JSON mode** (`response_format`) — no more flaky regex or markdown stripping |
| ✅ **Schema-validated extraction** | **Pydantic v2** models normalize European number formats (`"1.549,19"` → `1549.19`), currency prefixes (`B/.`, `$`, `€`), and missing fields |
| 🔁 **Resilient API calls** | **Tenacity** retries with exponential backoff — handles transient `429`, `5xx`, and timeout errors gracefully |
| 🚀 **Parallel batch processing** | `ThreadPoolExecutor` processes multiple PDFs concurrently with configurable workers |
| 💰 **Live cost telemetry** | Real-time tracking of tokens consumed and estimated USD cost per batch |
| 🖥️ **Beautiful UI** | Streamlit interface with progress bars, metrics, and per-file debug view |
| 🧪 **Unit tested** | 18 tests covering number parsing, JSON cleaning, Pydantic validation |
| ☁️ **Deploy-ready** | One-click deploy on Streamlit Cloud with `st.secrets` support |

---

## 🏗️ Architecture

```
┌──────────────┐       ┌──────────────────┐       ┌────────────────┐       ┌─────────────┐
│  PDF Upload  │──────▶│   LLMWhisperer   │──────▶│  OpenAI LLM    │──────▶│  Pydantic   │
│  (Streamlit) │       │  (structured     │       │  (JSON mode +  │       │  validation │
│              │       │   OCR + layout)  │       │   prompt)      │       │  & typing   │
└──────────────┘       └──────────────────┘       └────────────────┘       └──────┬──────┘
                                                                                   │
                              ┌────────────────────────────────────────────────────┘
                              │
                              ▼
                       ┌──────────────┐
                       │  Excel       │
                       │  (3 sheets:  │
                       │  Summary,    │
                       │  Detail,     │
                       │  Concepts)   │
                       └──────────────┘
```

**Pipeline stages:**

1. **OCR with layout preservation** — LLMWhisperer converts PDFs (even scanned ones) into ASCII-structured text that preserves tables and positional info.
2. **LLM extraction with JSON mode** — A carefully engineered prompt instructs GPT-4o-mini to return a strict JSON schema. JSON mode guarantees parseable output.
3. **Pydantic validation** — Raw LLM output passes through Pydantic v2 models that coerce types, normalize numeric formats, and handle missing fields gracefully.
4. **Excel generation** — pandas + openpyxl write a multi-sheet workbook ready for analysis.

---

## 🛠️ Tech Stack

<table>
<tr>
<td><b>Frontend</b></td>
<td>Streamlit</td>
</tr>
<tr>
<td><b>LLM Orchestration</b></td>
<td>LangChain · OpenAI (gpt-4o-mini, JSON mode)</td>
</tr>
<tr>
<td><b>OCR / Document AI</b></td>
<td>LLMWhisperer v2 (Unstract)</td>
</tr>
<tr>
<td><b>Data Validation</b></td>
<td>Pydantic v2</td>
</tr>
<tr>
<td><b>Resilience</b></td>
<td>Tenacity (exponential backoff, selective retry)</td>
</tr>
<tr>
<td><b>Data Processing</b></td>
<td>pandas · openpyxl</td>
</tr>
<tr>
<td><b>Testing</b></td>
<td>pytest</td>
</tr>
<tr>
<td><b>Deployment</b></td>
<td>Streamlit Cloud</td>
</tr>
</table>

---

## 🚀 Quickstart

### Prerequisites

- Python 3.10+
- [OpenAI API key](https://platform.openai.com/api-keys)
- [LLMWhisperer API key](https://unstract.com/llmwhisperer/) (free tier available)

### Local installation

```bash
# Clone the repo
git clone https://github.com/osangaal/invoice-ai-extractor.git
cd invoice-ai-extractor

# Install dependencies
pip install -r requirements.txt

# Set up your API keys
cp env.example .env
# Edit .env and add your keys

# Run the app
streamlit run app.py
```

The app will open at `http://localhost:8501`.

### Environment variables

```env
OPENAI_API_KEY=sk-...
LLMWHISPERER_API_KEY=...
OPENAI_MODEL=gpt-4o-mini   # optional, defaults to gpt-4o-mini
```

---

## ☁️ Deploy on Streamlit Cloud

1. Fork or push this repo to your GitHub.
2. Go to [share.streamlit.io](https://share.streamlit.io) → connect your repo.
3. In **Secrets**, paste your credentials:
   ```toml
   OPENAI_API_KEY = "sk-..."
   LLMWHISPERER_API_KEY = "..."
   OPENAI_MODEL = "gpt-4o-mini"
   ```
4. Deploy. ⚡

---

## 📁 Project Structure

```
invoice-ai-extractor/
├── app.py                          # Streamlit UI
├── requirements.txt
├── packages.txt                    # apt dependencies (Streamlit Cloud)
├── env.example
├── assets/
│   └── styles.css                  # Custom CSS
├── config/
│   └── prompts.yaml                # LLM prompts + processing config
├── src/
│   ├── clients/
│   │   ├── openai_client.py        # OpenAI w/ JSON mode + retries
│   │   └── llmwhisperer_client.py  # LLMWhisperer w/ smart retry
│   ├── services/
│   │   └── pdf_processor.py        # Main orchestrator
│   └── utils/
│       ├── secrets.py              # env vars + st.secrets resolver
│       └── models.py               # Pydantic v2 validation models
├── tests/                          # pytest unit tests
│   ├── test_models.py
│   └── test_openai_client.py
└── .streamlit/
    ├── config.toml
    └── secrets.toml.example
```

---

## 🧪 Testing

```bash
pip install pytest
pytest tests/ -v
```

```
tests/test_models.py::TestToFloat::test_handles_european_format        PASSED
tests/test_models.py::TestToFloat::test_handles_currency_prefix        PASSED
tests/test_models.py::TestConceptoFacturacion::test_normalizes_importe PASSED
tests/test_openai_client.py::TestCleanMarkdownJson::test_strips_json_fence PASSED
...
============================== 18 passed in 0.65s ==============================
```

---

## 🎬 Demo

> 🚧 *Live demo coming soon — deploy your own following the [Quickstart](#-quickstart).*

### Sample workflow

1. **Upload** one or multiple invoice PDFs.
2. Click **🚀 Process PDFs**.
3. Watch live metrics: tokens, cost, success rate.
4. Download a structured Excel with 3 sheets.
5. (Optional) Enable **debug mode** to inspect the raw JSON, LLMWhisperer text output, and per-file metrics.

---

## 🔍 Extracted Fields

<details>
<summary><b>Full schema</b> (click to expand)</summary>

```json
{
  "informacion_cliente": {
    "nombre_cliente": "...",
    "direccion": "...",
    "nis": "...",
    "contrato": "..."
  },
  "datos_factura": {
    "numero_factura": "...",
    "fecha_emision": "...",
    "fecha_vencimiento": "...",
    "medidor": "...",
    "sector": "..."
  },
  "periodo_lectura": {
    "fecha_desde": "...",
    "fecha_hasta": "...",
    "dias": 0,
    "tarifa": "..."
  },
  "conceptos_facturacion": [
    {"concepto": "Cargo Fijo", "importe": 0.0},
    {"concepto": "Energía", "importe": 0.0}
  ],
  "totales": {
    "total_mes": 0.0,
    "gran_total": 0.0,
    "saldo_anterior": 0.0
  },
  "resumen_tabular": { ... }
}
```

</details>

---

## ⚙️ Configuration

Adjust LLM behavior, parallel workers, and OCR settings in [`config/prompts.yaml`](config/prompts.yaml):

```yaml
models:
  default_model: "gpt-4o-mini"
  temperature: 0.0

llmwhisperer:
  mode: "table"                 # table | text | form | low_cost
  output_mode: "layout_preserving"
  wait_timeout: 120

parallel_processing:
  max_workers: 3                # threads for batch processing
  chunk_size: 5
```

---

## 🐛 Troubleshooting

| Symptom | Likely cause / Fix |
|---|---|
| `API Keys not configured` | Check env vars or `.streamlit/secrets.toml` |
| `LLMWhisperer client not available` | Run `pip install llmwhisperer-client>=2.3.1` |
| Empty / invalid JSON in response | The PDF may be an unsearchable image — enable debug mode to inspect raw text |
| Timeouts on large batches | Lower `max_workers` in `config/prompts.yaml` |
| `langchain.schema` import error | The code uses `langchain_core.messages` with a fallback — make sure your `langchain` is up to date |

---

## 🗺️ Roadmap

- [ ] Support for additional invoice types (telecom, utilities)
- [ ] PostgreSQL persistence for processed invoices
- [ ] REST API endpoint (FastAPI) for programmatic access
- [ ] Async processing with Celery for >100-file batches
- [ ] Multi-language invoice support
- [ ] OCR fallback (Tesseract) for offline-friendly mode

---

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repo
2. Create a feature branch (`git checkout -b feat/amazing-feature`)
3. Commit your changes (`git commit -m 'feat: add amazing feature'`)
4. Push to the branch (`git push origin feat/amazing-feature`)
5. Open a Pull Request

---

## 📝 License

Distributed under the MIT License. See [LICENSE](LICENSE) for details.

---

## 👤 Author

**Diego Fernando Martínez Herreño**

---

<div align="center">

**If this project helped you, please consider giving it a ⭐!**


</div>
