import matplotlib.pyplot as plt
import numpy as np
import os

# Diretório de saída
output_dir = 'experimento4/curvas'
os.makedirs(output_dir, exist_ok=True)

# ----------------------------------------------------
# 1. Configurações e Parâmetros do Motor
# ----------------------------------------------------
Y_AXIS_MAX = 23
X_AXIS_MIN = 3
X_AXIS_MAX = 17
LIMITE_Y_CURVAS_V = 22

TENSAO_LINHA = 220   # Volts (V_L) - Assumido padrão, altere se necessário
POTENCIA_ALVO = 1900 # Watts (1.9 kW)
FP_ALVO = 0.9        # Fator de Potência

# ----------------------------------------------------
# 2. Entrada de Dados
# ----------------------------------------------------
if_leve = [5.54, 5.92, 6.55, 7.10, 7.52, 8.08, 8.52, 8.98, 9.60, 10.00, 10.62, 11.05, 11.55, 12.04, 12.44, 13.12]
ia_leve = [13.72, 11.92, 9.24, 7.24, 6.33, 3.55, 3.23, 2.02, 3.03, 4.36, 6.83, 8.26, 9.67, 11.26, 13.25, 16.03]

if_media = [6.75, 7.05, 7.24, 8.88, 9.45, 10.14, 10.62, 11.02, 11.49]
ia_media = [12.21, 11.52, 10.88, 8.30, 8.67, 9.85, 10.75, 12.08, 13.30]

if_alta = [7.55, 8.02, 8.47, 9.28, 10.15]
ia_alta = [13.40, 12.17, 11.85, 11.62, 12.60]

# ----------------------------------------------------
# 3. Funções Matemáticas: Ajuste Hiperbólico
# ----------------------------------------------------
def ajustar_hiperbole(x_raw, y_raw):
    A, B, C = np.polyfit(x_raw, np.array(y_raw)**2, 2)
    fp_x = -B / (2 * A)
    fp_y = np.sqrt(C - (B**2) / (4 * A))
    
    x_smooth = np.linspace(X_AXIS_MIN - 1, X_AXIS_MAX + 1, 1000)
    conteudo_raiz = A * x_smooth**2 + B * x_smooth + C
    conteudo_raiz[conteudo_raiz < 0] = 0 
    y_smooth = np.sqrt(conteudo_raiz)
    
    mask = (y_smooth <= LIMITE_Y_CURVAS_V)
    return (A, B, C), x_smooth[mask], y_smooth[mask], fp_x, fp_y

# Modelos Originais
mod_leve, x_leve_s, y_leve_s, fpx_leve, fpy_leve = ajustar_hiperbole(if_leve, ia_leve)
mod_media, x_media_s, y_media_s, fpx_media, fpy_media = ajustar_hiperbole(if_media, ia_media)
mod_alta, x_alta_s, y_alta_s, fpx_alta, fpy_alta = ajustar_hiperbole(if_alta, ia_alta)

# ----------------------------------------------------
# 4. Interpolação da Curva de 1.9 kW e Ponto de Operação
# ----------------------------------------------------
# Ia mínimo alvo (onde FP = 1) para 1.9 kW
ia_min_alvo = POTENCIA_ALVO / (np.sqrt(3) * TENSAO_LINHA)

# Interpolação dos coeficientes hiperbólicos
A_orig, B_orig, C_orig = zip(mod_leve, mod_media, mod_alta)
ia_mins_orig = [fpy_leve, fpy_media, fpy_alta]

poly_A = np.polyfit(ia_mins_orig, A_orig, 2)
poly_B = np.polyfit(ia_mins_orig, B_orig, 2)
poly_C = np.polyfit(ia_mins_orig, C_orig, 2)

A_novo = np.polyval(poly_A, ia_min_alvo)
B_novo = np.polyval(poly_B, ia_min_alvo)
C_novo = np.polyval(poly_C, ia_min_alvo)

# Curva interpolada
x_novo = np.linspace(X_AXIS_MIN - 1, X_AXIS_MAX + 1, 1000)
conteudo_raiz = A_novo * x_novo**2 + B_novo * x_novo + C_novo
conteudo_raiz[conteudo_raiz < 0] = 0
y_novo = np.sqrt(conteudo_raiz)

# Máscara de limite
mask_novo = (y_novo <= LIMITE_Y_CURVAS_V)
x_novo = x_novo[mask_novo]
y_novo = y_novo[mask_novo]

