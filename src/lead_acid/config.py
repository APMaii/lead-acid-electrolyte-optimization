RESPONSES = {
    "RevRatio": {"label": "Reversibility (Ir/Io)", "goal": "max"},
    "DeltaE": {"label": "Reversibility (Er-Eo)", "goal": "min"},
    "Overpot": {"label": "-Overpotential at -10mA", "goal": "max"},
    "Rct": {"label": "R_ct", "goal": "min"},
}

# Based on your current model comparison decisions in the script.
BEST_MODEL = {
    "RevRatio": "reduced",
    "DeltaE": "quadratic",
    "Overpot": "reduced",
    "Rct": "reduced",
}
