import matplotlib.pyplot as plt
import numpy as np
import os

# Diretório de saída
output_dir = 'experimento4/curvas'
os.makedirs(output_dir, exist_ok=True)

# ----------------------------------------------------
# 1. Configurações de Limites do Gráfico
# ----------------------------------------------------
Y_AXIS_MAX = 23
X_AXIS_MIN = 3
X_AXIS_MAX = 17

# Limite onde a curva V é "cortada" para terminar graciosamente dentro do gráfico
LIMITE_Y_CURVAS_V = 22

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
# 3. Funções Matemáticas
# ----------------------------------------------------
def ajustar_hiperbole(x_raw, y_raw):
    A, B, C = np.polyfit(x_raw, np.array(y_raw)**2, 2)
    
    fp_x = -B / (2 * A)
    fp_y = np.sqrt(C - (B**2) / (4 * A))
    
    x_smooth = np.linspace(X_AXIS_MIN - 1, X_AXIS_MAX + 1, 1000)
    conteudo_raiz = A * x_smooth**2 + B * x_smooth + C
    conteudo_raiz[conteudo_raiz < 0] = 0 
    y_smooth = np.sqrt(conteudo_raiz)
    
    # MÁSCARA: Corta a curva para não encostar na borda do gráfico
    mask = (y_smooth <= LIMITE_Y_CURVAS_V)
    x_smooth = x_smooth[mask]
    y_smooth = y_smooth[mask]
    
    return (A, B, C), x_smooth, y_smooth, fp_x, fp_y

def encontrar_raizes_fp(A, B, C, fp_y, fator_potencia):
    ia_target = fp_y / fator_potencia
    c_eq = C - ia_target**2
    delta = B**2 - 4 * A * c_eq
    
    if delta < 0: return None, None
    
    if_indutivo = (-B - np.sqrt(delta)) / (2 * A)
    if_capacitivo = (-B + np.sqrt(delta)) / (2 * A)
    
    return if_indutivo, if_capacitivo

mod_leve, x_leve_s, y_leve_s, fpx_leve, fpy_leve = ajustar_hiperbole(if_leve, ia_leve)
mod_media, x_media_s, y_media_s, fpx_media, fpy_media = ajustar_hiperbole(if_media, ia_media)
mod_alta, x_alta_s, y_alta_s, fpx_alta, fpy_alta = ajustar_hiperbole(if_alta, ia_alta)

