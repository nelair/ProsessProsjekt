from scipy.optimize import root
from scipy.integrate import quad
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# operation parameters
# ----------------------------------------------------------------------
alpha3   = 0.21  # (mol CO2abs)/(mol amine (MEA))  CO2 loading into absorber
alpha4   = 0.47  # (mol CO2abs)/(mol amine (MEA))  CO2 loading out of absorber
wcapture = 0.85  # kg(CO2,captured)/kg(CO2,feed) CO2 capture rate
eta      = 0.85  # -            efficiency factor (all compressors)
waMEA    = 0.30  # -            weight fraction monoethanolamine (MEA), MEA-sol
U        = 1100  # W/(m^2*K)    heat transfer coefficient
xc8      = 0.7   # -            mole fraction of CO2 in stream 8
wc9      = 1     # -            wt fraction CO2 stream 9

# inlet conditions
# -----------------------------------------------------------------------
m1    = 750    # kg/s       mass flow (total), stream 1
wc1   = 0.09   # -          mass fraction CO2, stream 1
wh1   = 0.03   # -          mass fraction H2O, stream 1
wn1   = 0.795  # -          mass fraction N2,  stream 1
wo1   = 0.085  # -          mass fraction O2,  stream 1

# temperature
# -----------------------------------------------------------------------
T = [None]*11
T[0]  = 30     # degC       stream 1
T[1]  = 30     # degC       stream 2
T[2]  = 30     # degC       stream 3
T[3]  = 50     # degC       stream 4
T[4]  = 111    # degC       stream 5
T[5]  = 122    # degC       stream 6
# T[6] to be calculated
T[7]  = T[4]   # degC       stream 8
T[8]  = 25     # degC       stream 9
T[9]  = 3      # degC       stream 10
T[10] = 22     # degC       stream 11

# heat capacity constants (water)
# ---------------------------------------------------------------------
Aw =     5.0536  # kJ/(kg K)
Bw = -5.6552e-3  # kJ/(kg K^2)
Cw =  9.1400e-6  # kJ/(kg K^3)
water_cp = [Aw, Bw, Cw] 
# heat capacity constants (pure monoethanolamine)
# ---------------------------------------------------------------------
Aa =      -0.64878 # kJ/(kg K)
Ba =     1.6992e-2 # kJ/(kg K^2)
Ca =       -1.9e-5 # kJ/(kg K^3)
MEA_cp = [Aa, Ba, Ca]
# heat capacity constants (monoethanolamine + water solution)
# ---------------------------------------------------------------------
As = -4.9324    # kJ/(kg K)
Bs = 0.01469    # kJ/(kg K^2)
Cs = 69.6243    # kJ/(kg K^(-0.5859)) 
# heat capacity constants (co2 in monoethanolamine + water solution)
# ---------------------------------------------------------------------
Ac = 0.585      # kJ/(kg K)
Bc = 0.0009     # kJ/(kg K^2)
Cc = 0.0
blandingshii = [Ac, Bc, Cc]

### Varmeveksler: V-1: 
def cp(i, T):
    A = i[0]
    B = i[1]
    C = i[2]
    return A + B*T + C*T**2

w_MEA = 0.3

def cp_sol(T):
    ledd1 = (1-w_MEA)*cp(water_cp, T)
    ledd2 = w_MEA*cp(MEA_cp, T)
    ledd3 = w_MEA*(1-w_MEA)*(As + Bs*T + Cs*w_MEA*((T-273.15)**(-1.5859)))

    return ledd1 + ledd2 + ledd3

def likninger(ukjente):
    T_ut_varm, A, Q, dTlm = ukjente

    m_kald_inn = m_4 = 971.61
    m_varm_inn = m_6 = 917.23
    
    T_inn_kald = T[3] + 273
    T_ut_kald = T[4] + 273
    T_inn_varm = T[5] + 273

    dT1 = T_inn_varm - T_ut_kald
    dT2 = T_ut_varm - T_inn_kald

    if dT1 <= 0 or dT2 <= 0:
        return [np.inf, np.inf, np.inf, np.inf]  # Unngå udefinerte verdier


    return [
        U*A*dTlm - Q, 
        m_kald_inn*1000*cp(blandingshii, T_inn_kald)*(T_ut_kald - T_inn_kald) - Q,
        m_varm_inn*1000*cp_sol(T_inn_varm)*(T_ut_varm - T_inn_varm) + Q, 
        (dT1 - dT2)/(np.log(dT1 / dT2)) - dTlm,
    ]

initialgjett = [350, 12000, 1500000, 15]

solution = root(likninger, initialgjett, method="hybr")

if solution.success: 
    print("Løsning funnnet! V-1", solution.message)
if not solution.success:
    print("Fant ingen fullstendig løsning, V-1:", solution.message)
    print("Delsvar som ble funnet:")

print(f"T[6] = {round(solution.x[0],1)}K\nA={round(solution.x[1],2)}m^2\nQ={round(solution.x[2]/1e6,2)}MW\ndTlm={round(solution.x[3],2)}K")

##### Kjøler V-2:

"""
• nødvendig strømningsrate for kjølemedium (medium: H2O (l)) i kjøleren V-2
Ergo det er bare vann i strøm 10 og 11

Q = dH (3->7)
Ifølge simulering synker temperaturen fra strøm 7 til 3 (ergo kjøler)

-Q = dH (10->11)

H = mc_p*(dT) |ved isobar prosess (om jeg husker riktig)

dH = m_10*integral(cp(H2O, T), fra T(10) til T(11)) = -Q_v2    | eq1
dH = m_7*integral(cp_sol(T_inn_varm) fra T7 til T3) = Q_v2     | eq2
"""
def V_2_Likninger(ukjente):
    m_10, Q_v2 = ukjente

    T_10 = T[9] + 273
    T_11 = T[10] + 273
    T_7 = solution.x[0] + 273 #henter løsningen fra V-1
    T_3 = T[2] + 273
    m_7 = 917.23 #kg/s 

    return [
        m_10*cp(water_cp, T_10)*(T_11-T_10) - (Q_v2),
        m_7*cp_sol(T_7)*(T_3-T_7) + Q_v2,
    ]

initialgjett_v2 = [500, 1000] #idk hva som er bra

solution = root(V_2_Likninger, initialgjett_v2, method="hybr")

if solution.success: 
    print("Løsning funnnet! V-2", solution.message)
if not solution.success:
    print("Fant ingen fullstendig løsning, V-2:", solution.message)
    print("Delsvar som ble funnet:")

print(f"m_10 = m_11 {round(solution.x[0],1)} kg/s\nQ_v2={round(solution.x[1]/1e3,2)} MW")