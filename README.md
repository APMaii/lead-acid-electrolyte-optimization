# Lead Acid Electrolyte Analysis

Modular, GitHub-ready version of the lead-acid electrolyte statistical analysis workflow.

## Attribution

- This repository is based on the following research article:
- **Electrochemical Performance Enhancement of Lead–Acid Batteries through Electrolyte Modification**
- **Article authors:** Fahimeh Gholami, Javad Asghari, Ali Pilehvar Meibody , Arash Ghazitabar, Shaahin Esfandiyari, Seyed Mehdi Orouji, Malek Naderi
- Main author of the Python code in this repository: **Ali Pilehvar Meibody**.
- **Code author affiliation:** Department of Applied Science and Technology, Politecnico di Torino, Torino, Italy; Graphene and Advanced Materials Laboratory (GAMLab.), Tehran, Iran.



### Abstract

Lead–acid battery performance is significantly constrained by negative-plate sulfation and parasitic hydrogen and oxygen evolution reactions at electrodes, all of which accelerate capacity fading and reduce service life. Additive engineering offers a direct approach to mitigate these degradation pathways. In this work, a simplified electrolyte formulation is proposed to simultaneously improve the behavior of both electrodes by influencing the interfacial kinetics at the anode and cathode. Although metal sulfates and mineral acids are known individual modifiers, their synergistic interactions remain insufficiently understood. To address this gap, a data-driven statistical framework combining Pearson correlation analysis, factorial and quadratic response-surface modeling, Type II ANOVA, effect size quantification, and multi-response composite scoring was developed alongside the electrochemical investigation to objectively quantify additive contributions and rank all formulations simultaneously.


`I_V.png`

![Cyclic voltammetry panels (a–d): 27 electrolytes, first cycle, 10 mV/s](ARTICLE_FIG/I_V.png)

Panels (a–d): cyclic voltammograms of 27 electrolyte formulations, with and without additives, for the first cycle at a scan rate of 10 mV/s.


Here, the combined effects of H3PO4, Al2(SO4)3, and MgSO4 were systematically evaluated over concentrations ranging from 0.1–0.5 wt.% for sulfate salts and 0.1–0.2 wt.% for phosphoric acid. Electrochemical (CV, LSV, EIS) and structural (XRD, FESEM) characterizations demonstrate that optimal combinations significantly enhance performance. Statistical modeling confirmed Al2(SO4)3 as the dominant factor across all responses, with the Mg×Al interaction as the only statistically significant ANOVA term for reversibility (F = 5.71, p = 0.018, eta_p^2 = 0.740), and the Al×P interaction as the controlling term for charge-transfer resistance (F = 3.71, p = 0.054, eta_p^2 = 0.650). Multi-response composite scoring across all 27 formulations provided an objective, data-driven basis for optimal sample selection.

Electrochemical evaluations of the negative electrode revealed that Al2(SO4)3 increases redox peak currents by 35–55%, decreases CV redox peak separation by 20–40%, and lowers charge-transfer resistance by 30–60%. Furthermore, synergistic mixing with H3PO4 and MgSO4 improves PbSO4 crystal refinement and interface stability, resulting in HER overpotential shifts of 80–120 mV and OER suppression of 50–90 mV. An optimum formulation (Sample 8) was validated in a 2 V, 200 Ah commercial cell, where cycle life increased by approximately 41% compared to the baseline electrolyte. These results highlight that targeted, statistically guided electrolyte formulation can effectively suppress sulfation and parasitic reactions, providing a practical and reproducible route toward longer-life, higher-efficiency lead–acid batteries.

### Keywords

Lead-acid battery; Electrolyte Additive; Magnesium sulfate; Phosphoric acid; Aluminum sulfate; Hydrogen Evolution Reaction.

## Project Structure

- `run_analysis.py` - Entry point script
- `src/lead_acid/config.py` - Response metadata and model selection
- `src/lead_acid/data.py` - Data loading and preprocessing
- `src/lead_acid/style.py` - Figure style and sample-label annotation helpers
- `src/lead_acid/modeling.py` - Model formula and fitting helpers
- `src/lead_acid/plots.py` - Plot generation functions
- `src/lead_acid/pipeline.py` - End-to-end analysis pipeline
- `requirements.txt` - Python dependencies

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run

```bash
python run_analysis.py
```

The input response values for all 27 formulations are available in Sheet1 of lead_acid_data.xlsx. The scoring and sensitivity analysis are implemented in src/lead_acid/pipeline.py. The command above generates reproduced/17_composite_score_ranking.xlsx for Table D1 and reproduced/20_composite_score_sensitivity.xlsx for the weighting analysis. A copy of the sensitivity workbook is available in RESULTS/, with the scenario summaries in Summary and the scores and ranks for all formulations in All_formulations.

```bash
python run_analysis.py --input lead_acid_data.xlsx --output reproduced
```

## Notes

- The pipeline generates figures and summary Excel outputs in the selected output directory.
- Sample labels on scatter/surface figures are styled for visibility (bold, colored, outlined, optional boxed labels).

## RESULTS

Place generated analysis images in the `RESULTS/` folder.

### Correlation Matrix

`02_correlation_matrix.png`

![Correlation Matrix](RESULTS/02_correlation_matrix.png)

## ARTICLE_FIG

Place manuscript/article figures in the `ARTICLE_FIG/` folder.


### Interaction Plot

`interaction_plot.png`

![Interaction Plot](ARTICLE_FIG/interaction_plot.png)

### Prediction Plot

`prediction_plot.png`

![Prediction Plot](ARTICLE_FIG/prediction_plot.png)

### Surface Response

`surface_response.png`

![Surface Response](ARTICLE_FIG/surface_response.png)
