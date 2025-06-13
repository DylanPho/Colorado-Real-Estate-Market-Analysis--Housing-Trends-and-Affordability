import pandas as pd

# Load income file
df = pd.read_csv("data/raw/S1901Income in the Past 12 Months (in 2023 Inflation-Adjusted Dollars).csv")

# Show all possible labels to see what to filter
print(df['Label (Grouping)'].dropna().unique())

# Filter for just median household income
row = df[df['Label (Grouping)'].str.contains("Median household income", case=False, na=False)]

# Grab the estimate value
income_value = row['Colorado!!Households!!Estimate'].values[0]

# Clean value (remove commas, convert to float)
income_value = float(str(income_value).replace(',', ''))

# Create a DataFrame for merging later
income_df = pd.DataFrame({
    'Metro': ['Colorado (Statewide)'],
    'Income': [income_value]
})

# Save
income_df.to_csv("data/cleaned/income_colorado.csv", index=False)

print("Cleaned statewide income saved.")
print(income_df)
