import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import numpy as np

# ====================== CONFIGURACIÓN ======================
sns.set_theme(style="whitegrid", palette="muted", font_scale=1.1)
plt.rcParams['figure.dpi'] = 150
plt.rcParams['savefig.dpi'] = 300
plt.rcParams['font.family'] = 'DejaVu Sans'

# Colores consistentes
COLORS = {
    "Normal": "#2E86AB",
    "Ataque": "#E63946"
}

OUTPUT_DIR = "figures"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ====================== CARGA DE DATOS ======================
print("Cargando datos...")
df = pd.read_csv("veremi_multiattack_sample.csv")

print(f"Registros cargados: {len(df)}")
print(f"Columnas disponibles: {df.columns.tolist()}\n")

# ====================== GRÁFICO 1: Distribución Espacial ======================
print("Generando Gráfico 1: Distribución espacial...")
plt.figure(figsize=(11, 7))
sns.scatterplot(
    data=df.sample(min(8000, len(df)), random_state=42),
    x="pos_x", y="pos_y",
    hue="attack_label",
    palette=COLORS,
    alpha=0.65,
    s=12,
    edgecolor=None
)
plt.title("Distribución espacial de mensajes Normales vs Ataques", fontsize=16, pad=20, weight='bold')
plt.xlabel("Posición X (simulación)", fontsize=12)
plt.ylabel("Posición Y (simulación)", fontsize=12)
plt.legend(title="Tipo de mensaje", fontsize=11)
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/01_distribucion_espacial.png", bbox_inches="tight")
plt.close()

# ====================== GRÁFICO 2: Trayectorias de ejemplo ======================
print("Generando Gráfico 2: Ejemplos de trayectorias...")
plt.figure(figsize=(11, 8))
sample_senders = df.groupby("sender").size().sort_values(ascending=False).head(6).index
sample_traj = df[df["sender"].isin(sample_senders)].sort_values(["sender", "sendTime"])

for sender in sample_senders:
    sub = sample_traj[sample_traj["sender"] == sender]
    color = COLORS.get(sub["attack_label"].iloc[0], "#64748b")
    plt.plot(sub["pos_x"], sub["pos_y"],
             marker="o", markersize=3, linewidth=1.5,
             alpha=0.75, label=f"{sender} ({sub['attack_label'].iloc[0]})",
             color=color)

plt.title("Ejemplos de trayectorias de vehículos (Normal vs Ataque)", fontsize=16, pad=20, weight='bold')
plt.xlabel("Posición X", fontsize=12)
plt.ylabel("Posición Y", fontsize=12)
plt.legend(title="Vehículo (Tipo)", bbox_to_anchor=(1.02, 1), loc="upper left", fontsize=9)
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/02_ejemplos_trayectorias.png", bbox_inches="tight")
plt.close()

# ====================== GRÁFICO 3: Velocidad y Latencia ======================
print("Generando Gráfico 3: Velocidad y Latencia por tipo de mensaje...")
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

sns.boxplot(data=df, x="attack_label", y="speed_kmh", palette=COLORS, ax=axes[0], showfliers=False)
axes[0].set_title("Distribución de Velocidad (km/h)", fontsize=14, weight='bold')
axes[0].set_xlabel("Tipo de mensaje")
axes[0].set_ylabel("Velocidad (km/h)")

sns.boxplot(data=df, x="attack_label", y="latency", palette=COLORS, ax=axes[1], showfliers=False)
axes[1].set_title("Distribución de Latencia (segundos)", fontsize=14, weight='bold')
axes[1].set_xlabel("Tipo de mensaje")
axes[1].set_ylabel("Latencia (s)")

plt.suptitle("Comparación de Velocidad y Latencia entre Normal y Ataque", fontsize=16, weight='bold', y=1.02)
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/03_velocidad_latencia.png", bbox_inches="tight")
plt.close()

# ====================== GRÁFICO 4: Tipos de Ataque ======================
print("Generando Gráfico 4: Distribución de tipos de ataque...")
plt.figure(figsize=(10, 6))
order = df[df["attack_label"] == "Ataque"]["attack_type"].value_counts().index
sns.countplot(
    data=df[df["attack_label"] == "Ataque"],
    y="attack_type",
    order=order,
    palette="Set2"
)
plt.title("Cantidad de mensajes por tipo de ataque", fontsize=16, pad=20, weight='bold')
plt.xlabel("Número de mensajes")
plt.ylabel("Tipo de ataque")
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/04_tipos_de_ataque.png", bbox_inches="tight")
plt.close()

# ====================== GRÁFICO 5: % Ataques por Escenario y Densidad ======================
print("Generando Gráfico 5: Porcentaje de ataques por escenario y densidad...")
plt.figure(figsize=(9, 6))
pivot = pd.crosstab(
    df["scenario_type"],
    df["density"],
    values=df["is_attack"],
    aggfunc="mean"
) * 100

sns.heatmap(
    pivot,
    annot=True,
    fmt=".1f",
    cmap="Reds",
    linewidths=0.8,
    cbar_kws={'label': '% de mensajes que son ataques'}
)
plt.title("% de mensajes de ataque según Escenario y Densidad", fontsize=15, pad=20, weight='bold')
plt.xlabel("Densidad de tráfico")
plt.ylabel("Tipo de escenario")
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/05_ataques_por_escenario_densidad.png", bbox_inches="tight")
plt.close()

# ====================== GRÁFICO 6: Velocidad vs Latencia ======================
print("Generando Gráfico 6: Relación Velocidad vs Latencia...")
plt.figure(figsize=(10, 7))
sample = df.sample(min(4000, len(df)), random_state=42)
sns.scatterplot(
    data=sample,
    x="speed_kmh",
    y="latency",
    hue="attack_label",
    palette=COLORS,
    alpha=0.6,
    s=25
)
plt.title("Relación entre Velocidad y Latencia según tipo de mensaje", fontsize=15, pad=20, weight='bold')
plt.xlabel("Velocidad (km/h)")
plt.ylabel("Latencia (segundos)")
plt.legend(title="Tipo de mensaje")
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/06_velocidad_vs_latencia.png", bbox_inches="tight")
plt.close()

print("\n" + "="*50)
print(" ¡Gráficos generados exitosamente!")
print(f" Carpeta creada: {OUTPUT_DIR}/")
print("Archivos generados:")
for file in sorted(os.listdir(OUTPUT_DIR)):
    print(f"   - {file}")
print("="*50)