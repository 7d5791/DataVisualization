import pandas as pd
import json

df = pd.read_csv("veremi_multiattack_sample.csv")

# Muestra representativa (ajusta el número si quieres más/menos)
df_sample = df.sample(n=min(5000, len(df)), random_state=42)

# Guarda para la web
df_sample.to_json("web/sample_data.json", orient="records", indent=2)

print(f" Creado web/sample_data.json con {len(df_sample)} filas")
print("\nColumnas disponibles:")
print(df_sample.columns.tolist())
print("\nDistribución attack_label:")
print(df_sample["attack_label"].value_counts())
print("\nDistribución scenario_type:")
print(df_sample["scenario_type"].value_counts())