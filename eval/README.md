# RAG Evaluation Dataset Specification — Brújula Vocacional Colombia

> **Important Status Note**: This directory provides a **defined evaluation dataset and specification** (`questions.json`). It does **not** report measured retrieval benchmarks, as no live RAG retrieval or inference pipeline has been benchmarked in this repository.

---

## Purpose

The evaluation pack defines concrete test cases to evaluate downstream conversational RAG systems (such as Microsoft 365 Copilot Studio or custom LangChain/LlamaIndex pipelines) grounded on the Brújula Vocacional Colombia knowledge base.

---

## Contract Schema (`schema.json`)

Each test item in `questions.json` adheres to the formal schema defined in [`eval/schema.json`](schema.json):

```json
{
  "id": "BRU-RIA-001",
  "question": "¿Qué ocupaciones del catálogo del SENA se alinean con un perfil predominantemente Realista e Investigador?",
  "expected_topic": "RIASEC_INTEREST_MAPPING",
  "expected_source": "01_Compendio_Integral_Exploracion_Intereses_RIASEC_Colombia.pdf",
  "expected_section": "Compendio 1: #realista-r y #investigativa-i (#combinaciones-de-intereses)",
  "should_answer": true,
  "rationale": "El Compendio 1 detalla la correspondencia entre rasgos Realistas/Investigadores y programas de automatización, mecánica industrial y telecomunicaciones del SENA."
}
```

---

## Defined Evaluation Cases (30 Items)

| Category | Cases | `should_answer` | Evaluation Target |
|---|---|---|---|
| `RIASEC_INTEREST_MAPPING` | 8 | `true` | Accuracy of mapping RIASEC interest dimensions to Colombian technical / vocational tracks. |
| `COLOMBIAN_CONTEXT` | 8 | `true` | Knowledge of youth educational transitions, regional barriers, and pedagogical accompaniment. |
| `SAFETY_REFUSAL_OUT_OF_BOUNDS` | 7 | `false` | Verifies safe refusal of clinical counseling, psychiatric medication, wage guarantees, and PII requests. |
| `EXTERNAL_LIVE_DATA_REQUIRED` | 7 | `false` | Verifies safe redirection to official portals for dynamic dates, tuition fees, and live credit statuses. |

---

## Specification Validation

Run the contract validator to confirm dataset integrity and source file existence:

```bash
python -m pip install -r requirements-dev.txt
python eval/validate_benchmark.py
```

Validation checks:
1. Conformance to evaluation item keys and constraints.
2. Uniqueness of item IDs.
3. Category balance across in-domain and out-of-bounds queries.
4. Existence of referenced local compendiums and web documents on disk.
