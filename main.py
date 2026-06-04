import os
import json
import ast
import pandas as pd
import numpy as np

# ==========================
# CONFIGURACIÓN
# ==========================
ROOT_DIR = "."
OUTPUT_FILE = "veremi_multiattack_sample.csv"
MAX_ROWS_PER_FOLDER = 8000  # Bajé un poco el límite para probar
RANDOM_STATE = 42


def flatten_dict(d, parent_key="", sep="_"):
    items = []
    for key, value in d.items():
        new_key = f"{parent_key}{sep}{key}" if parent_key else str(key)
        if isinstance(value, dict):
            items.extend(flatten_dict(value, new_key, sep=sep).items())
        else:
            items.append((new_key, value))
    return dict(items)


def read_json_file(path):
    records = []
    with open(path, "r", encoding="utf-8") as f:
        content = f.read().strip()
    if not content:
        return records
    try:
        data = json.loads(content)
        if isinstance(data, list):
            records = data
        elif isinstance(data, dict):
            records = [data]
    except json.JSONDecodeError:
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    records.append(json.loads(line))
    return records


def parse_position(value):
    if pd.isna(value):
        return np.nan, np.nan
    if isinstance(value, (list, tuple)) and len(value) >= 2:
        return value[0], value[1]
    if isinstance(value, str):
        try:
            parsed = ast.literal_eval(value)
            if isinstance(parsed, (list, tuple)) and len(parsed) >= 2:
                return parsed[0], parsed[1]
        except:
            pass
    return np.nan, np.nan


def infer_metadata(folder_name):
    name = folder_name.lower()
    scenario_type = "Urban" if "urban" in name else "Highway" if "highway" in name else "Unknown"
    density = "Low density" if "_2_" in name else "High density" if "_7_" in name else "Unknown density"

    attack_map = {
        "randompositionoffset": "Random Position Offset",
        "dosattack": "DoS Attack",
        "timedelay": "Time Delay",
        "datareplay": "Data Replay",
        "sybil": "Sybil",
        "constantspeed": "Constant Speed Offset",
        "randomspeed": "Random Speed Offset",
        "reversedheading": "Reversed Heading",
        "suddenstop": "Sudden Stop"
    }

    for key, attack in attack_map.items():
        if key in name:
            return folder_name, scenario_type, density, attack

    return folder_name, scenario_type, density, folder_name.replace("InTAS_", "")


def process_folder(folder_path, folder_name):
    scenario, scenario_type, density, attack_type = infer_metadata(folder_name)

    json_files = [os.path.join(root, f) for root, _, files in os.walk(folder_path)
                  for f in files if f.endswith(".json")]

    print(f"\n▶ Procesando: {folder_name} | JSONs encontrados: {len(json_files)} | Ataque detectado: {attack_type}")

    rows = []
    for path in json_files:
        try:
            records = read_json_file(path)
            for record in records:
                if isinstance(record, dict):
                    flat = flatten_dict(record)
                    flat["source_file"] = os.path.basename(path)
                    flat["scenario"] = scenario
                    flat["scenario_type"] = scenario_type
                    flat["density"] = density
                    flat["attack_type"] = attack_type
                    rows.append(flat)

                if len(rows) >= MAX_ROWS_PER_FOLDER:
                    break
        except Exception as e:
            print(f"   ⚠ Error en {path}: {e}")

        if len(rows) >= MAX_ROWS_PER_FOLDER:
            break

    if not rows:
        print(f"    No se encontraron registros válidos en {folder_name}")
        return pd.DataFrame()

    df = pd.DataFrame(rows)

    # Columnas requeridas (más flexible)
    required = ["rcvTime", "sendTime", "sender_id", "attacker", "sender_pos", "sender_spd"]
    missing = [c for c in required if c not in df.columns]

    if missing:
        print(f"    Saltando {folder_name}. Faltan columnas: {missing}")
        print(f"      Columnas disponibles: {list(df.columns)[:15]}...")
        return pd.DataFrame()

    # Procesamiento normal
    positions = df["sender_pos"].apply(parse_position)
    df["pos_x"] = positions.apply(lambda p: p[0])
    df["pos_y"] = positions.apply(lambda p: p[1])

    out = pd.DataFrame()
    out["sender"] = df["sender_id"]
    out["scenario_type"] = df["scenario_type"]
    out["density"] = df["density"]
    out["attack_type"] = df["attack_type"]
    out["sendTime"] = df["sendTime"]
    out["rcvTime"] = df["rcvTime"]
    out["pos_x"] = df["pos_x"]
    out["pos_y"] = df["pos_y"]
    out["speed"] = df["sender_spd"]
    out["is_attack"] = pd.to_numeric(df["attacker"], errors="coerce").fillna(0).astype(int)
    out["attack_label"] = out["is_attack"].map({0: "Normal", 1: "Ataque"})

    out = out.dropna(subset=["pos_x", "pos_y", "speed"])
    out["speed_kmh"] = out["speed"] * 3.6
    out["latency"] = out["rcvTime"] - out["sendTime"]

    print(f"   ✅ {len(out)} registros procesados correctamente de {folder_name}")
    return out


# ==========================
# EJECUCIÓN PRINCIPAL
# ==========================
folders = [f for f in os.listdir(ROOT_DIR) if os.path.isdir(f) and f.startswith("InTAS_")]

print("Carpetas detectadas:")
for f in folders:
    print(" -", f)

all_data = []
for folder in folders:
    df_folder = process_folder(folder, folder)
    if not df_folder.empty:
        all_data.append(df_folder)

if not all_data:
    raise ValueError("No se procesó ninguna carpeta correctamente.")

final_df = pd.concat(all_data, ignore_index=True)
final_df = final_df.sample(frac=1, random_state=RANDOM_STATE).reset_index(drop=True)

final_df.to_csv(OUTPUT_FILE, index=False)

print("\n" + "=" * 60)
print("ARCHIVO GENERADO:", OUTPUT_FILE)
print(f"Total de registros: {len(final_df)}")
print("\nDistribución por attack_type:")
print(final_df["attack_type"].value_counts())
print("\nDistribución Normal / Ataque:")
print(final_df["attack_label"].value_counts())
print("=" * 60)