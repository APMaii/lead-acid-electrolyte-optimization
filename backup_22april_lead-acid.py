#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 22 19:57:12 2026

@author: apm





"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import patheffects

data= pd.read_excel('/Users/apm/Desktop/lead_acid_data.xlsx')


data.head()
'''
   Sample  MgSO4.7H2O (wt.%)  AlSO4.18H2O (wt.%)  ...    Rct       CPE      w
0       1                0.0                0.00  ...  23.81  0.000299  0.122
1       2                0.0                0.00  ...    NaN       NaN    NaN
2       3                0.0                0.00  ...    NaN       NaN    NaN
3       4                0.0                0.25  ...    NaN       NaN    NaN
4       5                0.0                0.25  ...    NaN       NaN    NaN

[5 rows x 12 columns]
'''

data.columns
'''
Index(['Sample', 'MgSO4.7H2O (wt.%)', 'AlSO4.18H2O (wt.%)',
       'Phosphoric Acid (wt.%)', 'Reversibility Ratio ',
       'Reversibility Energy', 'Overpotential', 'Resistance Ct', 'Rs', 'Rct',
       'CPE', 'w'],
      dtype='object')

'''



data.columns = [c.strip() for c in data.columns]



data.columns
'''
Index(['Sample', 'MgSO4.7H2O (wt.%)', 'AlSO4.18H2O (wt.%)',
       'Phosphoric Acid (wt.%)', 'Reversibility Ratio', 'Reversibility Energy',
       'Overpotential', 'Resistance Ct', 'Rs', 'Rct', 'CPE', 'w'],
      dtype='object')

'''




df = data.rename(columns={
    'Reversibility Ratio': 'RevRatio',
    'Reversibility Ratio ': 'RevRatio',
    'Reversibility Energy': 'DeltaE',
    'Resistance Ct': 'ResistanceCt'
})

# -----------------------------
# Global style
# -----------------------------
plt.rcParams['figure.figsize'] = (16, 8)
plt.rcParams['font.size'] = 11
plt.rcParams['axes.titlesize'] = 17
plt.rcParams['axes.labelsize'] = 13
plt.rcParams['xtick.labelsize'] = 10
plt.rcParams['ytick.labelsize'] = 11

metrics = [
    ('RevRatio', 'Reversibility Ratio (IR/IO)', 'Higher is better'),
    ('DeltaE', 'Delta E (mV)', 'Lower is better'),
    ('Overpotential', 'Overpotential', 'Higher is better'),
    ('ResistanceCt', 'Resistance Ct (Ω)', 'Lower is better')
]

for col, ylabel, note in metrics:
    fig, ax = plt.subplots()

    values = df[col].values
    x = np.arange(len(df))

    bars = ax.bar(
        x,
        values,
        width=0.72,
        edgecolor='black',
        linewidth=0.8,
        zorder=3
    )

    # Highlight best 3 bars
    if col in ['DeltaE', 'ResistanceCt']:
        best_idx = df.nsmallest(3, col).index
    else:
        best_idx = df.nlargest(3, col).index

    for i in best_idx:
        bars[i].set_linewidth(2.2)

    # Axis labels and title
    ax.set_title(f'{ylabel} Across 27 Electrolyte Samples', fontweight='bold', pad=16)
    ax.set_xlabel('Sample', fontweight='bold')
    ax.set_ylabel(ylabel, fontweight='bold')

    ax.set_xticks(x)
    ax.set_xticklabels(df['Sample'])

    # Grid
    ax.grid(axis='y', linestyle='--', alpha=0.30, zorder=0)
    ax.set_axisbelow(True)

    # Clean top/right spines
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    # Nice y-limits
    y_min = np.nanmin(values)
    y_max = np.nanmax(values)
    margin = (y_max - y_min) * 0.15 if y_max != y_min else 0.1

    if col in ['RevRatio', 'Overpotential']:
        ax.set_ylim(y_min - margin * 0.15, y_max + margin)
    else:
        ax.set_ylim(0, y_max + margin)

    # Add horizontal values on bars
    for i, bar in enumerate(bars):
        height = bar.get_height()

        if pd.isna(height):
            continue

        if col == 'Overpotential':
            txt = f'{height:.3f}'
        elif col == 'RevRatio':
            txt = f'{height:.2f}'
        else:
            txt = f'{height:.2f}'

        # Position inside or just above depending on bar height
        if col in ['DeltaE', 'ResistanceCt']:
            y_text = height - (ax.get_ylim()[1] * 0.03)
            va = 'top'
        else:
            y_text = height + (ax.get_ylim()[1] * 0.01)
            va = 'bottom'

        ax.text(
            bar.get_x() + bar.get_width() / 2,
            y_text,
            txt,
            ha='center',
            va=va,
            rotation=0,   # horizontal
            fontsize=9,
            fontweight='bold'
        )

    # Annotate best 3
    for i in best_idx:
        bar = bars[i]
        height = bar.get_height()
        ax.annotate(
            f'Best: S{df.loc[i, "Sample"]}',
            xy=(bar.get_x() + bar.get_width() / 2, height),
            xytext=(0, 14),
            textcoords='offset points',
            ha='center',
            va='bottom',
            fontsize=10,
            fontweight='bold',
            arrowprops=dict(arrowstyle='-', lw=1.0)
        )

    # Add performance note
    ax.text(
        0.99, 0.98, note,
        transform=ax.transAxes,
        ha='right',
        va='top',
        fontsize=10,
        bbox=dict(
            boxstyle='round,pad=0.35',
            facecolor='white',
            edgecolor='gray',
            alpha=0.95
        )
    )

    plt.tight_layout()
    plt.show()



data.columns

'''
Index(['Sample', 'MgSO4.7H2O (wt.%)', 'AlSO4.18H2O (wt.%)',
       'Phosphoric Acid (wt.%)', 'Reversibility Ratio', 'Reversibility Energy',
       'Overpotential', 'Resistance Ct', 'Rs', 'Rct', 'CPE', 'w'],
      dtype='object')

'''
df = data.rename(columns={
    'Reversibility Ratio': 'Reversibility (Ir/Io)',
    'Reversibility Energy': 'Reversibility (Er-Eo)',
    'Overpotential': '-Overpotential at -10mA',
    'Resistance Ct': 'R_ct'
})



import itertools
from pathlib import Path

import statsmodels.api as sm
import statsmodels.formula.api as smf
from statsmodels.stats.anova import anova_lm