# ----------------------------------------------------
# 4. Funções Auxiliares de Plotagem
# ----------------------------------------------------
def configurar_grafico(titulo):
    plt.title(titulo, fontsize=14, fontweight='bold')
    plt.xlabel('Corrente de Campo - If (A)', fontsize=12)
    plt.ylabel('Corrente de Armadura - Ia (A)', fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.xlim(X_AXIS_MIN, X_AXIS_MAX)
    # A borda vai até 19, mas as curvas param no 17.5 ou na Carga Alta
    plt.ylim(0, Y_AXIS_MAX) 
    plt.yticks(np.arange(0, Y_AXIS_MAX, step=2))

def plotar_curva_individual(x_raw, y_raw, x_smooth, y_smooth, fpx, fpy, label, cor, filename):
    plt.figure(figsize=(10, 6))
    plt.plot(x_smooth, y_smooth, color=cor, linewidth=2, label=f'Aproximação ({label})')
    plt.scatter(x_raw, y_raw, color=cor, marker='o', alpha=0.5, label='Dados Medidos')
    plt.plot(fpx, fpy, marker='D', markersize=8, color='red', linestyle='None', label=f'FP Unitário ({fpx:.2f}, {fpy:.2f})')
    
    configurar_grafico(f'Curva V - {label}')
    plt.legend(loc='best')
    plt.tight_layout()
    plt.savefig(f'{output_dir}/{filename}', bbox_inches='tight')
    plt.close()

def plotar_curva_fp_suave(x_pts, y_pts, label, color, marker, linestyle):
    """Ajusta e plota a curva suave dos Fatores de Potência sem extrapolar"""
    if len(x_pts) >= 3:
        coefs = np.polyfit(y_pts, x_pts, 2)
        poly = np.poly1d(coefs)
        
        # O SEGREDO ESTÁ AQUI: Limita exatamente entre a Carga Leve e a Carga Alta
        y_smooth = np.linspace(min(y_pts), max(y_pts), 100)
        x_smooth = poly(y_smooth)
        
        plt.plot(x_smooth, y_smooth, linestyle=linestyle, color=color, linewidth=1.5, label=label)
        plt.plot(x_pts, y_pts, marker=marker, linestyle='None', color=color, markersize=7)

# ----------------------------------------------------
# 5. Geração das Imagens
# ----------------------------------------------------

# Imagem 1, 2 e 3: Curvas Individuais
plotar_curva_individual(if_leve, ia_leve, x_leve_s, y_leve_s, fpx_leve, fpy_leve, 'Carga Leve', 'royalblue', 'curva_leve.png')
plotar_curva_individual(if_media, ia_media, x_media_s, y_media_s, fpx_media, fpy_media, 'Carga Média', 'darkorange', 'curva_media.png')
plotar_curva_individual(if_alta, ia_alta, x_alta_s, y_alta_s, fpx_alta, fpy_alta, 'Carga Alta', 'forestgreen', 'curva_alta.png')

plot_args = [
    (x_leve_s, y_leve_s, if_leve, ia_leve, 'royalblue', 'Carga Leve', 'o'),
    (x_media_s, y_media_s, if_media, ia_media, 'darkorange', 'Carga Média', 's'),
    (x_alta_s, y_alta_s, if_alta, ia_alta, 'forestgreen', 'Carga Alta', '^')
]

fp_1_x = [fpx_leve, fpx_media, fpx_alta]
fp_1_y = [fpy_leve, fpy_media, fpy_alta]

# Imagem 4: As Três Curvas Juntas
plt.figure(figsize=(12, 8))
for x_s, y_s, x_r, y_r, cor, lbl, m in plot_args:
    plt.plot(x_s, y_s, label=lbl, color=cor, linewidth=2)
    plt.scatter(x_r, y_r, color=cor, marker=m, alpha=0.4)

plotar_curva_fp_suave(fp_1_x, fp_1_y, 'FP = 1.0', 'red', 'D', '--')

configurar_grafico('Curvas V da Máquina Síncrona')
plt.legend(loc='upper right', fontsize=10)
plt.tight_layout()
plt.savefig(f'{output_dir}/curvas_todas.png', bbox_inches='tight')
plt.close()

# Imagem 5: As Três Curvas + Fatores de Potência Constantes
alvos_fp = [0.8, 0.6]
pontos_fp = {0.8: {'ind_x': [], 'ind_y': [], 'cap_x': [], 'cap_y': []},
             0.6: {'ind_x': [], 'ind_y': [], 'cap_x': [], 'cap_y': []}}
dados = [(mod_leve, fpx_leve, fpy_leve), (mod_media, fpx_media, fpy_media), (mod_alta, fpx_alta, fpy_alta)]

for mod, fp_x, fp_y in dados:
    A, B, C = mod
    for fp in alvos_fp:
        ia_target = fp_y / fp
        if_ind, if_cap = encontrar_raizes_fp(A, B, C, fp_y, fp)
        
        if if_ind is not None:
            pontos_fp[fp]['ind_x'].append(if_ind)
            pontos_fp[fp]['ind_y'].append(ia_target)
        if if_cap is not None:
            pontos_fp[fp]['cap_x'].append(if_cap)
            pontos_fp[fp]['cap_y'].append(ia_target)

plt.figure(figsize=(12, 8))
for x_s, y_s, x_r, y_r, cor, lbl, m in plot_args:
    plt.plot(x_s, y_s, label=lbl, color=cor, linewidth=2)
    plt.scatter(x_r, y_r, color=cor, marker=m, alpha=0.3)

plotar_curva_fp_suave(fp_1_x, fp_1_y, 'FP = 1.0', 'red', 'D', '--')

estilos = {0.8: ('purple', 's'), 0.6: ('brown', 'v')}
for fp in alvos_fp:
    cor, marcador = estilos[fp]
    lbl = str(fp).replace('.', ',')
    
    if len(pontos_fp[fp]['ind_x']) == 3:
        plotar_curva_fp_suave(pontos_fp[fp]['ind_x'], pontos_fp[fp]['ind_y'], 
                              f'FP = {lbl} Indutivo', cor, marcador, '-.')
    
    if len(pontos_fp[fp]['cap_x']) == 3:
        plotar_curva_fp_suave(pontos_fp[fp]['cap_x'], pontos_fp[fp]['cap_y'], 
                              f'FP = {lbl} Capacitivo', cor, marcador, ':')

configurar_grafico('Curvas V e Curvas de Fator de Potência Constante')
plt.legend(loc='upper center', bbox_to_anchor=(0.5, 0.98), fontsize=10, ncol=3) 
plt.tight_layout()
plt.savefig(f'{output_dir}/curvas_todas_fp_constante.png', bbox_inches='tight')
plt.show()