import pandas as pd
pd.set_option('display.max_columns', None)

df = pd.read_csv("Webscrape.csv", nrows=11, sep=";", encoding="utf-8")
df = df.replace('[]', pd.NA)

# Drop columns where all values are NaN
df = df.dropna(axis=1, how='all')
print(df.columns)
row = df.loc[10]
print("----------------row-------------------")
print(row)
asd = pd.Series({'DATE': ["2024-10-01 (Launch date for HELLA's new brake product lineup)"], 'PRODUCT': ['brake products', 'brake-by-wire technology', 'wear parts and hydraulics', 'brake pads', 'discs', 'brake calipers', 'premium accessory kit'], 'INDUSTRY_SECTOR': ['Automotive', 'Brake Industry'], 'INVESTMENT_TYPE': None, 'TECHNOLOGY_CATEGORY': ['Advanced Original Equipment (OE) expertise', 'brake-by-wire technology'], 'LAW': None, 'MARKET_TREND': ['Expansion in the truck sector', 'Enhanced support for electric and hybrid vehicle models'], 'POSITION': ['Dr. Marcel Wiedmann (Head of FORVIA HELLA’s global spare parts and workshop solutions division)'], 'SUMMARY': 'FORVIA HELLA launches new brake products under the HELLA brand, expanding its offerings in wear parts and hydraulics with a focus on innovation.', 'SENTIMENT': 750, 'EMPLOYMENT': None, 'ORG': ['HELLA Partner World', 'HELLA PAGID joint venture', 'FORVIA HELLA'], 'PERCENT': ['85% (coverage in brake hydraulics)', 'nearly 100% (coverage for brake pads and discs)']})
print("----------------asd-------------------")
print(asd)
print("----------------row update-------------------")

print(row)

# Convert to JSON
# result = 

# print(df.to_json(orient='records', lines=True, force_ascii=False))