# Keep only needed columns
df = df[['Sample',
         'MgSO4.7H2O (wt.%)',
         'AlSO4.18H2O (wt.%)',
         'Phosphoric Acid (wt.%)',
         'Reversibility (Ir/Io)',
         'Reversibility (Er-Eo)',
         '-Overpotential at -10mA',
         'R_ct']].copy()

# Safer names for modeling
df = df.rename(columns={
    'MgSO4.7H2O (wt.%)': 'Mg',
    'AlSO4.18H2O (wt.%)': 'Al',
    'Phosphoric Acid (wt.%)': 'P',
    'Reversibility (Ir/Io)': 'RevRatio',
    'Reversibility (Er-Eo)': 'DeltaE',
    '-Overpotential at -10mA': 'Overpot',
    'R_ct': 'Rct'
})



#final check

df.columns

'''
Out[40]: Index(['Sample', 'Mg', 'Al', 'P', 'RevRatio', 'DeltaE', 'Overpot', 'Rct'], dtype='object')

'''


df.head()




# Factor levels as categories too
df['Mg_cat'] = df['Mg'].astype(str)
df['Al_cat'] = df['Al'].astype(str)
df['P_cat']  = df['P'].astype(str)

# Output folder
outdir = Path('/Users/apm/Desktop/lead-acid-code/lead_acid_stats_outputs')
outdir.mkdir(parents=True, exist_ok=True)


# --------------------------------------------------
# 2) GLOBAL STYLE
# --------------------------------------------------
plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams['figure.figsize'] = (12, 7)
plt.rcParams['font.size'] = 11
plt.rcParams['axes.titlesize'] = 16
plt.rcParams['axes.labelsize'] = 12
plt.rcParams['xtick.labelsize'] = 10
plt.rcParams['ytick.labelsize'] = 10
plt.rcParams['axes.titleweight'] = 'bold'
plt.rcParams['axes.linewidth'] = 1.2
plt.rcParams['grid.alpha'] = 0.35
plt.rcParams['grid.linestyle'] = '--'
plt.rcParams['savefig.dpi'] = 400
plt.rcParams['figure.dpi'] = 140

SAMPLE_TEXT_COLOR = '#0B3D91'
SAMPLE_TEXT_STROKE = [patheffects.withStroke(linewidth=2.2, foreground='white')]


def annotate_sample_number(
    ax, x, y, sample_id, *, fontsize=9, ha='left', va='bottom', boxed=False, zorder=6
):
    text = ax.text(
        x,
        y,
        str(int(sample_id)),
        fontsize=fontsize,
        color=SAMPLE_TEXT_COLOR,
        fontweight='bold',
        ha=ha,
        va=va,
        zorder=zorder
    )
    text.set_path_effects(SAMPLE_TEXT_STROKE)
    if boxed:
        text.set_bbox(dict(facecolor='white', edgecolor='black', alpha=0.78, boxstyle='round,pad=0.16'))

responses = {
    'RevRatio': {'label': 'Reversibility (Ir/Io)', 'goal': 'max'},
    'DeltaE':   {'label': 'Reversibility (Er-Eo)', 'goal': 'min'},
    'Overpot':  {'label': '-Overpotential at -10mA', 'goal': 'max'},
    'Rct':      {'label': 'R_ct', 'goal': 'min'}
}



# --------------------------------------------------
# 3) DESCRIPTIVE STATISTICS
# --------------------------------------------------
desc = df[['RevRatio', 'DeltaE', 'Overpot', 'Rct']].describe().T
desc['range'] = desc['max'] - desc['min']
desc.to_excel(outdir / '01_descriptive_statistics.xlsx')




# --------------------------------------------------
# 4) CORRELATION HEATMAP (MATPLOTLIB ONLY)
# --------------------------------------------------
corr = df[['RevRatio', 'DeltaE', 'Overpot', 'Rct', 'Mg', 'Al', 'P']].corr()
fig, ax = plt.subplots(figsize=(10, 8))
im = ax.imshow(corr.values, aspect='auto', cmap='RdBu_r', vmin=-1, vmax=1)
ax.set_xticks(range(len(corr.columns)))
ax.set_yticks(range(len(corr.columns)))
ax.set_xticklabels(corr.columns, rotation=45, ha='right')
ax.set_yticklabels(corr.columns)
ax.set_title('Correlation Matrix')
for i in range(corr.shape[0]):
    for j in range(corr.shape[1]):
        val = corr.iloc[i, j]
        txt_color = 'white' if abs(val) > 0.55 else 'black'
        ax.text(j, i, f'{val:.2f}', ha='center', va='center', fontsize=9, fontweight='bold', color=txt_color)
fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
plt.tight_layout()
plt.savefig(outdir / '02_correlation_matrix.png', dpi=300, bbox_inches='tight')
plt.close()



# --------------------------------------------------
# 5) DISTRIBUTION FIGURES (HISTOGRAMS)
# --------------------------------------------------
for y, info in responses.items():
    fig, ax = plt.subplots()
    vals = df[y].dropna()
    ax.hist(vals, bins=8, edgecolor='black')
    ax.axvline(vals.mean(), linestyle='--', linewidth=1.5, label=f"Mean = {vals.mean():.3f}")
    ax.axvline(vals.median(), linestyle=':', linewidth=1.5, label=f"Median = {vals.median():.3f}")
    ax.set_title(f'Distribution of {info["label"]}')
    ax.set_xlabel(info['label'])
    ax.set_ylabel('Frequency')
    ax.legend()
    ax.grid(alpha=0.25)
    plt.tight_layout()
    plt.savefig(outdir / f'03_hist_{y}.png', dpi=300, bbox_inches='tight')
    plt.close()



# --------------------------------------------------
# 6) MAIN EFFECT PLOTS
# --------------------------------------------------
def main_effect_plot(data, factor, response, response_label, filename):
    grouped = data.groupby(factor)[response].mean().reset_index()
    x = grouped[factor].astype(float)
    y = grouped[response]

    fig, ax = plt.subplots()
    ax.plot(x, y, marker='o', linewidth=2)
    for xi, yi in zip(x, y):
        ax.text(xi, yi, f'{yi:.3f}', ha='center', va='bottom', fontsize=10)
    ax.set_title(f'Main Effect of {factor} on {response_label}')
    ax.set_xlabel(factor)
    ax.set_ylabel(response_label)
    ax.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    plt.close()

for y, info in responses.items():
    main_effect_plot(df, 'Mg', y, info['label'], outdir / f'04_main_effect_Mg_{y}.png')
    main_effect_plot(df, 'Al', y, info['label'], outdir / f'04_main_effect_Al_{y}.png')
    main_effect_plot(df, 'P',  y, info['label'], outdir / f'04_main_effect_P_{y}.png')



