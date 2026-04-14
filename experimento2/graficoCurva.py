import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# 1. Definição dos dados
if_data = [0.016, 0.330, 0.600, 1.040, 1.450, 1.860, 2.210, 2.340, 2.380, 2.630, 2.810, 3.030, 3.250]
ea_data = [12.170, 21.600, 38.000, 62.000, 82.700, 102.700, 115.400, 119.500, 120.900, 128.200, 132.800, 138.000, 142.100]


# Curva A Vazio - Descendente
if_desc = [3.090, 2.990, 2.760, 2.540, 2.340, 2.160, 1.780, 1.410, 1.080, 0.580, 0.240, 0.100]
ea_desc = [139.000, 137.000, 132.200, 126.700, 121.200, 115.200, 101.400, 85.200, 68.200, 45.200, 24.980, 4.990]

# if_desc = if_desc[::-1]
# ea_desc = ea_desc[-1]

# 2. Criação de um DataFrame e exportação para CSV
df = pd.DataFrame({'if': if_data, 'Ea': ea_data})
df.to_csv('dados_tensao_induzida.csv', index=False)

# 3. Configuração do gráfico
plt.figure(figsize=(10, 6))

# Ponto 1
z3 = np.polyfit(if_data, ea_data, 4)
p3 = np.poly1d(z3)
n1_linha = np.linspace(min(if_data), max(if_data), 100)
plt.plot(n1_linha, p3(n1_linha), 'b-',
                                 linewidth=2,
                                 label='Tendência curva de Magnetização')

plt.plot(if_data, ea_data, 'k.',
                        #    linestyle='--',
                        #    color='r',
                        #    linewidth=1,
                           label='Pontos obtidos curva de Magnetização')

# Adicionando títulos e rótulos (usando LaTeX para as fórmulas)
plt.xlabel('Corrente de Campo $i_f$ (A)')
plt.ylabel('Tensão Induzida $E_a$ (V)')
# plt.title('Curva de Magnetização - Ascendente')
# Melhorias visuais
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend()
# 4. Salvar e exibir o gráfico
plt.savefig('experimento2/curvas/curva_magnetização_ascendente.png')




plt.figure(figsize=(10, 6))
z_desc = np.polyfit(if_desc, ea_desc, 4)
p_desc = np.poly1d(z_desc)
x_desc = np.linspace(min(if_desc), max(if_desc), 100)
plt.plot(x_desc, p_desc(x_desc), 'b-', linewidth=2, label='Tendência (Descendente)')
plt.plot(if_desc, ea_desc, 'k.', markersize=8, label='Pontos (Descendente)')

plt.xlabel('Corrente de Campo $i_f$ (A)')
plt.ylabel('Tensão Induzida $E_a$ (V)')
# plt.title('Curva de Magnetização - Descendente')

plt.grid(True, linestyle='--', alpha=0.7)
plt.legend()

plt.savefig('experimento2/curvas/curva_magnetização_descendente.png')