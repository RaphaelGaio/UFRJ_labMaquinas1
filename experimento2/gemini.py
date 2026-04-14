import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# --- 1. DEFINIÇÃO DOS DADOS ---

# Curva A Vazio - Ascendente (Original)
if_asc = [0.016, 0.330, 0.600, 1.040, 1.450, 1.860, 2.210, 2.340, 2.380, 2.630, 2.810, 3.030, 3.250]
ea_asc = [12.170, 21.600, 38.000, 62.000, 82.700, 102.700, 115.400, 119.500, 120.900, 128.200, 132.800, 138.000, 142.100]

# Curva A Vazio - Descendente
if_desc = [3.090, 2.990, 2.760, 2.540, 2.340, 2.160, 1.780, 1.410, 1.080, 0.580, 0.240, 0.100]
ea_desc = [139.000, 137.000, 132.200, 126.700, 121.200, 115.200, 101.400, 85.200, 68.200, 45.200, 24.980, 4.990]

# Dados de Carga (Z1 a Z6)
if_load = [2.22, 2.20, 2.20, 2.19, 2.19, 2.17]
ea_load = [109.80, 100.40, 92.20, 84.90, 79.50, 76.40]
il_load = [3.08, 5.92, 8.31, 10.40, 12.32, 14.36]

# --- 2. GRÁFICO 1: CURVA DE MAGNETIZAÇÃO (ASC VS DESC) ---

plt.figure(figsize=(10, 6))

# Linha de tendência Ascendente
z_asc = np.polyfit(if_asc, ea_asc, 4)
p_asc = np.poly1d(z_asc)
x_asc = np.linspace(min(if_asc), max(if_asc), 100)
plt.plot(x_asc, p_asc(x_asc), 'b-', linewidth=2, label='Tendência (Ascendente)')
plt.plot(if_asc, ea_asc, 'r.', markersize=8, label='Pontos (Ascendente)')

# Linha de tendência Descendente
z_desc = np.polyfit(if_desc, ea_desc, 4)
p_desc = np.poly1d(z_desc)
x_desc = np.linspace(min(if_desc), max(if_desc), 100)
plt.plot(x_desc, p_desc(x_desc), 'g-', linewidth=2, label='Tendência (Descendente)')
plt.plot(if_desc, ea_desc, 'k.', markersize=8, label='Pontos (Descendente)')

plt.xlabel('Corrente de Campo $i_f$ (A)')
plt.ylabel('Tensão Induzida $E_a$ (V)')
# plt.title('Curva de Magnetização - Histerese (Ascendente vs Descendente)')
plt.grid(True, linestyle='--', alpha=0.6)
plt.legend()
plt.savefig('magnetizacao_histerese.png')
plt.show()

# --- 3. GRÁFICO 2: CARACTERÍSTICA DE CARGA (Ea vs IL) ---

plt.figure(figsize=(10, 6))

# Linha de tendência para os dados de carga
z_load = np.polyfit(il_load, ea_load, 1)
p_load = np.poly1d(z_load)
x_load = np.linspace(min(il_load), max(il_load), 100)

plt.plot(x_load, p_load(x_load), 'm--', label='Linha de Tendência de Carga')
plt.plot(il_load, ea_load, 'bo', markersize=7, label='Pontos de Carga (Z1-Z6)')

plt.xlabel('Corrente de Carga $I_L$ (A)')
plt.ylabel('Tensão $E_a$ (V)')
# plt.title('Característica de Carga (Tensão vs Corrente de Carga)')
plt.grid(True, linestyle='--', alpha=0.6)
plt.legend()
plt.savefig('caracteristica_carga.png')
plt.show()

# --- 4. SALVANDO OS DADOS ---
# Opcional: exportar para CSV para conferência
df_final = pd.DataFrame({
    'IL (A)': il_load,
    'Ea (V)': ea_load,
    'if (A)': if_load
})
df_final.to_csv('dados_experimento_carga.csv', index=False)