# Cálculo do Ponto Exato (FP 0.9 Indutivo)
ia_target = ia_min_alvo / FP_ALVO
delta = B_novo**2 - 4 * A_novo * (C_novo - ia_target**2)
if_estimado = (-B_novo - np.sqrt(delta)) / (2 * A_novo)

# ----------------------------------------------------
# 5. Geração do Gráfico Completo
# ----------------------------------------------------
plt.figure(figsize=(12, 8))

# 5.1 Plota as Curvas Originais de Referência
plt.plot(x_leve_s, y_leve_s, color='royalblue', linewidth=1.5, alpha=0.5, label='Curvas Base (Aproximação)')
plt.plot(x_media_s, y_media_s, color='darkorange', linewidth=1.5, alpha=0.5)
plt.plot(x_alta_s, y_alta_s, color='forestgreen', linewidth=1.5, alpha=0.5)

plt.scatter(if_leve, ia_leve, color='royalblue', marker='o', alpha=0.3)
plt.scatter(if_media, ia_media, color='darkorange', marker='s', alpha=0.3)
plt.scatter(if_alta, ia_alta, color='forestgreen', marker='^', alpha=0.3)

# Plota a linha guia FP = 1.0 Original
def plotar_curva_fp_suave(x_pts, y_pts, color, marker, linestyle):
    coefs = np.polyfit(y_pts, x_pts, 2)
    poly = np.poly1d(coefs)
    y_smooth = np.linspace(min(y_pts), max(y_pts), 100)
    plt.plot(poly(y_smooth), y_smooth, linestyle=linestyle, color=color, linewidth=1.5, alpha=0.5)
    plt.plot(x_pts, y_pts, marker=marker, linestyle='None', color=color, markersize=6, alpha=0.5)

plotar_curva_fp_suave([fpx_leve, fpx_media, fpx_alta], [fpy_leve, fpy_media, fpy_alta], 'red', 'D', '--')

# 5.2 Plota a Curva Estimada (Destaque)
plt.plot(x_novo, y_novo, color='crimson', linewidth=3, linestyle='-', label=f'Curva Estimada ({POTENCIA_ALVO/1000} kW)')

# Destaca o ponto operacional
plt.plot(if_estimado, ia_target, marker='X', color='black', markersize=10, label=f'Operação (FP {FP_ALVO} Indutivo)')

# Linhas tracejadas até os eixos
plt.plot([X_AXIS_MIN, if_estimado], [ia_target, ia_target], color='gray', linestyle='--', alpha=0.7)
plt.plot([if_estimado, if_estimado], [0, ia_target], color='gray', linestyle='--', alpha=0.7)

# Anotação
bbox_props = dict(boxstyle="round,pad=0.4", fc="white", ec="black", lw=1)
plt.annotate(f"Estimativa:\nIf = {if_estimado:.2f} A\nIa = {ia_target:.2f} A", 
             xy=(if_estimado, ia_target), 
             xytext=(if_estimado - 3.5, ia_target + 2),
             arrowprops=dict(facecolor='black', shrink=0.05, width=1.5, headwidth=6),
             fontsize=11, fontweight='bold', bbox=bbox_props)

# 5.3 Estética e Limites (Idêntico aos anteriores)
plt.title(f'Estimativa de Excitação (Potência = {POTENCIA_ALVO/1000} kW | V_linha = {TENSAO_LINHA}V)', fontsize=14, fontweight='bold')
plt.xlabel('Corrente de Campo - If (A)', fontsize=12)
plt.ylabel('Corrente de Armadura - Ia (A)', fontsize=12)
plt.grid(True, linestyle='--', alpha=0.6)

plt.xlim(X_AXIS_MIN, X_AXIS_MAX)
plt.ylim(0, Y_AXIS_MAX)
plt.yticks(np.arange(0, Y_AXIS_MAX, step=2))

# Legenda agrupada
handles, labels = plt.gca().get_legend_handles_labels()
# Remove itens duplicados (para as 3 curvas base ficarem em um único ícone na legenda)
by_label = dict(zip(labels, handles))
plt.legend(by_label.values(), by_label.keys(), loc='lower right', fontsize=10)

plt.tight_layout()
plt.savefig(f'{output_dir}/estimativa_fp09_contextualizada.png', bbox_inches='tight')
plt.show()