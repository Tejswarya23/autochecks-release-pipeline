"""Release readiness gate configuration."""

RELEASE_GATES = {
    "min_test_pass_rate": 95.0,       # % of tests that must pass
    "max_open_p0_issues": 0,          # zero P0 bugs allowed
    "required_modules": [             # all must have passing builds
        "vehicle_simulator",
        "release_tool",
        "config",
    ],
    "artifact_must_exist": True,      # release artifact required
}

VERSION = "1.0.0"
PIPELINE_NAME = "auto-release-pipeline"
