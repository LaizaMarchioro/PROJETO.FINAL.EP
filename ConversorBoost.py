#LAIZA MARCHIORO
#Projeto Final Eletrônica de Potência 
#Conversor Boost 

import numpy as np
import matplotlib.pyplot as plt


Vin = 12         
D = 0.6           # Razão Ciclica (Duty Cycle)
R = 10            
L = 1e-3          
C = 100e-6       
f = 100e3         # Frequência de chaveamento 
T = 1 / f         # Período de chaveamento 

#  PARTE 1: Formas de onda em um período
dt = T / 1000                 #dt define o passo de tempo para 1000 passos por período
t = np.arange(0, T, dt)
N = len(t)                               # N recebe o valor do comprimento de t

#Vetores para:
iL = np.zeros(N)      # Corrente no indutor
vL = np.zeros(N)      # Tensão no indutor
s = np.zeros(N)       # Estado da chave (0 ou 1)

IL = 0                # Corrente inicial
Vout = Vin / (1 - D)    # Tensão de Saída



for n in range(1, N):
    if t[n] < D * T:       #Durante o tempo D*T, a chave está fechada, o indutor carrega.
        dIL = Vin / L
        VL = Vin
        s[n] = 1          #Salva o estado da chave como ligada (1) no instante de tempo.
    else:                   #No restante, a chave abre, o indutor descarrega na carga.
        dIL = (Vin - Vout) / L 
        VL = Vin - Vout
        s[n] = 0
    IL += dIL * dt            #Atualiza a corrente em L com a derivada da corrente e no passo de tempo dt (quanto a corrente no L muda a cada passo de tempo). #Equiuivale IL2 = IL2 + (dIL * dt2) 
    iL[n] = IL
    vL[n] = VL         #armazena 'salva' os valores calculados 



# PARTE 2: Simulação da saída em vários ciclos (para 50ms) 
t_total = 5e-2
dt2 = T / 100
N2 = int(t_total / dt2)
t2 = np.linspace(0, t_total, N2)

iL2 = np.zeros(N2)
vC2 = np.zeros(N2)
IL2 = 0
Vout2 = 0


for n in range(1, N2):       #essa simulação é por um periodo maior, para gerar o gráfico da tensão de saída durante vários ciclos #Começa de 1 porque os valores em n = 0 já foram definidos.
    if (n % int(T/dt2)) < int(D*T/dt2): #T/dt2 → número de passos de tempo por período. #(n % int(T/dt2)) → local no do período de chaveamento atual. 
        dIL = Vin / L                        #int(D*T/dt2) → quantos passos a chave fica ligada dentro do período.
        VL = Vin
    else:
        dIL = (Vin - Vout2) / L
        VL = Vin - Vout2
        dVC = (IL2 - Vout2 / R) / C       # taxa de variação da tensão no capacitor.  #Lei dos nós Ic+Ir=Il2
        Vout2 += dVC * dt2                #Atualiza a tensão de saída com base na derivada da tensão e no passo de tempo dt2.
    IL2 += dIL * dt2
    iL2[n] = IL2                          #armaena valores
    vC2[n] = Vout2


# CÁLCULOS ANALÍTICOS 
Vout_calc = Vin / (1 - D)
Iout = Vout_calc / R
IL_calc = Iout * (1 - D)
delta_IL = (Vin * D) / (L * f)



print("RESULTADOS")
print(f"Tensão de saída teórica: {Vout_calc:.2f} V")
print(f"Corrente média de saída (Iout): {Iout:.2f} A")
print(f"Corrente média no indutor (IL): {IL_calc:.2f} A")
print(f"Ripple da corrente no indutor (ΔiL): {delta_IL*1000:.2f} mA")


#Gráficos divididos em três figuras

# Fig. 1: Formas de onda no indutor (um período/ciclo)
fig1, axs = plt.subplots(3, 1, figsize=(10, 7), sharex=True)

axs[0].plot(t * 1e6, s, color='black')
axs[0].set_title('Estado da Chave (S)')         #Estadi da chave (0 ou 1)
axs[0].set_ylabel('S')
axs[0].set_ylim([-0.1, 1.1])
axs[0].grid(True)

axs[1].plot(t * 1e6, vL, color='blue')
axs[1].set_title('Tensão no Indutor (vL)')          #Tensão no indutor
axs[1].set_ylabel('Tensão (V)')
axs[1].set_yticks(np.round(np.linspace(np.min(vL), np.max(vL), 6), 1))
axs[1].grid(True)

axs[2].plot(t * 1e6, iL, color='red')
axs[2].set_title('Corrente no Indutor (iL)')
axs[2].set_xlabel('Tempo (μs)')                           #Corrente no indutor
axs[2].set_ylabel('Corrente (A)')
axs[2].set_yticks(np.round(np.linspace(np.min(iL), np.max(iL), 6), 2))
axs[2].grid(True)

fig1.tight_layout()


# Fig. 2: Tensão de saída ao longo do tempo
fig2, ax2 = plt.subplots(figsize=(8, 4))
ax2.plot(t2 * 1e3, vC2, label='Tensão de saída simulada')                       #tensão de saída cresce até atingir o valor ideal.
ax2.axhline(Vout_calc, color='r', linestyle='--', label='Vout teórica')
ax2.set_title('Tensão de Saída (Vout) ao longo do tempo')
ax2.set_xlabel('Tempo (ms)')
ax2.set_ylabel('Tensão (V)')
ax2.legend()
ax2.grid(True)
ax2.set_yticks(np.round(np.linspace(min(vC2), max(vC2)+1, 6), 1))

fig2.tight_layout()

# Fig. 3: Curva Vout x Razão Cíclica
D_curve = np.linspace(0.01, 0.99, 500)
Vo_curve = Vin / (1 - D_curve)

fig3, ax3 = plt.subplots(figsize=(6, 4))
ax3.plot(D_curve, Vo_curve, color='purple')
ax3.set_title('Tensão de Saída Teórica vs Duty Cycle')            #Mostra a relação teórica entre a tensão de saída e a razão cíclica. Aumentar o D aumenta a tensão de saída.
ax3.set_xlabel('Duty Cycle (D)')
ax3.set_ylabel('Tensão de Saída (V_o)')
ax3.grid(True)
ax3.set_xlim([0, 1])
ax3.set_ylim([Vin, np.max(Vo_curve)])
ax3.set_yticks(np.round(np.linspace(Vin, np.max(Vo_curve), 7), 1))

fig3.tight_layout()

plt.show()