import pandas as pd
import statsmodels.formula.api as smf
from statsmodels.stats.anova import anova_lm

from .config import RESPONSES, BEST_MODEL
from .data import load_and_prepare, prepare_output_dir
from .modeling import fit_best_model, get_formula
from .plots import (
    save_correlation,
    save_observed_vs_predicted,
    save_residual_and_qq,
    save_real_heatmaps,
    save_predicted_surfaces,
)
from .style import apply_global_style


def _zscore(x):
    return (x - x.mean()) / x.std(ddof=0)


def run_pipeline(input_path: str, output_path: str) -> None:
    apply_global_style()
    df = load_and_prepare(input_path)
    outdir = prepare_output_dir(output_path)

    # Descriptive stats
    desc = df[["RevRatio", "DeltaE", "Overpot", "Rct"]].describe().T
    desc["range"] = desc["max"] - desc["min"]
    desc.to_excel(outdir / "01_descriptive_statistics.xlsx")

    # Figures
    save_correlation(df, outdir)
    save_observed_vs_predicted(df, RESPONSES, outdir)
    save_residual_and_qq(df, RESPONSES, outdir)
    save_real_heatmaps(df, RESPONSES, outdir)
    save_predicted_surfaces(df, RESPONSES, outdir)

    # Table 2: reduced factorial vs quadratic OLS comparison.
    # Preferred model follows BEST_MODEL rather than a fresh adjusted-R² rule.
    comparison_rows = []
    for y in RESPONSES:
        reduced = smf.ols(get_formula(y, "reduced"), data=df).fit()
        quadratic = smf.ols(get_formula(y, "quadratic"), data=df).fit()
        comparison_rows.append(
            {
                "response": y,
                "reduced_R2": reduced.rsquared,
                "quad_R2": quadratic.rsquared,
                "reduced_Adj_R2": reduced.rsquared_adj,
                "quad_Adj_R2": quadratic.rsquared_adj,
                "reduced_AIC": reduced.aic,
                "quad_AIC": quadratic.aic,
                "reduced_BIC": reduced.bic,
                "quad_BIC": quadratic.bic,
                "preferred_model": (
                    "Reduced Factorial" if BEST_MODEL[y] == "reduced" else "Quadratic"
                ),
            }
        )
    with pd.ExcelWriter(outdir / "10_model_comparison.xlsx", engine="openpyxl") as writer:
        pd.DataFrame(comparison_rows).to_excel(
            writer, sheet_name="Model_comparison", index=False
        )

    # Effect size by best model
    effect_writer = pd.ExcelWriter(outdir / "16_effect_size_summary.xlsx", engine="openpyxl")
    for y in RESPONSES.keys():
        model = fit_best_model(df, y)
        anova_tbl = anova_lm(model, typ=2).copy()
        if "sum_sq" in anova_tbl.columns:
            ss_resid = anova_tbl.loc["Residual", "sum_sq"]
            anova_tbl["partial_eta_sq"] = anova_tbl["sum_sq"] / (anova_tbl["sum_sq"] + ss_resid)
        anova_tbl["model_used"] = "Reduced Factorial" if BEST_MODEL[y] == "reduced" else "Quadratic"
        anova_tbl.to_excel(effect_writer, sheet_name=f"{y}_effect_sizes")
    effect_writer.close()

    # Composite score (Table D1). Same z-score mean as the removed duplicate block.
    opt = df.copy()
    opt["RevRatio_z"] = _zscore(opt["RevRatio"])
    opt["DeltaE_good"] = _zscore(-opt["DeltaE"])
    opt["Overpot_z"] = _zscore(opt["Overpot"])
    opt["Rct_good"] = _zscore(-opt["Rct"])

    score_columns = ["RevRatio_z", "DeltaE_good", "Overpot_z", "Rct_good"]
    opt["CompositeScore"] = opt[score_columns].mean(axis=1)
    opt = opt.sort_values("CompositeScore", ascending=False)

    opt[
        ["Sample", "Mg", "Al", "P", "RevRatio", "DeltaE",
         "Overpot", "Rct", "CompositeScore"]
    ].to_excel(outdir / "17_composite_score_ranking.xlsx", sheet_name="Sheet1", index=False)

    # Appendix D sensitivity analysis
    # Weight order is RevRatio, DeltaE, Overpot, Rct.
    scenarios = {
        "Equal": [0.25, 0.25, 0.25, 0.25],
        "RevRatio": [0.55, 0.15, 0.15, 0.15],
        "DeltaE": [0.15, 0.55, 0.15, 0.15],
        "Overpot": [0.15, 0.15, 0.55, 0.15],
        "Rct": [0.15, 0.15, 0.15, 0.55],
    }

    detail = opt[["Sample", *score_columns]].copy()
    equal_rank = opt["CompositeScore"].rank(ascending=False, method="average")
    summary = []

    for scenario, weights in scenarios.items():
        if scenario == "Equal":
            score = opt["CompositeScore"]
        else:
            score = opt[score_columns].mul(weights).sum(axis=1)

        rank = score.rank(ascending=False, method="average")
        detail[f"{scenario}_score"] = score
        detail[f"{scenario}_rank"] = rank

        top_five = detail.sort_values([f"{scenario}_rank", "Sample"])["Sample"].head(5)
        summary.append({
            "Scenario": scenario,
            "RevRatio_weight": weights[0],
            "DeltaE_weight": weights[1],
            "Overpot_weight": weights[2],
            "Rct_weight": weights[3],
            "Top_5_samples": ", ".join(map(str, top_five)),
            "Sample_15_rank": rank.loc[opt["Sample"].eq(15)].iloc[0],
            "Spearman_rho_vs_equal": rank.corr(equal_rank),
        })

    with pd.ExcelWriter(
        outdir / "20_composite_score_sensitivity.xlsx", engine="openpyxl"
    ) as writer:
        pd.DataFrame(summary).to_excel(writer, sheet_name="Summary", index=False)
        detail.to_excel(writer, sheet_name="All_formulations", index=False)




    print("=" * 80)
    print("Statistical analysis complete.")
    print(f"All outputs saved in:\n{outdir}")
    print("=" * 80)
    print("\nModel used per response:")
    for y, m in BEST_MODEL.items():
        print(f"  {y:10s} -> {m}")
