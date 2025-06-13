import pandas as pd

# Load raw ZORI rent data
df = pd.read_csv("data/raw/Metro_zori_uc_sfrcondomfr_sm_month.csv", header=0)

# Filter for Colorado metros (safe check using str.contains)
df_co = df[df['StateName'].str.contains("CO", case=False, na=False)]

# Melt wide format into long format
df_long = df_co.melt(
    id_vars=['RegionName', 'StateName'],
    var_name='Date',
    value_name='ZORI'
)

# Drop unused column and rename others
df_long = df_long.drop(columns=['StateName'])
df_long.rename(columns={'RegionName': 'Metro'}, inplace=True)

# Convert Date column to datetime
df_long['Date'] = pd.to_datetime(df_long['Date'], format='%Y-%m-%d', errors='coerce')
df_long = df_long.dropna(subset=['Date'])

# Save cleaned output
df_long.to_csv("data/cleaned/zori_colorado.csv", index=False)

print("ZORI cleaned and saved.")
