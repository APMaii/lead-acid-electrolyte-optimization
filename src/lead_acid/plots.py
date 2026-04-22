import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm

from .config import BEST_MODEL
from .modeling import get_formula, fit_best_model
from .style import annotate_sample_number


def save_correlation(df, outdir):
    corr = df[["RevRatio", "DeltaE", "Overpot", "Rct", "Mg", "Al", "P"]].corr()
    fig, ax = plt.subplots(figsize=(10, 8))
    im = ax.imshow(corr.values, aspect="auto", cmap="RdBu_r", vmin=-1, vmax=1)
    ax.set_xticks(range(len(corr.columns)))
    ax.set_yticks(range(len(corr.columns)))
    ax.set_xticklabels(corr.columns, rotation=45, ha="right")
    ax.set_yticklabels(corr.columns)
    ax.set_title("Correlation Matrix")

    for i in range(corr.shape[0]):
        for j in range(corr.shape[1]):
            val = corr.iloc[i, j]
            txt_color = "white" if abs(val) > 0.55 else "black"
            ax.text(
                j, i, f"{val:.2f}", ha="center", va="center", fontsize=9, fontweight="bold", color=txt_color
            )

    fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    plt.tight_layout()
    plt.savefig(outdir / "02_correlation_matrix.png", dpi=300, bbox_inches="tight")
    plt.close()


def save_observed_vs_predicted(df, responses, outdir):
    for y, info in responses.items():
        model = fit_best_model(df, y)
        pred = model.predict(df)
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.scatter(df[y], pred, s=85, edgecolor="black", linewidth=0.8, color="#4C72B0", alpha=0.9)

        mn = min(df[y].min(), pred.min())
        mx = max(df[y].max(), pred.max())
        ax.plot([mn, mx], [mn, mx], linestyle="--", linewidth=1.8, color="#DD8452")

        for i, row in df.iterrows():
            annotate_sample_number(ax, row[y], pred.iloc[i], row["Sample"], fontsize=9, ha="left", va="bottom")

        model_label = "Reduced Factorial" if BEST_MODEL[y] == "reduced" else "Quadratic"
        ax.set_title(f'Observed vs Predicted - {info["label"]}\n({model_label} Model)')
        ax.set_xlabel("Observed")
        ax.set_ylabel("Predicted")
        ax.grid(alpha=0.3)
        plt.tight_layout()
        plt.savefig(outdir / f"11_observed_vs_predicted_{y}.png", dpi=300, bbox_inches="tight")
        plt.close()


def save_residual_and_qq(df, responses, outdir):
    for y, info in responses.items():
        model = fit_best_model(df, y)
        fitted = model.fittedvalues
        resid = model.resid

        fig, ax = plt.subplots(figsize=(8, 6))
        ax.scatter(fitted, resid, s=85, edgecolor="black", linewidth=0.8, color="#55A868", alpha=0.9)
        ax.axhline(0, linestyle="--", linewidth=1.8, color="#C44E52")
        for i, s in enumerate(df["Sample"]):
            annotate_sample_number(ax, fitted.iloc[i], resid.iloc[i], s, fontsize=9, ha="left", va="bottom")

        model_label = "Reduced Factorial" if BEST_MODEL[y] == "reduced" else "Quadratic"
        ax.set_title(f'Residual Plot - {info["label"]}\n({model_label} Model)')
        ax.set_xlabel("Fitted")
        ax.set_ylabel("Residual")
        ax.grid(alpha=0.3)
        plt.tight_layout()
        plt.savefig(outdir / f"12_residual_plot_{y}.png", dpi=300, bbox_inches="tight")
        plt.close()

        fig = plt.figure(figsize=(7, 6))
        ax = fig.add_subplot(111)
        sm.qqplot(model.resid, line="45", ax=ax, markerfacecolor="none", markeredgecolor="black")
        ax.set_title(f'Q-Q Plot of Residuals - {info["label"]}\n({model_label} Model)')
        plt.tight_layout()
        plt.savefig(outdir / f"13_qqplot_{y}.png", dpi=300, bbox_inches="tight")
        plt.close()


def save_real_heatmaps(df, responses, outdir):
    for y, info in responses.items():
        al_levels = sorted(df["Al"].unique())
        mg_levels = sorted(df["Mg"].unique())
        p_levels = sorted(df["P"].unique())

        fig, axes = plt.subplots(1, len(al_levels), figsize=(18, 5), constrained_layout=True)
        if len(al_levels) == 1:
            axes = [axes]

        vmin = df[y].min()
        vmax = df[y].max()
        for ax, al in zip(axes, al_levels):
            sub = df[df["Al"] == al].copy()
            pivot = sub.pivot(index="Mg", columns="P", values=y).reindex(index=mg_levels, columns=p_levels)
            im = ax.imshow(pivot.values, aspect="auto", origin="lower", vmin=vmin, vmax=vmax, cmap="YlGnBu")
            ax.set_title(f"Al = {al}")
            ax.set_xlabel("P")
            ax.set_ylabel("Mg")
            ax.set_xticks(range(len(p_levels)))
            ax.set_yticks(range(len(mg_levels)))
            ax.set_xticklabels([f"{x:.2f}" for x in p_levels])
            ax.set_yticklabels([f"{x:.2f}" for x in mg_levels])

            for i in range(len(mg_levels)):
                for j in range(len(p_levels)):
                    val = pivot.values[i, j]
                    if np.isnan(val):
                        continue
                    norm = (val - vmin) / (vmax - vmin + 1e-12)
                    txt_color = "white" if norm > 0.65 else "black"
                    ax.text(
                        j, i, f"{val:.2f}", ha="center", va="center", fontsize=9, fontweight="bold", color=txt_color
                    )

        cbar = fig.colorbar(im, ax=axes, shrink=0.9)
        cbar.set_label(info["label"])
        fig.suptitle(f'Heatmaps of {info["label"]} at Different Al Levels', fontsize=16, fontweight="bold")
        plt.savefig(outdir / f"14_heatmaps_real_{y}.png", dpi=300, bbox_inches="tight")
        plt.close()


