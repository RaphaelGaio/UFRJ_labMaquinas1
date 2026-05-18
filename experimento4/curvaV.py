import matplotlib.pyplot as plt
import numpy as np
import os

output_dir = 'experimento4/curvas'
os.makedirs(output_dir, exist_ok=True)

# ----------------------------------------------------
# 1. Entrada de Dados (Extraídos das Tabelas)
# ----------------------------------------------------

# Tabela 1: Carga Leve
if_leve = [5.54, 5.92, 6.55, 7.10, 7.52, 8.08, 8.52, 8.98, 9.60, 10.00, 10.62, 11.05, 11.55, 12.04, 12.44, 13.12]
ia_leve = [13.72, 11.92, 9.24, 7.24, 6.33, 3.55, 3.23, 2.02, 3.03, 4.36, 6.83, 8.26, 9.67, 11.26, 13.25, 16.03]

# Tabela 2: Carga Média
if_media = [6.75, 7.05, 7.24, 8.88, 9.45, 10.14, 10.62, 11.02, 11.49]
ia_media = [12.21, 11.52, 10.88, 8.30, 8.67, 9.85, 10.75, 12.08, 13.30]

# Tabela 3: Carga Alta
if_alta = [7.55, 8.02, 8.47, 9.28, 10.15]
ia_alta = [13.40, 12.17, 11.85, 11.62, 12.60]

# Pontos de Fator de Potência Unitário (FP = 1)
if_fp_unitario = [8.98, 8.88, 9.28]
ia_fp_unitario = [2.02, 8.30, 11.62]

# ----------------------------------------------------
# 2. Cálculos das Aproximações Polinomiais
# ----------------------------------------------------

# Definindo o grau do polinômio (grau 4 se adapta bem ao formato de 'V')
grau = 5

# Aproximação - Carga Leve
poly_leve = np.poly1d(np.polyfit(if_leve, ia_leve, grau))
x_leve_smooth = np.linspace(min(if_leve), max(if_leve), 100)
y_leve_smooth = poly_leve(x_leve_smooth)

# Aproximação - Carga Média
poly_media = np.poly1d(np.polyfit(if_media, ia_media, grau))
x_media_smooth = np.linspace(min(if_media), max(if_media), 100)
y_media_smooth = poly_media(x_media_smooth)

# Aproximação - Carga Alta
poly_alta = np.poly1d(np.polyfit(if_alta, ia_alta, grau))
x_alta_smooth = np.linspace(min(if_alta), max(if_alta), 100)
y_alta_smooth = poly_alta(x_alta_smooth)


# ----------------------------------------------------
# 3. Configuração e Plotagem do Gráfico
# ----------------------------------------------------

plt.figure(figsize=(10, 6))

# Plotando os dados reais como pontos semi-transparentes
plt.scatter(if_leve, ia_leve, color='royalblue', marker='o', alpha=0.5)
plt.scatter(if_media, ia_media, color='darkorange', marker='s', alpha=0.5)
plt.scatter(if_alta, ia_alta, color='forestgreen', marker='^', alpha=0.5)

# Plotagem das Curvas Polinomiais Ajustadas
plt.plot(x_leve_smooth, y_leve_smooth, label='Carga Leve (Polinômio)', color='royalblue', linewidth=2)
plt.plot(x_media_smooth, y_media_smooth, label='Carga Média (Polinômio)', color='darkorange', linewidth=2)
plt.plot(x_alta_smooth, y_alta_smooth, label='Carga Alta (Polinômio)', color='forestgreen', linewidth=2)

# Plotagem da linha pontilhada de Fator de Potência Unitário
plt.plot(if_fp_unitario, ia_fp_unitario, marker='D', linestyle='--', color='red', label='FP Unitário')

# Títulos e Rótulos
plt.title('Curvas V da Máquina Síncrona (Aproximação Polinomial)', fontsize=14, fontweight='bold')
plt.xlabel('Corrente de Campo - If (A)', fontsize=12)
plt.ylabel('Corrente de Armadura - Ia (A)', fontsize=12)

# Configurações visuais adicionais
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend(loc='best')
plt.xlim(5, 14) 
plt.ylim(0, 18) 

# ----------------------------------------------------
# 4. Exibição / Salvamento
# ----------------------------------------------------
plt.tight_layout()
plt.savefig(f'{output_dir}/curva.png', bbox_inches='tight')
plt.show() # Adicionado plt.show() para visualizar no console, caso deseje