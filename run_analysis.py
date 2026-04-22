#!/usr/bin/env python3
import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "src"))

from lead_acid.pipeline import run_pipeline


def parse_args():
    parser = argparse.ArgumentParser(description="Run lead-acid analysis pipeline.")
    parser.add_argument(
        "--input",
        default=str(ROOT / "data" / "lead_acid_data.xlsx"),
        help="Path to input Excel file (default: data/lead_acid_data.xlsx).",
    )
    parser.add_argument(
        "--output",
        default=str(ROOT / "outputs" / "lead_acid_stats_outputs"),
        help="Directory for output files (default: outputs/lead_acid_stats_outputs).",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    input_path = Path(args.input)
    if not input_path.exists():
        raise FileNotFoundError(
            f"Input file not found: {input_path}\n"
            "Place your Excel file at data/lead_acid_data.xlsx "
            "or pass --input with a repo-relative path."
        )
    run_pipeline(str(input_path), args.output)
