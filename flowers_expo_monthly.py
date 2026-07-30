import pandas as pd

# 1. Load raw export dataset from DANE
raw_data_path = r"C:\Users\Germán Calderón\Downloads\Exportaciones_agrícolas_no_tradicionales_y_tradicionales_20260709.csv"
df_dane = pd.read_csv(raw_data_path, encoding='utf-8')

# 2. Filter HS Code for Fresh Cut Flowers (0603) and Department (Bogotá)
# Normalize to string and pad with zeros to 10 digits to keep leading zero ('0603...')
normalized_hs_code = df_dane['Partida'].astype(str).str.split('.').str[0].str.zfill(10)

df_flowers = df_dane[
    normalized_hs_code.str.startswith('0603') &
    (df_dane['Descripción Departamento'].astype(str).str.upper().str.contains('BOGOTÁ', na=False))
].copy()

# 3. Clean and standardize Year and Month
df_flowers['year'] = df_flowers['Año'].astype(int)
df_flowers['month_name_es'] = df_flowers['Mes'].astype(str).str.strip().str.title()

# Spanish month mapping to numeric values for chronological sorting
spanish_months_map = {
    'Enero': 1, 'Febrero': 2, 'Marzo': 3, 'Abril': 4,
    'Mayo': 5, 'Junio': 6, 'Julio': 7, 'Agosto': 8,
    'Septiembre': 9, 'Octubre': 10, 'Noviembre': 11, 'Diciembre': 12
}
df_flowers['month_num'] = df_flowers['month_name_es'].map(spanish_months_map)

# 4. Aggregate data by Year and Month (Monthly Consolidation)
df_exports_monthly = df_flowers.groupby(['year', 'month_name_es', 'month_num']).agg({
    'Valor Miles FOB Dol Expo': 'sum',
    'Ton Netas Expo': 'sum'
}).reset_index()

# Rename columns to SQL-friendly standard names (lowercase, snake_case)
df_exports_monthly = df_exports_monthly.rename(columns={
    'month_name_es': 'month_name',
    'Valor Miles FOB Dol Expo': 'fob_usd_thousands',
    'Ton Netas Expo': 'net_tons_exported'
})

# Sort chronologically by Year and Month Number
df_exports_monthly = df_exports_monthly.sort_values(by=['year', 'month_num'])

# Reorder columns for optimal SQL presentation
df_exports_monthly = df_exports_monthly[['year', 'month_num', 'month_name', 'fob_usd_thousands', 'net_tons_exported']]

# 5. Export clean dataset to CSV for SQL import
output_path = r"C:\Users\Germán Calderón\Downloads\bogota_flower_exports_monthly.csv"
df_exports_monthly.to_csv(output_path, index=False, encoding='utf-8')

print("File successfully processed and saved to:", output_path)

# Verify first rows
df_exports_monthly.head()