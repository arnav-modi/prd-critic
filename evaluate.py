from datetime import datetime

import critic
from critic import review_prd
from eval_data import PRDS


def finding_matches_flaw(flaw, finding):
    """Does this finding correctly point at this planted flaw?"""
    if flaw["anchors"] == ["(missing)"]:
        text = (finding.issue + " " + finding.suggested_fix).lower()
        return finding.quote == "(missing)" and any(
            k in text for k in flaw["keywords"]
        )
    if finding.quote == "(missing)":
        return False
    q = finding.quote.lower().strip()
    if not q:
        return False
    for a in flaw["anchors"]:
        a = a.lower()
        if a in q or q in a:
            return True
    return False


def check_answer_key():
    """Catch typos: every anchor must really appear in its PRD."""
    for prd in PRDS:
        for flaw in prd["flaws"]:
            if flaw["anchors"] == ["(missing)"]:
                continue
            for a in flaw["anchors"]:
                if a.lower() not in prd["text"].lower():
                    raise ValueError(f"Anchor not found in {prd['name']}: {a!r}")


def main():
    check_answer_key()
    mode = "MOCK" if critic.USE_MOCK else "REAL"
    print(f"MODE: {mode}\n")

    total_flaws = 0
    total_caught = 0
    total_findings = 0
    total_unmatched = 0
    unmatched_list = []

    for prd in PRDS:
        print(f"=== {prd['name']}")
        results = review_prd(prd["text"])
        by_dim = {r.dimension: r for r in results}

        for flaw in prd["flaws"]:
            result = by_dim.get(flaw["dimension"])
            findings = result.findings if result else []
            caught = any(finding_matches_flaw(flaw, f) for f in findings)
            total_flaws += 1
            total_caught += caught
            label = flaw["anchors"][0]
            print(f"  {'CAUGHT' if caught else 'MISSED'}  [{flaw['dimension']}] {label}")

        # Findings that match no planted flaw (maybe valid, maybe false alarms)
        for r in results:
            for f in r.findings:
                total_findings += 1
                same_dim = [fl for fl in prd["flaws"] if fl["dimension"] == r.dimension]
                if not any(finding_matches_flaw(fl, f) for fl in same_dim):
                    total_unmatched += 1
                    unmatched_list.append((prd["name"], r.dimension, f.quote, f.issue))
        print()

    recall = round(100 * total_caught / total_flaws)
    print("-" * 50)
    print(f"RECALL: {total_caught}/{total_flaws} planted flaws caught = {recall}%")
    matched = total_findings - total_unmatched
    print(f"FINDINGS: {total_findings} total, {matched} matched a planted flaw, "
          f"{total_unmatched} unmatched")

    if unmatched_list:
        print("\nUNMATCHED FINDINGS (judge each by hand: valid extra issue or false alarm?)")
        for name, dim, quote, issue in unmatched_list:
            print(f"  - {name} / {dim}: \"{quote}\"")
            print(f"      {issue}")

    with open("eval_log.txt", "a", encoding="utf-8") as log:
        log.write(f"{datetime.now():%Y-%m-%d %H:%M} | {mode} | "
                  f"recall {total_caught}/{total_flaws} ({recall}%) | "
                  f"unmatched {total_unmatched}\n")
    print("\n(Result added to eval_log.txt)")


if __name__ == "__main__":
    main()