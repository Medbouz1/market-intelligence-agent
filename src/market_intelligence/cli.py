"""Command line entry point."""
import argparse
import json
from pathlib import Path

from .engine import build_report
from .pdf import render_pdf


def main():
    parser = argparse.ArgumentParser(description="Market Intelligence PDF+JSON generator")
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--out", type=Path, default=Path("reports"))
    parser.add_argument("--allow-synthetic", action="store_true")
    args = parser.parse_args()
    snapshot = json.loads(args.input.read_text(encoding="utf-8"))
    if snapshot.get("synthetic") and not args.allow_synthetic:
        parser.error("DONNÉES FICTIVES : publication refusée sans --allow-synthetic")
    report = build_report(snapshot)
    args.out.mkdir(parents=True, exist_ok=True)
    (args.out / "market_intelligence.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    output = args.out / "market_intelligence.pdf"
    render_pdf(report, output)
    print("Rapport généré : " + str(output))
    if report["quality_warnings"]:
        print("AVERTISSEMENTS : " + "; ".join(report["quality_warnings"]))


if __name__ == "__main__":
    main()