# --------------------------------------------------
# 7) INTERACTION PLOTS
# --------------------------------------------------
def interaction_plot_custom(data, factor1, factor2, response, response_label, filename):
    grouped = data.groupby([factor1, factor2])[response].mean().reset_index()
    levels1 = sorted(grouped[factor1].unique())
    levels2 = sorted(grouped[factor2].unique())

    fig, ax = plt.subplots()
    for lev2 in levels2:
        sub = grouped[grouped[factor2] == lev2].sort_values(factor1)
        ax.plot(sub[factor1], sub[response], marker='o', linewidth=2, label=f'{factor2}={lev2}')
    ax.set_title(f'Interaction Plot: {factor1} × {factor2} on {response_label}')
    ax.set_xlabel(factor1)
    ax.set_ylabel(response_label)
    ax.legend(title=factor2)
    ax.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    plt.close()

pairs = [('Mg', 'Al'), ('Mg', 'P'), ('Al', 'P')]
for y, info in responses.items():
    for f1, f2 in pairs:
        interaction_plot_custom(df, f1, f2, y, info['label'],
                                outdir / f'05_interaction_{f1}_{f2}_{y}.png')



# --------------------------------------------------
# 8) FULL FACTORIAL CATEGORICAL MODEL + ANOVA
# --------------------------------------------------

#***** NOOOOO
anova_writer = pd.ExcelWriter(outdir / '06_factorial_anova_results.xlsx', engine='openpyxl')

for y, info in responses.items():
    # Categorical factorial model
    formula = f'{y} ~ C(Mg_cat) * C(Al_cat) * C(P_cat)'
    model = smf.ols(formula, data=df).fit()
    try:
        anova_tbl = anova_lm(model, typ=2)
    except:
        anova_tbl = anova_lm(model, typ=1)

    coef_tbl = pd.DataFrame({
        'term': model.params.index,
        'coef': model.params.values,
        'pvalue': model.pvalues.values
    })

    coef_tbl.to_excel(anova_writer, sheet_name=f'{y}_coef', index=False)
    anova_tbl.to_excel(anova_writer, sheet_name=f'{y}_anova')

anova_writer.close()


# -----------------------------
# 8A) Reduced categorical factorial model
# main effects + two-way interactions only
# -----------------------------
anova_writer = pd.ExcelWriter(outdir / '08_reduced_factorial_anova_results.xlsx', engine='openpyxl')

reduced_model_summary = []

for y, info in responses.items():
    formula = (
        f'{y} ~ C(Mg_cat) + C(Al_cat) + C(P_cat)'
        f' + C(Mg_cat):C(Al_cat)'
        f' + C(Mg_cat):C(P_cat)'
        f' + C(Al_cat):C(P_cat)'
    )

    model = smf.ols(formula, data=df).fit()
    anova_tbl = anova_lm(model, typ=2)

    coef_tbl = pd.DataFrame({
        'term': model.params.index,
        'coef': model.params.values,
        'pvalue': model.pvalues.values
    })

    fit_tbl = pd.DataFrame([{
        'response': y,
        'R2': model.rsquared,
        'Adj_R2': model.rsquared_adj,
        'AIC': model.aic,
        'BIC': model.bic,
        'df_model': model.df_model,
        'df_resid': model.df_resid
    }])

    coef_tbl.to_excel(anova_writer, sheet_name=f'{y}_coef', index=False)
    anova_tbl.to_excel(anova_writer, sheet_name=f'{y}_anova')
    fit_tbl.to_excel(anova_writer, sheet_name=f'{y}_fit', index=False)

    reduced_model_summary.append({
        'response': y,
        'R2': model.rsquared,
        'Adj_R2': model.rsquared_adj,
        'AIC': model.aic,
        'BIC': model.bic,
        'df_model': model.df_model,
        'df_resid': model.df_resid
    })

anova_writer.close()

reduced_model_summary_df = pd.DataFrame(reduced_model_summary)
reduced_model_summary_df.to_excel(outdir / '08_reduced_factorial_model_summary.xlsx', index=False)



# -----------------------------
# 8B) Quadratic numeric response-surface model
# This is usually the better model for your case
# -----------------------------
quad_writer = pd.ExcelWriter(outdir / '09_quadratic_models.xlsx', engine='openpyxl')

quad_model_summary = []

for y, info in responses.items():
    formula_quad = f'''
    {y} ~ Mg + Al + P
        + I(Mg**2) + I(Al**2) + I(P**2)
        + Mg:Al + Mg:P + Al:P
    '''

    model = smf.ols(formula_quad, data=df).fit()
    anova_tbl = anova_lm(model, typ=2)

    coef_tbl = pd.DataFrame({
        'term': model.params.index,
        'coef': model.params.values,
        'pvalue': model.pvalues.values
    })

    fit_tbl = pd.DataFrame([{
        'response': y,
        'R2': model.rsquared,
        'Adj_R2': model.rsquared_adj,
        'AIC': model.aic,
        'BIC': model.bic,
        'df_model': model.df_model,
        'df_resid': model.df_resid
    }])

    coef_tbl.to_excel(quad_writer, sheet_name=f'{y}_coef', index=False)
    anova_tbl.to_excel(quad_writer, sheet_name=f'{y}_anova')
    fit_tbl.to_excel(quad_writer, sheet_name=f'{y}_fit', index=False)

    quad_model_summary.append({
        'response': y,
        'R2': model.rsquared,
        'Adj_R2': model.rsquared_adj,
        'AIC': model.aic,
        'BIC': model.bic,
        'df_model': model.df_model,
        'df_resid': model.df_resid
    })

quad_writer.close()

quad_model_summary_df = pd.DataFrame(quad_model_summary)
quad_model_summary_df.to_excel(outdir / '09_quadratic_model_summary.xlsx', index=False)



# --------------------------------------------------
# 9) MODEL COMPARISON TABLE
# --------------------------------------------------
comparison_rows = []
for y in responses.keys():
    red_row = reduced_model_summary_df[reduced_model_summary_df['response'] == y].iloc[0]
    quad_row = quad_model_summary_df[quad_model_summary_df['response'] == y].iloc[0]

    comparison_rows.append({
        'response': y,
        'reduced_R2': red_row['R2'],
        'quad_R2': quad_row['R2'],
        'reduced_Adj_R2': red_row['Adj_R2'],
        'quad_Adj_R2': quad_row['Adj_R2'],
        'reduced_AIC': red_row['AIC'],
        'quad_AIC': quad_row['AIC'],
        'reduced_BIC': red_row['BIC'],
        'quad_BIC': quad_row['BIC'],
        'preferred_model_by_AdjR2': 'quadratic' if quad_row['Adj_R2'] > red_row['Adj_R2'] else 'reduced_factorial'
    })

