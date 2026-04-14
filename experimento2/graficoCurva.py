import os
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# --- 0. CONFIGURAÇÃO DO DIRETÓRIO ---
# Garante que a pasta de destino exista antes de tentar salvar
output_dir = 'experimento2/curvas'
os.makedirs(output_dir, exist_ok=True)

# --- 1. DEFINIÇÃO DOS DADOS ---
# Curva A Vazio - Ascendente
if_asc = [0.016, 0.330, 0.600, 1.040, 1.450, 1.860, 2.210, 2.340, 2.380, 2.630, 2.810, 3.030, 3.250]
ea_asc = [12.170, 21.600, 38.000, 62.000, 82.700, 102.700, 115.400, 119.500, 120.900, 128.200, 132.800, 138.000, 142.100]

# Curva A Vazio - Descendente
if_desc = [3.090, 2.990, 2.760, 2.540, 2.340, 2.160, 1.780, 1.410, 1.080, 0.580, 0.240, 0.100]
ea_desc = [139.000, 137.000, 132.200, 126.700, 121.200, 115.200, 101.400, 85.200, 68.200, 45.200, 24.980, 4.990]

# Dados de Carga (Z1 a Z6)
if_load = [2.22, 2.20, 2.20, 2.19, 2.19, 2.17]
ea_load = [109.80, 100.40, 92.20, 84.90, 79.50, 76.40]
il_load = [3.08, 5.92, 8.31, 10.40, 12.32, 14.36]

# --- 2. EXPORTAÇÃO DE CSV (Opcional, também salvos na mesma pasta) ---
df_asc = pd.DataFrame({'if': if_asc, 'Ea': ea_asc})
df_asc.to_csv(f'{output_dir}/dados_tensao_induzida.csv', index=False)

df_carga = pd.DataFrame({'IL (A)': il_load, 'Ea (V)': ea_load, 'if (A)': if_load})
df_carga.to_csv(f'{output_dir}/dados_experimento_carga.csv', index=False)


# --- 3. GRÁFICO 1: CURVA DE MAGNETIZAÇÃO (ASCENDENTE) ---
plt.figure(figsize=(10, 6))

z1 = np.polyfit(if_asc, ea_asc, 4)
p1 = np.poly1d(z1)
x_asc_linha = np.linspace(min(if_asc), max(if_asc), 100)

plt.plot(x_asc_linha, p1(x_asc_linha), 'b-', linewidth=2, label='Tendência curva de Magnetização')
plt.plot(if_asc, ea_asc, 'k.', label='Pontos obtidos curva de Magnetização')

plt.xlabel('Corrente de Campo $i_f$ (A)')
plt.ylabel('Tensão Induzida $E_a$ (V)')
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend()

plt.tight_layout() # Ajusta os elementos para não sobrar espaço
plt.savefig(f'{output_dir}/curva_magnetizacao_ascendente.png', bbox_inches='tight') # Remove as bordas extras ao salvar
plt.close() # Fecha a figura para economizar memória


# --- 4. GRÁFICO 2: CURVA DE MAGNETIZAÇÃO (DESCENDENTE) ---
plt.figure(figsize=(10, 6))

z2 = np.polyfit(if_desc, ea_desc, 4)
p2 = np.poly1d(z2)
x_desc_linha = np.linspace(min(if_desc), max(if_desc), 100)

plt.plot(x_desc_linha, p2(x_desc_linha), 'b-', linewidth=2, label='Tendência (Descendente)')
plt.plot(if_desc, ea_desc, 'k.', markersize=8, label='Pontos (Descendente)')

plt.xlabel('Corrente de Campo $i_f$ (A)')
plt.ylabel('Tensão Induzida $E_a$ (V)')
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend()

plt.tight_layout()
plt.savefig(f'{output_dir}/curva_magnetizacao_descendente.png', bbox_inches='tight')
plt.close()


# --- 5. GRÁFICO 3: CURVA DE MAGNETIZAÇÃO (ASC VS DESC - HISTERESE) ---
plt.figure(figsize=(10, 6))

plt.plot(x_asc_linha, p1(x_asc_linha), 'b-', linewidth=2, label='Tendência (Ascendente)')
plt.plot(if_asc, ea_asc, 'r.', markersize=8, label='Pontos (Ascendente)')

plt.plot(x_desc_linha, p2(x_desc_linha), 'g-', linewidth=2, label='Tendência (Descendente)')
plt.plot(if_desc, ea_desc, 'k.', markersize=8, label='Pontos (Descendente)')

plt.xlabel('Corrente de Campo $i_f$ (A)')
plt.ylabel('Tensão Induzida $E_a$ (V)')
plt.grid(True, linestyle='--', alpha=0.6)
plt.legend()

plt.tight_layout()
plt.savefig(f'{output_dir}/magnetizacao_histerese.png', bbox_inches='tight')
plt.show()


# --- 6. GRÁFICO 4: CARACTERÍSTICA DE CARGA (Ea vs IL) ---
plt.figure(figsize=(10, 6))

z_load = np.polyfit(il_load, ea_load, 2)
p_load = np.poly1d(z_load)
x_load_linha = np.linspace(min(il_load), max(il_load), 100)

plt.plot(x_load_linha, p_load(x_load_linha), 'm--', label='Linha de Tendência de Carga')
plt.plot(il_load, ea_load, 'bo', markersize=7, label='Pontos de Carga (Z1-Z6)')

plt.xlabel('Corrente de Carga $I_L$ (A)')
plt.ylabel('Tensão $E_a$ (V)')
plt.grid(True, linestyle='--', alpha=0.6)
plt.legend()

plt.tight_layout()
plt.savefig(f'{output_dir}/caracteristica_carga.png', bbox_inches='tight')
plt.show()