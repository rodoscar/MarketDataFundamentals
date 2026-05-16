from edgar_client import get_company_facts, get_annual_concept
from dcf_model import project_ebit, calculate_growth_rate, project_concept

# P&G como caso de prueba
CIK_PG = "80424"

facts = get_company_facts(CIK_PG)
print(f"Empresa: {facts['entityName']}")

df = get_annual_concept(facts, "OperatingIncomeLoss")
print("\nHistórico EBIT:")
print(df.tail(5))

growth_rate = calculate_growth_rate(df, periods=3)
print(f"\nTasa de crecimiento promedio (últimos 3 años): {growth_rate:.2%}")

proyeccion = project_ebit(df, growth_rate)
print("\nProyección EBIT:")
print(proyeccion)

df_tax = get_annual_concept(facts, "IncomeTaxExpenseBenefit")
print("\nHistórico Taxes:")
print(df_tax.tail(5))

proj_tax = project_concept(df_tax, "IncomeTaxExpenseBenefit", growth_rate)
print("\nProyección Taxes:")
print(proj_tax)