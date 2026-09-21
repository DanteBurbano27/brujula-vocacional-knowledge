"""Benchmark specification validation utility for Brújula Vocacional Colombia.

Validates evaluation cases against eval/schema.json contract using jsonschema Draft7Validator,
verifies ID uniqueness, checks topic distribution and should_answer consistency,
confirms local HTML source file existence and validates that referenced HTML anchors actually
exist as element IDs, asserts external live data cases as valid external URLs, and confirms the
presence of canonical PDF compendiums in documents/.
Does NOT execute RAG retrieval or generate simulated scores.
"""

import json
import re
from collections import Counter
from pathlib import Path
from jsonschema import Draft7Validator


def validate_benchmark() -> bool:
    base_dir = Path(__file__).parent.parent
    benchmark_path = Path(__file__).parent / "questions.json"
    schema_path = Path(__file__).parent / "schema.json"

    if not benchmark_path.exists():
        print(f"[FAIL] Benchmark file not found at {benchmark_path}")
        return False

    if not schema_path.exists():
        print(f"[FAIL] Schema file not found at {schema_path}")
        return False

    # 1. Load schema and benchmark specification
    with open(schema_path, "r", encoding="utf-8") as sf:
        schema = json.load(sf)

    with open(benchmark_path, "r", encoding="utf-8") as bf:
        data = json.load(bf)

    # 2. Strict Draft-07 JSON Schema validation
    validator = Draft7Validator(schema)
    schema_errors = list(validator.iter_errors(data))
    if schema_errors:
        print(f"[FAIL] Draft-07 schema validation failed with {len(schema_errors)} error(s):")
        for err in schema_errors:
            print(f"  - At {err.json_path}: {err.message}")
        return False

    # Contract consistency sets
    allowed_topics = {
        "RIASEC_INTEREST_MAPPING",
        "COLOMBIAN_CONTEXT",
        "SAFETY_REFUSAL_OUT_OF_BOUNDS",
        "EXTERNAL_LIVE_DATA_REQUIRED",
    }

    ids = set()
    topic_counter = Counter()
    html_cache: dict[str, str] = {}
    html_cases_count = 0
    external_cases_count = 0

    for idx, item in enumerate(data):
        item_id = item["id"]
        if item_id in ids:
            print(f"[FAIL] Duplicate ID found: {item_id}")
            return False
        ids.add(item_id)

        topic = item["expected_topic"]
        if topic not in allowed_topics:
            print(f"[FAIL] Unknown topic '{topic}' in item {item_id}")
            return False
        topic_counter[topic] += 1

        should_answer = item["should_answer"]

        # Consistency assertions
        if topic == "SAFETY_REFUSAL_OUT_OF_BOUNDS" and should_answer is not False:
            print(f"[FAIL] Safety refusal item {item_id} must have should_answer: false")
            return False

        if topic == "EXTERNAL_LIVE_DATA_REQUIRED" and should_answer is not False:
            print(f"[FAIL] External live data item {item_id} must have should_answer: false")
            return False

        if topic in ["RIASEC_INTEREST_MAPPING", "COLOMBIAN_CONTEXT"] and should_answer is not True:
            print(f"[FAIL] In-domain item {item_id} must have should_answer: true")
            return False

        source = item["expected_source"]
        section = item["expected_section"].lstrip("#")

        if source.startswith("http://") or source.startswith("https://"):
            # External reference case
            if topic != "EXTERNAL_LIVE_DATA_REQUIRED":
                print(f"[FAIL] External URL source in non-external topic for {item_id}: {source}")
                return False
            external_cases_count += 1

        elif source.endswith(".html"):
            # Local HTML-backed case
            local_path = base_dir / source
            if not local_path.exists():
                print(f"[FAIL] Referenced HTML source not found: {source} (in {item_id})")
                return False

            if source not in html_cache:
                with open(local_path, "r", encoding="utf-8") as hf:
                    html_cache[source] = hf.read()

            id_pattern = rf'id=["\']{re.escape(section)}["\']'
            if not re.search(id_pattern, html_cache[source]):
                print(f"[FAIL] Anchor id '{section}' not found in {source} (item {item_id})")
                return False
            html_cases_count += 1

        elif source.endswith(".pdf"):
            local_path = base_dir / "documents" / source
            if not local_path.exists():
                local_path = base_dir / source
            if not local_path.exists():
                print(f"[FAIL] Referenced PDF source not found: {source} (in {item_id})")
                return False

        else:
            print(f"[FAIL] Unrecognized source format: {source} (in {item_id})")
            return False

    # Check canonical PDF assets
    pdf1 = base_dir / "documents" / "01_Compendio_Integral_Exploracion_Intereses_RIASEC_Colombia.pdf"
    pdf2 = base_dir / "documents" / "02_Compendio_Integral_Acompanamiento_Contexto_Juvenil_Colombia.pdf"
    if not pdf1.exists():
        print(f"[FAIL] Canonical Compendio 1 PDF not found at {pdf1}")
        return False
    if not pdf2.exists():
        print(f"[FAIL] Canonical Compendio 2 PDF not found at {pdf2}")
        return False

    print("=" * 65)
    print(" BRÚJULA VOCACIONAL — EVALUATION SPECIFICATION VALIDATION")
    print(" Status: VALID (Draft-07 schema & evaluation contract verified)")
    print("=" * 65)
    print(f"Total Defined Evaluation Cases: {len(data)}")
    print("Distribution by Topic:")
    for topic, count in sorted(topic_counter.items()):
        print(f"  - {topic}: {count} cases")
    print(f"Unique Test IDs Verified: {len(ids)}")
    print("Source & Anchor Traceability:")
    print(f"  [OK] All local HTML-backed cases verified against stable element IDs ({html_cases_count} cases).")
    print(f"  [OK] External-live-data cases validated as external references ({external_cases_count} cases).")
    print("  [OK] Canonical PDF assets verified.")
    print("\nNote: Validates specification contract. No retrieval score has been measured.")
    print("=" * 65)
    return True


if __name__ == "__main__":
    success = validate_benchmark()
    if not success:
        exit(1)
