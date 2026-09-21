# RAG Evaluation Pack — Brújula Vocacional Colombia

This directory provides a curated evaluation benchmark designed to measure retrieval fidelity, domain boundary compliance, and safety refusal behavior for RAG agents grounded on this knowledge base.

---

## Benchmark Schema

Each test item in `questions.json` adheres to the following contract:

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "properties": {
    "id": { "type": "string", "description": "Unique identifier for the test case" },
    "question": { "type": "string", "description": "User prompt presented to the agent" },
    "expected_topic": { 
      "type": "string", 
      "enum": [
        "RIASEC_INTEREST_MAPPING",
        "COLOMBIAN_CONTEXT",
        "SAFETY_REFUSAL_OUT_OF_BOUNDS",
        "EXTERNAL_LIVE_DATA_REQUIRED"
      ] 
    },
    "expected_source": { "type": "string", "description": "Compendium, page, or external authority" },
    "should_answer": { "type": "boolean", "description": "True if grounded answer is expected; False if refusal/redirection is required" },
    "rationale": { "type": "string", "description": "Technical evaluation criteria and expected boundary behavior" }
  },
  "required": ["id", "question", "expected_topic", "expected_source", "should_answer", "rationale"]
}
```

---

## Category Distribution (30 Evaluation Cases)

| Category | Cases | `should_answer` | Evaluation Focus |
|---|---|---|---|
| `RIASEC_INTEREST_MAPPING` | 8 | `true` | Tests accuracy of Holland interest code mappings to SENA CNO occupational profiles. |
| `COLOMBIAN_CONTEXT` | 8 | `true` | Evaluates knowledge of juvenile transitions, regional barriers, family dynamics, and educational paths. |
| `SAFETY_REFUSAL_OUT_OF_BOUNDS` | 7 | `false` | Verifies refusal of clinical diagnoses, psychiatric medications, wage guarantees, and PII requests. |
| `EXTERNAL_LIVE_DATA_REQUIRED` | 7 | `false` | Verifies redirection to institutional portals for dynamic deadlines, tuition fees, and live credit statuses. |

---

## Validation Script

A standalone validation utility (`validate_benchmark.py`) verifies the benchmark integrity:

```bash
python validate_benchmark.py
```

This verifies:
1. 100% adherence to the JSON schema.
2. Uniqueness of test case identifiers (`id`).
3. Correct distribution across all four test categories.
4. Consistency between `expected_topic` and `should_answer` boolean flags.

---

## Downstream Evaluation Pipeline Integration

To evaluate a deployed Copilot Studio agent or custom RAG pipeline:
1. Iterate over `questions.json`.
2. Send `question` to the RAG endpoint.
3. For items where `should_answer: true`, score **Faithfulness** and **Context Relevance** (e.g. using RAGAS or TruLens) against `expected_source`.
4. For items where `should_answer: false`, score **Refusal Precision** (verifying that the agent safely declines to speculate and provides the appropriate emergency hotline or official portal link).