def save_predicted_surfaces(df, responses, outdir):
    for y, info in responses.items():
        if BEST_MODEL[y] == "reduced":
            _save_surface_reduced(df, y, info["label"], outdir / f"15_predicted_surface_{y}.png")
        else:
            _save_surface_quadratic(df, y, info["label"], outdir / f"15_predicted_surface_{y}.png")


def _save_surface_reduced(df, response, response_label, save_path):
    formula = get_formula(response, "reduced")
    import statsmodels.formula.api as smf

    model = smf.ols(formula, data=df).fit()
    al_levels = sorted(df["Al"].unique())
    mg_levels = sorted(df["Mg"].unique())
    p_levels = sorted(df["P"].unique())

    grid_rows = []
    for mg in mg_levels:
        for al in al_levels:
            for p in p_levels:
                grid_rows.append({"Mg": mg, "Al": al, "P": p, "Mg_cat": str(mg), "Al_cat": str(al), "P_cat": str(p)})
    grid_df = pd.DataFrame(grid_rows)
    grid_df["predicted"] = model.predict(grid_df)

    fig, axes = plt.subplots(1, len(al_levels), figsize=(18, 5), constrained_layout=True)
    if len(al_levels) == 1:
        axes = [axes]
    vmin = grid_df["predicted"].min()
    vmax = grid_df["predicted"].max()

    for ax, al in zip(axes, al_levels):
        sub = grid_df[grid_df["Al"] == al].copy()
        pivot = sub.pivot(index="Mg", columns="P", values="predicted").reindex(index=mg_levels, columns=p_levels)
        im = ax.imshow(pivot.values, aspect="auto", origin="lower", vmin=vmin, vmax=vmax, cmap="viridis")
        ax.set_title(f"Predicted Surface at Al = {al}")
        ax.set_xlabel("P")
        ax.set_ylabel("Mg")
        ax.set_xticks(range(len(p_levels)))
        ax.set_yticks(range(len(mg_levels)))
        ax.set_xticklabels([f"{x:.2f}" for x in p_levels])
        ax.set_yticklabels([f"{x:.2f}" for x in mg_levels])

        real_sub = df[df["Al"] == al]
        ax.scatter(
            [p_levels.index(p) for p in real_sub["P"]],
            [mg_levels.index(m) for m in real_sub["Mg"]],
            s=75,
            edgecolor="white",
            linewidth=1.0,
            color="#F28E2B",
            zorder=5,
        )
        for _, row in real_sub.iterrows():
            annotate_sample_number(
                ax,
                p_levels.index(row["P"]),
                mg_levels.index(row["Mg"]),
                row["Sample"],
                fontsize=9,
                ha="center",
                va="center",
                boxed=True,
                zorder=8,
            )

    cbar = fig.colorbar(im, ax=axes, shrink=0.9)
    cbar.set_label(response_label)
    fig.suptitle(f"Predicted Response Surface (Reduced Factorial) - {response_label}", fontsize=14, fontweight="bold")
    plt.savefig(save_path, dpi=300, bbox_inches="tight")
    plt.close()


def _save_surface_quadratic(df, response, response_label, save_path):
    formula = get_formula(response, "quadratic")
    import statsmodels.formula.api as smf

    model = smf.ols(formula, data=df).fit()
    mg_grid = np.linspace(df["Mg"].min(), df["Mg"].max(), 100)
    p_grid = np.linspace(df["P"].min(), df["P"].max(), 100)
    al_levels = sorted(df["Al"].unique())

    fig, axes = plt.subplots(1, len(al_levels), figsize=(18, 5), constrained_layout=True)
    if len(al_levels) == 1:
        axes = [axes]

    for ax, al in zip(axes, al_levels):
        xx, yy = np.meshgrid(p_grid, mg_grid)
        grid = pd.DataFrame({"Mg": yy.ravel(), "Al": al, "P": xx.ravel()})
        zz = model.predict(grid).values.reshape(yy.shape)
        im = ax.contourf(xx, yy, zz, levels=24, cmap="viridis")
        ax.set_title(f"Predicted Surface at Al = {al}")
        ax.set_xlabel("P")
        ax.set_ylabel("Mg")

        sub = df[df["Al"] == al]
        ax.scatter(sub["P"], sub["Mg"], s=75, edgecolor="black", linewidth=0.8, color="#F28E2B")
        for _, row in sub.iterrows():
            annotate_sample_number(
                ax, row["P"], row["Mg"], row["Sample"], fontsize=10, ha="center", va="center", boxed=True, zorder=8
            )

    cbar = fig.colorbar(im, ax=axes, shrink=0.9)
    cbar.set_label(response_label)
    fig.suptitle(f"Predicted Response Surface (Quadratic) - {response_label}", fontsize=14, fontweight="bold")
    plt.savefig(save_path, dpi=300, bbox_inches="tight")
    plt.close()
