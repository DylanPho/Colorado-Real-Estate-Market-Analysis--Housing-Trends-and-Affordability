import pandas as pd

# Load raw ZHVI data
df = pd.read_csv("data/raw/Metro_zhvi_uc_sfrcondo_tier_0.33_0.67_sm_sa_month.csv", header=0)

# Filter only Colorado metros
df_co = df[df['StateName'] == 'CO']

# Reshape to long format
df_long = df_co.melt(
    id_vars=['RegionName', 'StateName'],
    var_name='Date',
    value_name='ZHVI'
)

# Now drop unnecessary columns
df_long = df_long.drop(columns=['StateName'])

# Convert date to datetime
df_long['Date'] = pd.to_datetime(df_long['Date'], format='%Y-%m-%d', errors='coerce')

# Rename columns
df_long.rename(columns={'RegionName': 'Metro'}, inplace=True)

# Save cleaned file
df_long.to_csv("data/cleaned/zhvi_colorado.csv", index=False)

print("ZHVI cleaned and saved.")