comparison_df = pd.DataFrame(comparison_rows)
comparison_df.to_excel(outdir / '10_model_comparison.xlsx', index=False)



#=====================================================
#=====================================================
#=====================================================
#=====================================================
#=====================================================
#=====================================================
#=====================================================
#=====================================================
#=====================================================
#=====================================================
#============= (QUADRATIC  MODELS) ==================
#=====================================================
#=====================================================
#=====================================================
#=====================================================
#=====================================================
#=====================================================
#=====================================================
#=====================================================
#=====================================================
#=====================================================

# --------------------------------------------------
# 10) OBSERVED VS PREDICTED PLOTS (quadratic model)
# --------------------------------------------------
for y, info in responses.items():
    formula_quad = f'''
    {y} ~ Mg + Al + P
        + I(Mg**2) + I(Al**2) + I(P**2)
        + Mg:Al + Mg:P + Al:P
    '''
    model = smf.ols(formula_quad, data=df).fit()
    pred = model.predict(df)

    fig, ax = plt.subplots(figsize=(8, 6))
    ax.scatter(df[y], pred, s=85, edgecolor='black', linewidth=0.8, color='#4C72B0', alpha=0.9)

    mn = min(df[y].min(), pred.min())
    mx = max(df[y].max(), pred.max())
    ax.plot([mn, mx], [mn, mx], linestyle='--', linewidth=1.8, color='#DD8452')

    for i, row in df.iterrows():
        annotate_sample_number(
            ax,
            row[y],
            pred.iloc[i],
            row['Sample'],
            fontsize=9,
            ha='left',
            va='bottom'
        )

    ax.set_title(f'Observed vs Predicted ({info["label"]})')
    ax.set_xlabel('Observed')
    ax.set_ylabel('Predicted')
    ax.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(outdir / f'11_observed_vs_predicted_{y}.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    
# --------------------------------------------------
# 11) RESIDUAL PLOTS (quadratic model)
# --------------------------------------------------
for y, info in responses.items():
    formula_quad = f'''
    {y} ~ Mg + Al + P
        + I(Mg**2) + I(Al**2) + I(P**2)
        + Mg:Al + Mg:P + Al:P
    '''
    model = smf.ols(formula_quad, data=df).fit()

    fitted = model.fittedvalues
    resid = model.resid

    fig, ax = plt.subplots(figsize=(8, 6))
    ax.scatter(fitted, resid, s=85, edgecolor='black', linewidth=0.8, color='#55A868', alpha=0.9)
    ax.axhline(0, linestyle='--', linewidth=1.8, color='#C44E52')

    for i, s in enumerate(df['Sample']):
        annotate_sample_number(ax, fitted.iloc[i], resid.iloc[i], s, fontsize=9, ha='left', va='bottom')

    ax.set_title(f'Residual Plot ({info["label"]})')
    ax.set_xlabel('Fitted')
    ax.set_ylabel('Residual')
    ax.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(outdir / f'12_residual_plot_{y}.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    
# --------------------------------------------------
# 12) Q-Q PLOTS OF RESIDUALS (quadratic model)
# --------------------------------------------------
import statsmodels.api as sm

for y, info in responses.items():
    formula_quad = f'''
    {y} ~ Mg + Al + P
        + I(Mg**2) + I(Al**2) + I(P**2)
        + Mg:Al + Mg:P + Al:P
    '''
    model = smf.ols(formula_quad, data=df).fit()

    fig = plt.figure(figsize=(7, 6))
    ax = fig.add_subplot(111)
    sm.qqplot(model.resid, line='45', ax=ax, markerfacecolor='none', markeredgecolor='black')
    ax.set_title(f'Q-Q Plot of Residuals ({info["label"]})')
    plt.tight_layout()
    plt.savefig(outdir / f'13_qqplot_{y}.png', dpi=300, bbox_inches='tight')
    plt.close()
    


# --------------------------------------------------
# 13) HEATMAPS OF REAL DATA
# x = P, y = Mg, separate panel for each Al level
# --------------------------------------------------
def make_heatmaps(data, response, response_label, save_path):
    al_levels = sorted(data['Al'].unique())
    mg_levels = sorted(data['Mg'].unique())
    p_levels = sorted(data['P'].unique())

    fig, axes = plt.subplots(1, len(al_levels), figsize=(18, 5), constrained_layout=True)
    if len(al_levels) == 1:
        axes = [axes]

    vmin = data[response].min()
    vmax = data[response].max()

    for ax, al in zip(axes, al_levels):
        sub = data[data['Al'] == al].copy()
        pivot = sub.pivot(index='Mg', columns='P', values=response).reindex(index=mg_levels, columns=p_levels)

        im = ax.imshow(pivot.values, aspect='auto', origin='lower', vmin=vmin, vmax=vmax, cmap='YlGnBu')
        ax.set_title(f'Al = {al}')
        ax.set_xlabel('P')
        ax.set_ylabel('Mg')
        ax.set_xticks(range(len(p_levels)))
        ax.set_yticks(range(len(mg_levels)))
        ax.set_xticklabels([f'{x:.2f}' for x in p_levels])
        ax.set_yticklabels([f'{x:.2f}' for x in mg_levels])

        for i in range(len(mg_levels)):
            for j in range(len(p_levels)):
                val = pivot.values[i, j]
                if np.isnan(val):
                    continue
                norm = (val - vmin) / (vmax - vmin + 1e-12)
                txt_color = 'white' if norm > 0.65 else 'black'
                ax.text(
                    j,
                    i,
                    f'{val:.2f}',
                    ha='center',
                    va='center',
                    fontsize=9,
                    fontweight='bold',
                    color=txt_color
                )

    cbar = fig.colorbar(im, ax=axes, shrink=0.9)
    cbar.set_label(response_label)
    fig.suptitle(f'Heatmaps of {response_label} at Different Al Levels', fontsize=16, fontweight='bold')
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.close()

for y, info in responses.items():
    make_heatmaps(
        df,
        response=y,
        response_label=info['label'],
        save_path=outdir / f'14_heatmaps_real_{y}.png'
    )



# --------------------------------------------------
# 14) PREDICTED RESPONSE SURFACE HEATMAPS (quadratic model)
# On a fine grid for each Al level
# --------------------------------------------------
def make_predicted_surface_heatmaps(data, response, response_label, save_path):
    formula_quad = f'''
    {response} ~ Mg + Al + P
        + I(Mg**2) + I(Al**2) + I(P**2)
        + Mg:Al + Mg:P + Al:P
    '''
    model = smf.ols(formula_quad, data=data).fit()

    mg_grid = np.linspace(data['Mg'].min(), data['Mg'].max(), 100)
    p_grid = np.linspace(data['P'].min(), data['P'].max(), 100)
    al_levels = sorted(data['Al'].unique())

    fig, axes = plt.subplots(1, len(al_levels), figsize=(18, 5), constrained_layout=True)
    if len(al_levels) == 1:
        axes = [axes]

    for ax, al in zip(axes, al_levels):
        XX, YY = np.meshgrid(p_grid, mg_grid)
        grid = pd.DataFrame({
            'Mg': YY.ravel(),
            'Al': al,
            'P': XX.ravel()
        })
        ZZ = model.predict(grid).values.reshape(YY.shape)

        im = ax.contourf(XX, YY, ZZ, levels=24, cmap='viridis')
        ax.set_title(f'Predicted Surface at Al = {al}')
        ax.set_xlabel('P')
        ax.set_ylabel('Mg')

        # overlay real points
        sub = data[data['Al'] == al]
        ax.scatter(sub['P'], sub['Mg'], s=75, edgecolor='black', linewidth=0.8, color='#F28E2B')

        for _, row in sub.iterrows():
            annotate_sample_number(ax, row['P'], row['Mg'], row['Sample'], fontsize=9, ha='center', va='center')

    cbar = fig.colorbar(im, ax=axes, shrink=0.9)
    cbar.set_label(response_label)
    fig.suptitle(f'Predicted Response Surfaces for {response_label}', fontsize=16, fontweight='bold')
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.close()

for y, info in responses.items():
    make_predicted_surface_heatmaps(
        df,
        response=y,
        response_label=info['label'],
        save_path=outdir / f'15_predicted_surface_{y}.png'
    )
    
    
    
# --------------------------------------------------
# 15) EFFECT SIZE SUMMARY FROM QUADRATIC MODELS
# --------------------------------------------------
effect_writer = pd.ExcelWriter(outdir / '16_effect_size_summary.xlsx', engine='openpyxl')

for y, info in responses.items():
    formula_quad = f'''
    {y} ~ Mg + Al + P
        + I(Mg**2) + I(Al**2) + I(P**2)
        + Mg:Al + Mg:P + Al:P
    '''
    model = smf.ols(formula_quad, data=df).fit()
    anova_tbl = anova_lm(model, typ=2).copy()

    # Partial eta squared approximation
    if 'sum_sq' in anova_tbl.columns:
        ss_resid = anova_tbl.loc['Residual', 'sum_sq']
        anova_tbl['partial_eta_sq'] = anova_tbl['sum_sq'] / (anova_tbl['sum_sq'] + ss_resid)

    anova_tbl.to_excel(effect_writer, sheet_name=f'{y}_effect_sizes')

effect_writer.close()


# --------------------------------------------------
# 16) COMPOSITE SCORE (multi-response optimization)
# --------------------------------------------------
opt = df.copy()

def zscore(x):
    return (x - x.mean()) / x.std(ddof=0)

opt['RevRatio_z'] = zscore(opt['RevRatio'])
opt['DeltaE_good'] = zscore(-opt['DeltaE'])   # smaller is better
opt['Overpot_z'] = zscore(opt['Overpot'])
opt['Rct_good'] = zscore(-opt['Rct'])         # smaller is better

opt['CompositeScore'] = opt[['RevRatio_z', 'DeltaE_good', 'Overpot_z', 'Rct_good']].mean(axis=1)
opt = opt.sort_values('CompositeScore', ascending=False)

opt[['Sample', 'Mg', 'Al', 'P', 'RevRatio', 'DeltaE', 'Overpot', 'Rct', 'CompositeScore']] \
    .to_excel(outdir / '17_composite_score_ranking.xlsx', index=False)

fig, ax = plt.subplots(figsize=(14, 8))
bars = ax.bar(opt['Sample'].astype(str), opt['CompositeScore'], edgecolor='black', linewidth=0.8)

for i in range(min(5, len(opt))):
    bars[i].set_linewidth(2.0)

for bar, val in zip(bars, opt['CompositeScore']):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height(), f'{val:.2f}',
            ha='center', va='bottom', fontsize=9)

ax.set_title('Composite Performance Score Ranking')
ax.set_xlabel('Sample')
ax.set_ylabel('Composite Score')
ax.grid(axis='y', alpha=0.3)
ax.set_axisbelow(True)
plt.tight_layout()
plt.savefig(outdir / '18_composite_score_bar_chart.png', dpi=300, bbox_inches='tight')
plt.close()




# --------------------------------------------------
# 17) BEST SAMPLE MAPS
# --------------------------------------------------
for y, info in responses.items():
    if info['goal'] == 'max':
        best_row = df.loc[df[y].idxmax()]
    else:
        best_row = df.loc[df[y].idxmin()]

    fig, ax = plt.subplots(figsize=(8, 6))
    sc = ax.scatter(df['Mg'], df['P'], s=150, c=df[y], edgecolor='black', linewidth=0.8, cmap='plasma')
    ax.scatter(best_row['Mg'], best_row['P'], s=340, marker='*', edgecolor='black', linewidth=1.2, color='#FFD700')

    for _, row in df.iterrows():
        annotate_sample_number(ax, row['Mg'], row['P'], row['Sample'], fontsize=9, ha='center', va='center')

    ax.set_title(f'Composition Map for {info["label"]} (Best Sample Marked)')
    ax.set_xlabel('Mg')
    ax.set_ylabel('P')
    cbar = plt.colorbar(sc, ax=ax)
    cbar.set_label(info['label'])
    plt.tight_layout()
    plt.savefig(outdir / f'19_best_sample_map_{y}.png', dpi=300, bbox_inches='tight')
    plt.close()



# --------------------------------------------------
# 18) PRINT SUMMARY
# --------------------------------------------------
print("=" * 80)
print("Statistical analysis complete.")
print(f"All outputs saved in:\n{outdir}")
print("=" * 80)

print("\nModel comparison:")
print(comparison_df.to_string(index=False))

print("\nTop 10 samples by composite score:")
print(opt[['Sample', 'Mg', 'Al', 'P', 'CompositeScore']].head(10).to_string(index=False))


'''
================================================================================
Statistical analysis complete.
All outputs saved in:
/Users/apm/Desktop/lead-acid-code/lead_acid_stats_outputs
================================================================================

Model comparison:
response  reduced_R2  quad_R2  reduced_Adj_R2  quad_Adj_R2  reduced_AIC    quad_AIC  reduced_BIC    quad_BIC preferred_model_by_AdjR2
RevRatio    0.821569 0.347694        0.420099     0.002356   -92.783835  -75.783440   -68.162934  -62.825071        reduced_factorial
  DeltaE    0.645051 0.355956       -0.153584     0.014991   170.647149  168.733577   195.268049  181.691945                quadratic
 Overpot    0.761282 0.382086        0.224168     0.054955  -130.797739 -123.118896  -106.176839 -110.160527        reduced_factorial
     Rct    0.776560 0.427567        0.273821     0.124515   240.213004  247.613343   264.833905  260.571712        reduced_factorial

Top 10 samples by composite score:
 Sample   Mg   Al   P  CompositeScore
     15 0.15 0.25 0.2        1.050693
     27 0.30 0.50 0.2        1.024134
     11 0.15 0.00 0.1        0.809962
      8 0.00 0.50 0.1        0.795598
     13 0.15 0.25 0.0        0.453538
      9 0.00 0.50 0.2        0.448487
     25 0.30 0.50 0.0        0.403741
      7 0.00 0.50 0.0        0.346297
     26 0.30 0.50 0.1        0.332183
     22 0.30 0.25 0.0        0.128005
'''


#=====================================================
#=====================================================
#=====================================================
#=====================================================
#=====================================================
#=====================================================
#=====================================================
#=====================================================
#=====================================================
#=====================================================
#=====================================================
#=====================================================
#=====================================================
#=====================================================
#=====================================================
#=====================================================
#=====================================================
#=====================================================
#=====================================================
#=====================================================

#=====================================================
#=====================================================
#=====================================================
#=====================================================
#=====================================================
#=====================================================
#=====================================================
#=====================================================
#=====================================================
#=====================================================

#=====================================================
#=====================================================
#=====================================================
#=====================================================
#=====================================================
#=====================================================
#=====================================================
#=====================================================
#=====================================================
#=====================================================

# --------------------------------------------------
# MODEL ASSIGNMENT
# Based on model comparison (Section 3.1.5):
#   Reduced factorial wins for: RevRatio, Overpot, Rct
#   Quadratic wins for:         DeltaE
# --------------------------------------------------
BEST_MODEL = {
    'RevRatio': 'reduced',
    'DeltaE':   'quadratic',
    'Overpot':  'reduced',
    'Rct':      'reduced'
}

def get_formula(y, model_type):
    """Return the correct formula string for the given response and model type."""
    if model_type == 'reduced':
        return (
            f'{y} ~ C(Mg_cat) + C(Al_cat) + C(P_cat)'
            f' + C(Mg_cat):C(Al_cat)'
            f' + C(Mg_cat):C(P_cat)'
            f' + C(Al_cat):C(P_cat)'
        )
    else:  # quadratic
        return (
            f'{y} ~ Mg + Al + P'
            f' + I(Mg**2) + I(Al**2) + I(P**2)'
            f' + Mg:Al + Mg:P + Al:P'
        )

def fit_best_model(y):
    """Fit and return the best model for response y."""
    formula = get_formula(y, BEST_MODEL[y])
    return smf.ols(formula, data=df).fit()


# --------------------------------------------------
# 10) OBSERVED VS PREDICTED PLOTS (best model per response)
# --------------------------------------------------
for y, info in responses.items():
    model = fit_best_model(y)
    pred  = model.predict(df)

    fig, ax = plt.subplots(figsize=(8, 6))
    ax.scatter(df[y], pred, s=85, edgecolor='black',
               linewidth=0.8, color='#4C72B0', alpha=0.9)

    mn = min(df[y].min(), pred.min())
    mx = max(df[y].max(), pred.max())
    ax.plot([mn, mx], [mn, mx], linestyle='--', linewidth=1.8, color='#DD8452')

    for i, row in df.iterrows():
        annotate_sample_number(ax, row[y], pred.iloc[i],
                               row['Sample'], fontsize=9, ha='left', va='bottom')

    model_label = 'Reduced Factorial' if BEST_MODEL[y] == 'reduced' else 'Quadratic'
    ax.set_title(f'Observed vs Predicted — {info["label"]}\n({model_label} Model)')
    ax.set_xlabel('Observed')
    ax.set_ylabel('Predicted')
    ax.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(outdir / f'11_observed_vs_predicted_{y}.png', dpi=300, bbox_inches='tight')
    plt.close()
    print(f'[10] Saved: 11_observed_vs_predicted_{y}.png  [{model_label}]')


# --------------------------------------------------
# 11) RESIDUAL PLOTS (best model per response)
# --------------------------------------------------
for y, info in responses.items():
    model  = fit_best_model(y)
    fitted = model.fittedvalues
    resid  = model.resid

    fig, ax = plt.subplots(figsize=(8, 6))
    ax.scatter(fitted, resid, s=85, edgecolor='black',
               linewidth=0.8, color='#55A868', alpha=0.9)
    ax.axhline(0, linestyle='--', linewidth=1.8, color='#C44E52')

    for i, s in enumerate(df['Sample']):
        annotate_sample_number(ax, fitted.iloc[i], resid.iloc[i],
                               s, fontsize=9, ha='left', va='bottom')

    model_label = 'Reduced Factorial' if BEST_MODEL[y] == 'reduced' else 'Quadratic'
    ax.set_title(f'Residual Plot — {info["label"]}\n({model_label} Model)')
    ax.set_xlabel('Fitted')
    ax.set_ylabel('Residual')
    ax.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(outdir / f'12_residual_plot_{y}.png', dpi=300, bbox_inches='tight')
    plt.close()
    print(f'[11] Saved: 12_residual_plot_{y}.png  [{model_label}]')


# --------------------------------------------------
# 12) Q-Q PLOTS OF RESIDUALS (best model per response)
# --------------------------------------------------
for y, info in responses.items():
    model = fit_best_model(y)

    fig = plt.figure(figsize=(7, 6))
    ax  = fig.add_subplot(111)
    sm.qqplot(model.resid, line='45', ax=ax,
              markerfacecolor='none', markeredgecolor='black')

    model_label = 'Reduced Factorial' if BEST_MODEL[y] == 'reduced' else 'Quadratic'
    ax.set_title(f'Q-Q Plot of Residuals — {info["label"]}\n({model_label} Model)')
    plt.tight_layout()
    plt.savefig(outdir / f'13_qqplot_{y}.png', dpi=300, bbox_inches='tight')
    plt.close()
    print(f'[12] Saved: 13_qqplot_{y}.png  [{model_label}]')


# --------------------------------------------------
# 13) HEATMAPS OF REAL DATA
# (unchanged — these show raw data, no model needed)
# --------------------------------------------------
def make_heatmaps(data, response, response_label, save_path):
    al_levels = sorted(data['Al'].unique())
    mg_levels = sorted(data['Mg'].unique())
    p_levels  = sorted(data['P'].unique())

    fig, axes = plt.subplots(1, len(al_levels), figsize=(18, 5), constrained_layout=True)
    if len(al_levels) == 1:
        axes = [axes]

    vmin = data[response].min()
    vmax = data[response].max()

    for ax, al in zip(axes, al_levels):
        sub   = data[data['Al'] == al].copy()
        pivot = sub.pivot(index='Mg', columns='P', values=response)\
                   .reindex(index=mg_levels, columns=p_levels)

        im = ax.imshow(pivot.values, aspect='auto', origin='lower',
                       vmin=vmin, vmax=vmax, cmap='YlGnBu')
        ax.set_title(f'Al = {al}')
        ax.set_xlabel('P')
        ax.set_ylabel('Mg')
        ax.set_xticks(range(len(p_levels)))
        ax.set_yticks(range(len(mg_levels)))
        ax.set_xticklabels([f'{x:.2f}' for x in p_levels])
        ax.set_yticklabels([f'{x:.2f}' for x in mg_levels])

        for i in range(len(mg_levels)):
            for j in range(len(p_levels)):
                val = pivot.values[i, j]
                if np.isnan(val):
                    continue
                norm = (val - vmin) / (vmax - vmin + 1e-12)
                txt_color = 'white' if norm > 0.65 else 'black'
                ax.text(j, i, f'{val:.2f}', ha='center', va='center',
                        fontsize=9, fontweight='bold', color=txt_color)

    cbar = fig.colorbar(im, ax=axes, shrink=0.9)
    cbar.set_label(response_label)
    fig.suptitle(f'Heatmaps of {response_label} at Different Al Levels',
                 fontsize=16, fontweight='bold')
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.close()

for y, info in responses.items():
    make_heatmaps(df, response=y, response_label=info['label'],
                  save_path=outdir / f'14_heatmaps_real_{y}.png')
    print(f'[13] Saved: 14_heatmaps_real_{y}.png  [raw data]')


# --------------------------------------------------
# 14) PREDICTED RESPONSE SURFACE HEATMAPS (best model per response)
# --------------------------------------------------
def make_predicted_surface_heatmaps_reduced(data, response, response_label, save_path):
    """
    For reduced factorial model: predict on the observed grid points only,
    then show as heatmap (no fine interpolation — model is categorical).
    """
    formula = get_formula(response, 'reduced')
    model   = smf.ols(formula, data=data).fit()

    al_levels = sorted(data['Al'].unique())
    mg_levels = sorted(data['Mg'].unique())
    p_levels  = sorted(data['P'].unique())

    # Build prediction grid using all combinations of actual factor levels
    grid_rows = []
    for mg in mg_levels:
        for al in al_levels:
            for p in p_levels:
                grid_rows.append({
                    'Mg': mg, 'Al': al, 'P': p,
                    'Mg_cat': str(mg), 'Al_cat': str(al), 'P_cat': str(p)
                })
    grid_df = pd.DataFrame(grid_rows)
    grid_df['predicted'] = model.predict(grid_df)

    fig, axes = plt.subplots(1, len(al_levels), figsize=(18, 5), constrained_layout=True)
    if len(al_levels) == 1:
        axes = [axes]

    vmin = grid_df['predicted'].min()
    vmax = grid_df['predicted'].max()

    for ax, al in zip(axes, al_levels):
        sub   = grid_df[grid_df['Al'] == al].copy()
        pivot = sub.pivot(index='Mg', columns='P', values='predicted')\
                   .reindex(index=mg_levels, columns=p_levels)

        im = ax.imshow(pivot.values, aspect='auto', origin='lower',
                       vmin=vmin, vmax=vmax, cmap='viridis')
        ax.set_title(f'Predicted Surface at Al = {al}')
        ax.set_xlabel('P')
        ax.set_ylabel('Mg')
        ax.set_xticks(range(len(p_levels)))
        ax.set_yticks(range(len(mg_levels)))
        ax.set_xticklabels([f'{x:.2f}' for x in p_levels])
        ax.set_yticklabels([f'{x:.2f}' for x in mg_levels])

        for i in range(len(mg_levels)):
            for j in range(len(p_levels)):
                val = pivot.values[i, j]
                if np.isnan(val):
                    continue
                norm = (val - vmin) / (vmax - vmin + 1e-12)
                txt_color = 'white' if norm > 0.65 else 'black'
                ax.text(j, i, f'{val:.2f}', ha='center', va='center',
                        fontsize=9, fontweight='bold', color=txt_color)

        # Overlay real data points
        real_sub = data[data['Al'] == al]
        ax.scatter(
            [p_levels.index(p) for p in real_sub['P']],
            [mg_levels.index(m) for m in real_sub['Mg']],
            s=75, edgecolor='white', linewidth=1.0, color='#F28E2B', zorder=5
        )
        for _, row in real_sub.iterrows():
            annotate_sample_number(
                ax,
                p_levels.index(row['P']),
                mg_levels.index(row['Mg']),
                row['Sample'], fontsize=9, ha='center', va='center', boxed=True, zorder=8
            )

    cbar = fig.colorbar(im, ax=axes, shrink=0.9)
    cbar.set_label(response_label)
    fig.suptitle(f'Predicted Response Surface (Reduced Factorial) — {response_label}',
                 fontsize=14, fontweight='bold')
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.close()


def make_predicted_surface_heatmaps_quadratic(data, response, response_label, save_path):
    """
    For quadratic model: predict on a fine continuous grid (contour plot).
    """
    formula = get_formula(response, 'quadratic')
    model   = smf.ols(formula, data=data).fit()

    mg_grid   = np.linspace(data['Mg'].min(), data['Mg'].max(), 100)
    p_grid    = np.linspace(data['P'].min(),  data['P'].max(),  100)
    al_levels = sorted(data['Al'].unique())

    fig, axes = plt.subplots(1, len(al_levels), figsize=(18, 5), constrained_layout=True)
    if len(al_levels) == 1:
        axes = [axes]

    for ax, al in zip(axes, al_levels):
        XX, YY = np.meshgrid(p_grid, mg_grid)
        grid = pd.DataFrame({'Mg': YY.ravel(), 'Al': al, 'P': XX.ravel()})
        ZZ   = model.predict(grid).values.reshape(YY.shape)

        im = ax.contourf(XX, YY, ZZ, levels=24, cmap='viridis')
        ax.set_title(f'Predicted Surface at Al = {al}')
        ax.set_xlabel('P')
        ax.set_ylabel('Mg')

        sub = data[data['Al'] == al]
        ax.scatter(sub['P'], sub['Mg'], s=75, edgecolor='black',
                   linewidth=0.8, color='#F28E2B')
        for _, row in sub.iterrows():
            annotate_sample_number(ax, row['P'], row['Mg'], row['Sample'],
                                   fontsize=10, ha='center', va='center', boxed=True, zorder=8)

    cbar = fig.colorbar(im, ax=axes, shrink=0.9)
    cbar.set_label(response_label)
    fig.suptitle(f'Predicted Response Surface (Quadratic) — {response_label}',
                 fontsize=14, fontweight='bold')
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.close()


for y, info in responses.items():
    if BEST_MODEL[y] == 'reduced':
        make_predicted_surface_heatmaps_reduced(
            df, response=y, response_label=info['label'],
            save_path=outdir / f'15_predicted_surface_{y}.png'
        )
        print(f'[14] Saved: 15_predicted_surface_{y}.png  [Reduced Factorial]')
    else:
        make_predicted_surface_heatmaps_quadratic(
            df, response=y, response_label=info['label'],
            save_path=outdir / f'15_predicted_surface_{y}.png'
        )
        print(f'[14] Saved: 15_predicted_surface_{y}.png  [Quadratic]')


# --------------------------------------------------
# 15) EFFECT SIZE SUMMARY (best model per response)
# --------------------------------------------------
effect_writer = pd.ExcelWriter(outdir / '16_effect_size_summary.xlsx', engine='openpyxl')

for y, info in responses.items():
    model     = fit_best_model(y)
    anova_tbl = anova_lm(model, typ=2).copy()

    if 'sum_sq' in anova_tbl.columns:
        ss_resid = anova_tbl.loc['Residual', 'sum_sq']
        anova_tbl['partial_eta_sq'] = anova_tbl['sum_sq'] / (anova_tbl['sum_sq'] + ss_resid)

    model_label = 'Reduced Factorial' if BEST_MODEL[y] == 'reduced' else 'Quadratic'
    anova_tbl['model_used'] = model_label
    anova_tbl.to_excel(effect_writer, sheet_name=f'{y}_effect_sizes')
    print(f'[15] Effect sizes saved for {y}  [{model_label}]')

effect_writer.close()


# --------------------------------------------------
# 16) COMPOSITE SCORE (multi-response optimization)
# (unchanged — this uses raw data, not model predictions)
# --------------------------------------------------
opt = df.copy()

def zscore(x):
    return (x - x.mean()) / x.std(ddof=0)

opt['RevRatio_z']  = zscore(opt['RevRatio'])
opt['DeltaE_good'] = zscore(-opt['DeltaE'])   # smaller is better
opt['Overpot_z']   = zscore(opt['Overpot'])
opt['Rct_good']    = zscore(-opt['Rct'])       # smaller is better

opt['CompositeScore'] = opt[['RevRatio_z', 'DeltaE_good', 'Overpot_z', 'Rct_good']].mean(axis=1)
opt = opt.sort_values('CompositeScore', ascending=False)

opt[['Sample', 'Mg', 'Al', 'P', 'RevRatio', 'DeltaE', 'Overpot', 'Rct', 'CompositeScore']] \
    .to_excel(outdir / '17_composite_score_ranking.xlsx', index=False)

fig, ax = plt.subplots(figsize=(14, 8))
bars = ax.bar(opt['Sample'].astype(str), opt['CompositeScore'],
              edgecolor='black', linewidth=0.8)

for i in range(min(5, len(opt))):
    bars[i].set_linewidth(2.0)

for bar, val in zip(bars, opt['CompositeScore']):
    ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height(),
            f'{val:.2f}', ha='center', va='bottom', fontsize=9)

