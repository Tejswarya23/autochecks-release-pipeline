# autochecks-release-pipeline

A production-inspired, monorepo release pipeline built with Bazel and Jenkins, featuring automated release gating, manifest generation, and 25 unit tests covering both pass and failure modes.

Designed to mirror the release orchestration challenges of safety-critical autonomous vehicle software delivery.

---

## Tech Stack
Bazel
Jenkins
Python
Github

---
## Project Structure

autochecks-release-pipeline/

autochecks-release-pipeline/
    |-- vehicle_simulator/         # Simulated AV sensors (Lidar + Camera)
    |   |-- sensor.py              # Sensor modules with health checks
    |   |-- sensor_test.py         # 11 unit tests (pass + failure modes)
    |   +-- BUILD                  # Bazel build definition
    |-- release_tool/              # Release gatekeeper + manifest generator
    |   |-- release.py             # Gate evaluation + JSON manifest
    |   |-- release_test.py        # 14 unit tests (pass + failure modes)
    |   +-- BUILD                  # Bazel build definition
    |-- config/                    # Release gate configuration
    |   |-- settings.py            # Thresholds: pass rate, P0 issues, modules
    |   +-- BUILD                  # Bazel build definition
    |-- Jenkinsfile                # CI/CD pipeline definition
    |-- MODULE.bazel               # Bazel module dependencies
    +-- release_manifest.json      # Generated release report
---

## How It Works

### 1. Bazel Monorepo Build
Every module is independently buildable. Bazel detects which packages changed and only rebuilds affected targets — critical for large codebases.

### 2. Release Gates
Before any release is approved, the pipeline evaluates:
| Gate | Threshold | Action if failed |
|---|---|---|
| Test pass rate | >= 95% | Block release |
| Open P0 issues | 0 | Block release |
| Required modules built | All 3 | Block release |
| Release artifact exists | Yes | Block release |

### 3. Release Manifest
Every pipeline run generates a `release_manifest.json`:

```json
{
  "pipeline": "autochecks-release-pipeline",
  "version": "1.0.0",
  "release_approved": true,
  "gates": {
    "test_pass_rate": { "passed": true, "value": 100.0, "threshold": 95.0 },
    "p0_issues": { "passed": true, "value": 0, "threshold": 0 },
    "required_modules": { "passed": true, "missing": [] },
    "artifact_exists": { "passed": true }
  },
  "summary": "RELEASE APPROVED"
}
```

### 4. Jenkins Pipeline
The `Jenkinsfile` orchestrates:
- Checkout -> Detect changed modules -> Bazel build ->  Bazel test -> Generate manifest -> Gate check

---

## Quick Start

### Prerequisites
- Python 3.x
- Bazel (via Bazelisk)

### Clone the repo
```bash
git clone https://github.com/Tejswarya23/autochecks-release-pipeline.git
cd autochecks-release-pipeline
```

### Build all modules
```bash
bazel build //...
```

### Run all tests
```bash
bazel test //... --test_output=all
```

### Generate release manifest
```bash
python3 release_tool/release.py
```

---

## Test Coverage
//vehicle_simulator:sensor_test 11 tests PASSED
//release_tool:release_test 14 tests PASSED
Total 25 tests ALL GREEN


Failure modes covered:
- Low test pass rate (80%, 0%)
- Pass rate at exact threshold (95.0%)
- Pass rate just below threshold (94.9%)
- Open P0 bugs (1, 5)
- Missing modules (partial, all)
- Missing release artifact
- Worst case all gates failing simultaneously

---

## Branch Strategy

| Branch | Purpose |
|---|---|
| `main` | Stable, production-ready |
| `dev` | Active development |
| `feature/*` | Individual feature additions |

---

## Roadmap

- feature/slack-notifications - notify team when release is blocked
- feature/github-actions - GitHub Actions as alternative to Jenkins
- feature/dashboard - HTML release status dashboard

---

## Author

**Tejaswini Boregowda**
Senior Build & Release / SCM Engineer
LinkedIn: https://www.linkedin.com/in/tejaswini-boregowda-3174a725/
github: https://github.com/Tejswarya23
