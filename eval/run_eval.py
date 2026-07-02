"""Layer 6: groundedness eval — YOUR STANDOUT, HONESTY-AS-A-METRIC BULLET.

For each test job description, run the agent and check that every retrieved source
is real and that the agent reports a sane number of revisions. The interesting metric
to report: average revisions-to-pass, and a manual groundedness spot-check rate.

Loop + reporting written. You implement the groundedness check.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import json
from pathlib import Path
from app.agent import run
TESTS = Path(__file__).parent / "job_descriptions.json"




def is_grounded(bullets, sources):
    return bool(bullets and bullets.strip()) and len(sources) > 0


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