ax.set_title('Composite Performance Score Ranking')
ax.set_xlabel('Sample')
ax.set_ylabel('Composite Score')
ax.grid(axis='y', alpha=0.3)
ax.set_axisbelow(True)
plt.tight_layout()
plt.savefig(outdir / '18_composite_score_bar_chart.png', dpi=300, bbox_inches='tight')
plt.close()
print('[16] Saved: 18_composite_score_bar_chart.png  [raw data]')


# --------------------------------------------------
# 17) BEST SAMPLE MAPS
# (unchanged — these use raw data, no model needed)
# --------------------------------------------------
for y, info in responses.items():
    if info['goal'] == 'max':
        best_row = df.loc[df[y].idxmax()]
    else:
        best_row = df.loc[df[y].idxmin()]

    fig, ax = plt.subplots(figsize=(8, 6))
    sc = ax.scatter(df['Mg'], df['P'], s=150, c=df[y],
                    edgecolor='black', linewidth=0.8, cmap='plasma')
    ax.scatter(best_row['Mg'], best_row['P'], s=340, marker='*',
               edgecolor='black', linewidth=1.2, color='#FFD700')

    for _, row in df.iterrows():
        annotate_sample_number(ax, row['Mg'], row['P'], row['Sample'],
                               fontsize=9, ha='center', va='center')

    ax.set_title(f'Composition Map — {info["label"]} (Best Sample Marked)')
    ax.set_xlabel('Mg')
    ax.set_ylabel('P')
    cbar = plt.colorbar(sc, ax=ax)
    cbar.set_label(info['label'])
    plt.tight_layout()
    plt.savefig(outdir / f'19_best_sample_map_{y}.png', dpi=300, bbox_inches='tight')
    plt.close()
    print(f'[17] Saved: 19_best_sample_map_{y}.png  [raw data]')


# --------------------------------------------------
# 18) PRINT SUMMARY
# --------------------------------------------------
print("\n" + "=" * 80)
print("Statistical analysis complete.")
print(f"All outputs saved in:\n{outdir}")
print("=" * 80)
print("\nModel used per response:")
for y, m in BEST_MODEL.items():
    print(f"  {y:10s} -> {m}")

'''
================================================================================
Statistical analysis complete.
All outputs saved in:
/Users/apm/Desktop/lead-acid-code/lead_acid_stats_outputs
================================================================================

Model used per response:
  RevRatio   -> reduced
  DeltaE     -> quadratic
  Overpot    -> reduced
  Rct        -> reduced
  
'''













