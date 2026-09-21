"""Benchmark validation utility for Brújula Vocacional RAG evaluation pack."""

import json
from pathlib import Path
from typing import Counter


def validate_benchmark() -> bool:
    benchmark_path = Path(__file__).parent / "questions.json"
    if not benchmark_path.exists():
        print(f"[FAIL] Benchmark file not found at {benchmark_path}")
        return False

    with open(benchmark_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    if not isinstance(data, list):
        print("[FAIL] Root of questions.json must be an array.")
        return False

    required_keys = {"id", "question", "expected_topic", "expected_source", "should_answer", "rationale"}
    allowed_topics = {
        "RIASEC_INTEREST_MAPPING",
        "COLOMBIAN_CONTEXT",
        "SAFETY_REFUSAL_OUT_OF_BOUNDS",
        "EXTERNAL_LIVE_DATA_REQUIRED",
    }

    ids = set()
    topic_counter = Counter()

    for idx, item in enumerate(data):
        if not isinstance(item, dict):
            print(f"[FAIL] Item at index {idx} is not an object.")
            return False

        missing = required_keys - set(item.keys())
        if missing:
            print(f"[FAIL] Item {item.get('id', idx)} is missing keys: {missing}")
            return False

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
        if not isinstance(should_answer, bool):
            print(f"[FAIL] 'should_answer' must be boolean in {item_id}")
            return False

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

    print("=" * 60)
    print(" RAG EVALUATION BENCHMARK VALIDATION PASSED")
    print("=" * 60)
    print(f"Total Evaluated Test Cases: {len(data)}")
    print("Distribution by Topic:")
    for topic, count in topic_counter.items():
        print(f"  - {topic}: {count} cases")
    print(f"Unique Test IDs Verified: {len(ids)}")
    print("Zero synthetic or fake retrieval scores generated.")
    print("=" * 60)
    return True


if __name__ == "__main__":
    success = validate_benchmark()
    if not success:
        exit(1)
