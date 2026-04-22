from pathlib import Path

import pandas as pd


def load_and_prepare(input_path: str) -> pd.DataFrame:
    data = pd.read_excel(input_path)
    data.columns = [c.strip() for c in data.columns]

    df = data.rename(
        columns={
            "Reversibility Ratio": "Reversibility (Ir/Io)",
            "Reversibility Energy": "Reversibility (Er-Eo)",
            "Overpotential": "-Overpotential at -10mA",
            "Resistance Ct": "R_ct",
        }
    )

    df = df[
        [
            "Sample",
            "MgSO4.7H2O (wt.%)",
            "AlSO4.18H2O (wt.%)",
            "Phosphoric Acid (wt.%)",
            "Reversibility (Ir/Io)",
            "Reversibility (Er-Eo)",
            "-Overpotential at -10mA",
            "R_ct",
        ]
    ].copy()

    df = df.rename(
        columns={
            "MgSO4.7H2O (wt.%)": "Mg",
            "AlSO4.18H2O (wt.%)": "Al",
            "Phosphoric Acid (wt.%)": "P",
            "Reversibility (Ir/Io)": "RevRatio",
            "Reversibility (Er-Eo)": "DeltaE",
            "-Overpotential at -10mA": "Overpot",
            "R_ct": "Rct",
        }
    )

    df["Mg_cat"] = df["Mg"].astype(str)
    df["Al_cat"] = df["Al"].astype(str)
    df["P_cat"] = df["P"].astype(str)
    return df


def prepare_output_dir(path: str) -> Path:
    outdir = Path(path)
    outdir.mkdir(parents=True, exist_ok=True)
    return outdir
