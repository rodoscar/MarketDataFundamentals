import pandas as pd

def calculate_growth_rate(df: pd.DataFrame, periods: int = 3) -> float:
    df_recent = df.tail(periods + 1)
    rates = []
    values = df_recent["OperatingIncomeLoss"].values
    for i in range(1, len(values)):
        if values[i-1] > 0:
            rate = (values[i] / values[i-1]) - 1
            rates.append(rate)
    avg_rate = sum(rates) / len(rates)
    return avg_rate

def project_ebit(df: pd.DataFrame, growth_rate: float, years: int = 3) -> pd.DataFrame:
    last_year = df["fiscal_year"].max()
    last_ebit = df.loc[df["fiscal_year"] == last_year, "OperatingIncomeLoss"].values[0]

    projections = []
    for i in range(1, years + 1):
        projected_year = last_year + i
        projected_ebit = last_ebit * ((1 + growth_rate) ** i)
        projections.append({"fiscal_year": projected_year, "EBIT": round(projected_ebit)})

    return pd.DataFrame(projections)

def project_concept(df: pd.DataFrame, concept: str, growth_rate: float, years: int = 3) -> pd.DataFrame:
    last_year = df["fiscal_year"].max()
    last_val = df.loc[df["fiscal_year"] == last_year, concept].values[0]

    projections = []
    for i in range(1, years + 1):
        projected_year = last_year + i
        projected_val = last_val * ((1 + growth_rate) ** i)
        projections.append({"fiscal_year": projected_year, concept: round(projected_val)})

    return pd.DataFrame(projections)