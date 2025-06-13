import pandas as pd

# Load the file
df = pd.read_csv("data/raw/S1901Income in the Past 12 Months (in 2023 Inflation-Adjusted Dollars).csv")

# Clean label column
df['Label (Grouping)'] = df['Label (Grouping)'].str.replace('\xa0', '', regex=True).str.strip()

# Extract the row for "Median income (dollars)"
median_row = df[df['Label (Grouping)'] == 'Median income (dollars)']

if median_row.empty:
    print("'Median income (dollars)' row not found. Check file format.")
    exit()

# Drop the label column and transpose
median_row = median_row.drop(columns=['Label (Grouping)'])
df_long = median_row.transpose().reset_index()
df_long.columns = ['Metro', 'Income']

# Clean up Metro names (remove !!Households!!Estimate)
df_long['Metro'] = df_long['Metro'].str.replace('!!Households!!Estimate', '', regex=False).str.strip()

# Clean Income values
df_long['Income'] = df_long['Income'].replace(',', '', regex=True).astype(float)

# Save cleaned output
df_long.to_csv("data/cleaned/income_colorado.csv", index=False)

print("Cleaned income data saved:")
print(df_long.head())
