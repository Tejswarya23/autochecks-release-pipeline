"""Release manifest generator with readiness gate evaluation."""

import json
import sys
import datetime
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from config.settings import RELEASE_GATES, VERSION, PIPELINE_NAME


def evaluate_gates(test_pass_rate: float, open_p0_issues: int,
                   built_modules: list, artifact_exists: bool) -> dict:
    results = {}
    results["test_pass_rate"] = {
        "passed": test_pass_rate >= RELEASE_GATES["min_test_pass_rate"],
        "value": test_pass_rate,
        "threshold": RELEASE_GATES["min_test_pass_rate"],
    }
    results["p0_issues"] = {
        "passed": open_p0_issues <= RELEASE_GATES["max_open_p0_issues"],
        "value": open_p0_issues,
        "threshold": RELEASE_GATES["max_open_p0_issues"],
    }
    missing = [m for m in RELEASE_GATES["required_modules"] if m not in built_modules]
    results["required_modules"] = {
        "passed": len(missing) == 0,
        "missing": missing,
    }
    results["artifact_exists"] = {
        "passed": artifact_exists,
    }
    return results


def generate_manifest(test_pass_rate: float, open_p0_issues: int,
                      built_modules: list, artifact_exists: bool) -> dict:
    gate_results = evaluate_gates(test_pass_rate, open_p0_issues,
                                  built_modules, artifact_exists)
    all_passed = all(v["passed"] for v in gate_results.values())
    manifest = {
        "pipeline": PIPELINE_NAME,
        "version": VERSION,
        "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat() + "Z",
        "release_approved": all_passed,
        "gates": gate_results,
        "summary": "RELEASE APPROVED" if all_passed else "RELEASE BLOCKED gate failures detected",
    }
    return manifest


if __name__ == "__main__":
    # Simulate a real pipeline run
    manifest = generate_manifest(
        test_pass_rate=100.0,
        open_p0_issues=0,
        built_modules=["vehicle_simulator", "release_tool", "config"],
        artifact_exists=True,
    )
    print(json.dumps(manifest, indent=2))
    with open("release_manifest.json", "w") as f:
        json.dump(manifest, f, indent=2)
    print("\nManifest written to release_manifest.json")
    if not manifest["release_approved"]:
        sys.exit(1)
