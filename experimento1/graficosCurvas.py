import matplotlib.pyplot as plt
import numpy as np
import os

# Certifica-se de que a pasta existe (opcional, evita erro no savefig)
os.makedirs('experimento1/curvas', exist_ok=True)

# Extracao de Dados
# Ponto 1 (Operacao 1)
n1 = np.array([1500, 1500, 1213, 1142, 1107])
Va1 = np.array([106.4, 94.4, 88.1, 83.1, 81.8])
Ia1 = np.array([3.25, 6.0, 7.5, 8.0, 8.5])
VL1 = np.array([110.9, 91.5, 81.0, 75.3, 72.0])
iL1 = np.array([0.0, 2.8, 4.34, 5.14, 5.64])

# Ponto 2 (Operacao 2)
n2 = np.array([1500, 1200, 1047, 971, 922.6])
Va2 = np.array([99.5, 81.2, 72.3, 67.8, 65.1])
Ia2 = np.array([3.0, 6.0, 7.5, 8.5, 8.5])
VL2 = np.array([108.9, 82.9, 70.1, 63.5, 59.7])
iL2 = np.array([0.0, 2.67, 4.0, 4.71, 5.11])

# Calculos Ponto 1
omega1 = n1 * 2 * np.pi / 60
Pin1 = Va1 * Ia1
Pout1 = VL1 * iL1
Eficiencia1 = (Pout1 / Pin1) * 100
Torque1 = Pin1 / omega1 

# Calculos Ponto 2
omega2 = n2 * 2 * np.pi / 60
Pin2 = Va2 * Ia2
Pout2 = VL2 * iL2
Eficiencia2 = (Pout2 / Pin2) * 100
Torque2 = Pin2 / omega2 


# ==========================================
# GRAFICO 1: CONJUGADO VS VELOCIDADE
# ==========================================
plt.figure(figsize=(8, 6))

# Plotagem dos dados (linha tracejada fina, pontos redondos menores)
plt.plot(Torque1, n1, marker='o', markersize=4, linestyle='--', color='b', linewidth=1, alpha=0.6, label='Dados P1')
plt.plot(Torque2, n2, marker='o', markersize=4, linestyle='--', color='r', linewidth=1, alpha=0.6, label='Dados P2')

# Curvas de Tendência (Polinômio de grau 2)
# Ponto 1
z1 = np.polyfit(Torque1, n1, 3)
p1 = np.poly1d(z1)
t1_linha = np.linspace(min(Torque1), max(Torque1), 100)
plt.plot(t1_linha, p1(t1_linha), linestyle='-', color='b', linewidth=2, label='Tendência P1')

# Ponto 2
z2 = np.polyfit(Torque2, n2, 3)
p2 = np.poly1d(z2)
t2_linha = np.linspace(min(Torque2), max(Torque2), 100)
plt.plot(t2_linha, p2(t2_linha), linestyle='-', color='r', linewidth=2, label='Tendência P2')

plt.xlabel('Conjugado (N.m)', fontsize=12, fontweight='bold')
plt.ylabel('Velocidade (rpm)', fontsize=12, fontweight='bold')
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend()
plt.tight_layout()

# Salvar o grafico 1
plt.savefig('experimento1/curvas/curvaConjugadoVelocidade.png')


# ==========================================
# GRAFICO 2: EFICIENCIA VS VELOCIDADE
# ==========================================
plt.figure(figsize=(8, 6))

# Plotagem dos dados (linha tracejada fina, pontos redondos menores)
plt.plot(n1, Eficiencia1, marker='o', markersize=4, linestyle='--', color='b', linewidth=1, alpha=0.6, label='Dados P1')
plt.plot(n2, Eficiencia2, marker='o', markersize=4, linestyle='--', color='r', linewidth=1, alpha=0.6, label='Dados P2')

# Curvas de Tendência (Polinômio de grau 2)
# Ponto 1
z3 = np.polyfit(n1, Eficiencia1, 3)
p3 = np.poly1d(z3)
n1_linha = np.linspace(min(n1), max(n1), 100)
plt.plot(n1_linha, p3(n1_linha), linestyle='-', color='b', linewidth=2, label='Tendência P1')

# Ponto 2
z4 = np.polyfit(n2, Eficiencia2, 3)
p4 = np.poly1d(z4)
n2_linha = np.linspace(min(n2), max(n2), 100)
plt.plot(n2_linha, p4(n2_linha), linestyle='-', color='r', linewidth=2, label='Tendência P2')

plt.xlabel('Velocidade (rpm)', fontsize=12, fontweight='bold')
plt.ylabel('Eficiência (%)', fontsize=12, fontweight='bold')
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend()
plt.tight_layout()

# Salvar o grafico 2
plt.savefig('experimento1/curvas/curvaEficienciaVelocidade.png')