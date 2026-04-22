import statsmodels.formula.api as smf

from .config import BEST_MODEL


def get_formula(y: str, model_type: str) -> str:
    if model_type == "reduced":
        return (
            f"{y} ~ C(Mg_cat) + C(Al_cat) + C(P_cat)"
            f" + C(Mg_cat):C(Al_cat)"
            f" + C(Mg_cat):C(P_cat)"
            f" + C(Al_cat):C(P_cat)"
        )

    return (
        f"{y} ~ Mg + Al + P"
        f" + I(Mg**2) + I(Al**2) + I(P**2)"
        f" + Mg:Al + Mg:P + Al:P"
    )


def fit_best_model(df, y: str):
    formula = get_formula(y, BEST_MODEL[y])
    return smf.ols(formula, data=df).fit()
