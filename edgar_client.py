import requests
import pandas as pd

BASE_URL = "https://data.sec.gov/api/xbrl/companyfacts"

HEADERS = {
    "User-Agent": "MarketDataFundamentals contact@email.com"
}

def get_company_facts(cik: str) -> dict:
    url = f"{BASE_URL}/CIK{cik.zfill(10)}.json"
    response = requests.get(url, headers=HEADERS, timeout=30)
    response.raise_for_status()
    return response.json()

def get_annual_concept(facts: dict, concept: str) -> pd.DataFrame:
    try:
        entries = facts["facts"]["us-gaap"][concept]["units"]["USD"]
    except KeyError:
        print(f"Concepto no encontrado: {concept}")
        return pd.DataFrame()

    df = pd.DataFrame(entries)
    df = df[df["form"] == "10-K"]
    df = df[df["fp"] == "FY"]
    df = df.drop_duplicates(subset="fy", keep="last")
    df = df[["fy", "end", "val"]].sort_values("fy").reset_index(drop=True)
    df.rename(columns={"fy": "fiscal_year", "val": concept}, inplace=True)

    return df
