import matplotlib.pyplot as plt
import numpy as np
import os

output_dir = 'experimento3/curvas'
os.makedirs(output_dir, exist_ok=True)

# --- 1. DADOS (Extraídos de image_108e23.png) ---
if_vazio = np.array([0, 0.48, 1.06, 1.5, 2.12, 2.58, 2.99, 3.67, 4.14, 4.6, 5.05, 5.56, 6, 6.59, 7.01, 7.55, 8.18, 8.61, 9.09, 9.56, 10.21, 10.5, 11.1, 11.49, 12.17, 13, 13.48])
va_vazio = np.array([5.94, 24.2, 41, 55.5, 73.7, 88.1, 101.4, 121.5, 135.5, 145.8, 160.7, 171.9, 179.5, 191.5, 199.4, 207.4, 215.4, 221.7, 228.1, 232.4, 239.1, 241.5, 246.7, 250.8, 255.7, 261.4, 264.2])

if_curto = np.array([0, 0.14, 0.34, 0.55, 0.77, 1, 1.21, 1.43, 1.64, 1.97, 2.1, 2.28, 2.52])
ia_curto = np.array([1.31, 1.92, 2.96, 4.12, 5.04, 6.1, 7.05, 8.1, 9.12, 10.4, 11.3, 12.24, 13.31])

# --- 2. CÁLCULOS E AJUSTES ---
# Curva a Vazio e Linha do Entreferro
z_vazio = np.polyfit(if_vazio, va_vazio, 4)
p_vazio = np.poly1d(z_vazio)
z_gap = np.polyfit(if_vazio[:5], va_vazio[:5], 1)
p_gap = np.poly1d(z_gap)

# Curva de Curto-Circuito
z_curto = np.polyfit(if_curto, ia_curto, 1)
p_curto = np.poly1d(z_curto)

# Linhas de tendência para o gráfico
x_v_linha = np.linspace(min(if_vazio), max(if_vazio), 100)
x_c_linha = np.linspace(min(if_curto), max(if_curto), 100)

# --- 3. GRÁFICO 1: COMBINADO (OCC + SCC + AIR GAP) ---
fig, ax1 = plt.subplots(figsize=(10, 6))
ax1.plot(if_vazio, va_vazio, 'k.', label='Pontos Vazio')
ax1.plot(x_v_linha, p_vazio(x_v_linha), 'b-', linewidth=2, label='Curva a Vazio (OCC)')
ax1.plot(x_v_linha, p_gap(x_v_linha), 'g--', alpha=0.7, label='Linha do Entreferro')
ax1.set_xlabel('Corrente de Campo $i_f$ (A)')
ax1.set_ylabel('Tensão de Armadura $V_a$ (V)', color='b')
ax1.grid(True, linestyle='--', alpha=0.6)

ax2 = ax1.twinx()
ax2.plot(if_curto, ia_curto, 'r.', label='Pontos Curto')
ax2.plot(x_c_linha, p_curto(x_c_linha), 'r-', linewidth=2, label='Curva de Curto (SCC)')
ax2.set_ylabel('Corrente de Armadura $I_a$ (A)', color='r')

lines, labels = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines + lines2, labels + labels2, loc='lower right')
plt.title('')
plt.savefig(f'{output_dir}/01_combinado_vazio_curto.png', bbox_inches='tight')
plt.close()

# --- 4. GRÁFICO 2: ENSAIO DE CURTO-CIRCUITO (SCC) ---
plt.figure(figsize=(10, 6))
plt.plot(if_curto, ia_curto, 'r.', markersize=8, label='Dados Experimentais')
plt.plot(x_c_linha, p_curto(x_c_linha), 'r-', linewidth=2, label='Linha de Tendência')
plt.xlabel('Corrente de Campo $i_f$ (A)')
plt.ylabel('Corrente de Armadura $I_a$ (A)')
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend()
plt.savefig(f'{output_dir}/02_ensaio_curto_circuito.png', bbox_inches='tight')
plt.close()

# --- 5. GRÁFICO 3: ENSAIO A VAZIO (OCC + AIR GAP) ---
plt.figure(figsize=(10, 6))
plt.plot(if_vazio, va_vazio, 'k.', markersize=8, label='Dados Experimentais')
plt.plot(x_v_linha, p_vazio(x_v_linha), 'b-', linewidth=2, label='Tendência de Saturação')
plt.plot(x_v_linha, p_gap(x_v_linha), 'g--', linewidth=1.5, label='Linha do Entreferro')
plt.xlabel('Corrente de Campo $i_f$ (A)')
plt.ylabel('Tensão de Armadura $V_a$ (V)')
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend()
plt.savefig(f'{output_dir}/03_ensaio_a_vazio.png', bbox_inches='tight')