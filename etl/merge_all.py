import pandas as pd

# Load all cleaned CSVs
zhvi = pd.read_csv("data/cleaned/zhvi_colorado.csv")
zori = pd.read_csv("data/cleaned/zori_colorado.csv")
income = pd.read_csv("data/cleaned/income_colorado.csv")
population = pd.read_csv("data/cleaned/population_colorado.csv")

# Function to normalize metro names
def clean_metro(val):
    return val.strip().replace(" Metro Area", "").replace("–", "-").replace("!!Households!!Estimate", "")

# Apply name cleaning
zhvi['Metro'] = zhvi['Metro'].apply(clean_metro)
zori['Metro'] = zori['Metro'].apply(clean_metro)
income['Metro'] = income['Metro'].apply(clean_metro)
population['Metro'] = population['Metro'].apply(clean_metro)

# Convert date columns to datetime
zori['Date'] = pd.to_datetime(zori['Date'], errors='coerce')
zhvi['Date'] = pd.to_datetime(zhvi['Date'], errors='coerce')

# Merge ZORI and ZHVI on Metro + Date
merged = pd.merge(zori, zhvi, on=["Metro", "Date"], how="inner")

# Merge in income and population
merged = pd.merge(merged, income, on="Metro", how="left")
merged = pd.merge(merged, population, on="Metro", how="left")

# Drop rows with missing core data
merged = merged.dropna(subset=["ZORI", "ZHVI", "Income", "Population"])

# Clean ZHVI and Income columns if they’re still strings
merged["ZHVI"] = pd.to_numeric(merged["ZHVI"], errors="coerce")
merged["Income"] = merged["Income"].replace('[\$,]', '', regex=True).astype(float)

# Then calculate the affordability ratio
merged["AffordabilityRatio"] = merged["ZHVI"] / merged["Income"]

# Save final output
merged.to_csv("data/cleaned/final_colorado_housing_analytics_long.csv", index=False)
print("Final long-form dataset saved to 'data/cleaned/final_colorado_housing_analytics_long.csv'")
