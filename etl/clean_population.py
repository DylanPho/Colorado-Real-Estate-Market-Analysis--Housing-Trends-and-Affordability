import pandas as pd

# Load wide-form population file
df = pd.read_csv("data/raw/B01003_Total_Population_Metros_CO.csv")

# Clean label column
df['Label (Grouping)'] = df['Label (Grouping)'].str.strip()

# Get only the row where Label is 'Total'
total_row = df[df['Label (Grouping)'] == 'Total']

if total_row.empty:
    print("'Total' row not found. Check file format.")
    exit()

# Drop the 'Label (Grouping)' column so we only keep metro columns
total_row = total_row.drop(columns=['Label (Grouping)'])

# Transpose the row to turn it into long-form
df_long = total_row.transpose().reset_index()
df_long.columns = ['Metro', 'Population']

# Clean population numbers
df_long['Population'] = df_long['Population'].replace(',', '', regex=True).astype(int)

# Clean metro names (remove trailing !!Estimate)
df_long['Metro'] = df_long['Metro'].str.replace('!!Estimate', '', regex=False).str.strip()

# Save cleaned file
df_long.to_csv("data/cleaned/population_colorado.csv", index=False)

print("Cleaned population data saved:")
print(df_long.head())
