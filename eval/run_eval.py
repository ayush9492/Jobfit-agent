"""Layer 6: groundedness eval — YOUR STANDOUT, HONESTY-AS-A-METRIC BULLET.

For each test job description, run the agent and check that every retrieved source
is real and that the agent reports a sane number of revisions. The interesting metric
to report: average revisions-to-pass, and a manual groundedness spot-check rate.

Loop + reporting written. You implement the groundedness check.
"""
import json
from pathlib import Path
from app.agent import run

TESTS = Path(__file__).parent / "job_descriptions.json"


def is_grounded(bullets, sources):
    """
    TODO (you implement):
    A lightweight automatic check. One reasonable proxy: ensure the agent returned
    at least one source and that `bullets` is non-empty. For a stronger check, ask
    the LLM (app.llm.call_llm) to verify each bullet is supported by the experience
    corpus and return a yes/no. Return True/False.
    """
    raise NotImplementedError


def main():
    jds = json.loads(TESTS.read_text())
    total_revs = grounded = 0
    for jd in jds:
        r = run(jd)
        total_revs += r["revisions"]
        ok = is_grounded(r["bullets"], r["sources"])
        grounded += ok
        print(f"{'✓' if ok else '✗'} grounded | revisions={r['revisions']} | {jd[:50]}...")
    n = len(jds)
    print(f"\nGrounded: {grounded}/{n} ({grounded/n:.0%})")
    print(f"Avg revisions to pass: {total_revs/n:.1f}")


if __name__ == "__main__":
    main()
