import matplotlib.pyplot as plt
import numpy as np

# Extracao de Dados
# Ponto 1 (Operacao 1)
Va1 = np.array([106.4, 94.4, 88.1, 83.1, 81.8])
Ia1 = np.array([3.25, 6.0, 7.5, 8.0, 8.5])
VL1 = np.array([110.9, 91.5, 81.0, 75.3, 72.0])
iL1 = np.array([0.0, 2.8, 4.34, 5.14, 5.64])

# Ponto 2 (Operacao 2)
Va2 = np.array([99.5, 81.2, 72.3, 67.8, 65.1])
Ia2 = np.array([3.0, 6.0, 7.5, 8.5, 8.5])
VL2 = np.array([108.9, 82.9, 70.1, 63.5, 59.7])
iL2 = np.array([0.0, 2.67, 4.0, 4.71, 5.11])

# Calculos das Potencias (Entrada no Motor e Saida no Gerador)
Pin1 = Va1 * Ia1
Pout1 = VL1 * iL1

Pin2 = Va2 * Ia2
Pout2 = VL2 * iL2

# Calculo da Eficiencia Individual (Assumindo que sao iguais)
# n_global = Pout / Pin = n_motor * n_gerador = n_individual^2
# Logo, n_individual = raiz_quadrada(Pout / Pin) * 100 para converter em %
Eficiencia_ind_1 = np.sqrt(Pout1 / Pin1) * 100
Eficiencia_ind_2 = np.sqrt(Pout2 / Pin2) * 100

# ==========================================
# GRAFICO: EFICIENCIA INDIVIDUAL VS CORRENTE DE CARGA
# ==========================================
plt.figure(figsize=(8, 6))

# Plotando as curvas
plt.plot(iL1, Eficiencia_ind_1, marker='o', label='Ponto de Operacao 1', color='b', linewidth=2)
plt.plot(iL2, Eficiencia_ind_2, marker='s', label='Ponto de Operacao 2', color='r', linewidth=2)

# Formatacao do grafico
plt.title('Eficiencia Individual (Motor/Gerador) vs. Corrente de Carga', fontsize=14, fontweight='bold')
plt.xlabel('Corrente de Carga iL (A)', fontsize=12, fontweight='bold')
plt.ylabel('Eficiencia Individual (%)', fontsize=12, fontweight='bold')
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend()
plt.tight_layout()

# Mostrar o grafico na tela
plt.savefig('experimento1/curvas/curvaEficienciaCorrente.png')