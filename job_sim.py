import os
import random
import sys


ERROR_CATALOG = {
    "OBJECT_NOT_FOUND": {
        "summary": "Required object does not exist",
        "details": "The workflow could not find the required object in storage.",
        "severity": "medium",
    },
    "OUTPUT_WRITE_FAILED": {
        "summary": "Output write failed",
        "details": "The workflow failed while writing the output artifact.",
        "severity": "high",
    },
    "INVALID_INPUT": {
        "summary": "Input validation failed",
        "details": "The workflow received invalid or incomplete input data.",
        "severity": "medium",
    },
    "DOWNSTREAM_UNAVAILABLE": {
        "summary": "Downstream service unavailable",
        "details": "A required downstream dependency did not respond successfully.",
        "severity": "high",
    },
    "PROCESSING_TIMEOUT": {
        "summary": "Processing timed out",
        "details": "The workflow exceeded the allowed processing time.",
        "severity": "high",
    },
}


def emit_failure(error_code: str) -> int:
    error = ERROR_CATALOG.get(error_code)
    if error is None:
        print(f"Unknown SIM_ERROR_CODE: {error_code}", file=sys.stderr)
        return 2

    print("JOB_RESULT=FAILURE", file=sys.stderr)
    print(f"ERROR_CODE={error_code}", file=sys.stderr)
    print(f"SUMMARY={error['summary']}", file=sys.stderr)
    print(f"DETAILS={error['details']}", file=sys.stderr)
    print(f"SEVERITY={error['severity']}", file=sys.stderr)
    return 1


def main() -> int:
    mode = os.getenv("SIM_MODE", "success").strip().lower()
    requested_error_code = (
        os.getenv("SIM_ERROR_CODE", "OBJECT_NOT_FOUND").strip().upper()
    )

    print("Starting simulated operational job...")

    if mode == "success":
        print("Job completed successfully.")
        print("Records processed and output generated.")
        return 0

    if mode == "random":
        error_code = random.choice(list(ERROR_CATALOG.keys()))
        return emit_failure(error_code)

    if mode == "failure":
        return emit_failure(requested_error_code)

    print(f"Unknown SIM_MODE: {mode}", file=sys.stderr)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
