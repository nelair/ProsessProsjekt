from scipy.optimize import root
from scipy.integrate import quad
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from constanst8 import Mw
from Massebalanser import massebalanser

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
MEA_og_vann_cp = [As, Bs, Cs]
# heat capacity constants (co2 in monoethanolamine + water solution)
# ---------------------------------------------------------------------
Ac = 0.585      # kJ/(kg K)
Bc = 0.0009     # kJ/(kg K^2)
Cc = 0.0        # kJ/(kg K^3)
blandingshii = [Ac, Bc, Cc]

### Varmeveksler: V-1: 
def cp(i, T): #T må være en integer (ikke float, vet ikke hvorfor)
    A = i[0]
    B = i[1]
    C = i[2]
    return A + B*T + C*(T**2)

w_MEA = 0.3

def cp_sol(T):
    ledd1 = (1-w_MEA)*cp(water_cp, T)
    ledd2 = w_MEA*cp(MEA_cp, T)
    ledd3 = w_MEA*(1-w_MEA)*(As + Bs*T + Cs*w_MEA*((T-273.15)**(-1.5859)))

    return ledd1 + ledd2 + ledd3

integral = lambda f, x0, x1: quad(f, x0, x1)[0] #Integralregning ved hjelp av scipy.integrate.quad

solution_massebalanser = massebalanser()

# Rund alle verdiene i løsningen til 2 desimaler
x = [round(i, 3) for i in solution_massebalanser.x]

wc6 = x[5]
wM6 = x[8]

def V_1_likninger():
    def likninger(ukjente):
        T_ut_varm, A, Q, dTlm = ukjente

        m_kald_inn = m_4 = 974.61
        m_varm_inn = m_6 = 917.23
        
        T_inn_kald = T[3] + 273
        T_ut_kald = T[4] + 273
        T_inn_varm = T[5] + 273

        dT1 = T_inn_varm - T_ut_kald
        dT2 = T_ut_varm - T_inn_kald
        U = 1.100 #kW/(m2*K)
        log_term = np.log(dT1 / dT2) if dT1 != dT2 else 0 #0 vil gi ZeroDivisionError - alltid godt med feilmeldinger.

        return [
            U*A*dTlm - Q, 
            m_kald_inn*integral(lambda T: cp(blandingshii, T), T_inn_kald, T_ut_kald) - Q,
            #m_varm_inn*integral(cp_sol, T_inn_varm, T_ut_varm) + Q,
            m_varm_inn*wM6*integral(cp_sol, T_inn_varm, T_ut_varm) + m_varm_inn*wc6*integral(lambda T: cp(blandingshii, T), T_inn_varm, T_ut_varm) + Q,
            (dT1 - dT2)/log_term - dTlm,
        ]
    initialgjett = [324, 15000, 1e5, 24]

    

    solution = root(likninger, initialgjett, method="hybr")
    print(solution.message)
    print(f"T[6] = {round(solution.x[0],1)} K |333\nA = {round(solution.x[1],2)}m^2 |15503\nQ_v1 = {round(solution.x[2]/1000,2)} MW\ndTlm = {round(solution.x[3],2)} K")
    return solution
    """
    T[6] = {round(solution.x[0],1)} K
    A = {round(solution.x[1],2)}m^2
    Q = {round(solution.x[2]/1e6,2)} MW
    dTlm = {round(solution.x[3],2)} K
    """

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

def V_2_Likninger(): #dette treng ikke å simulere, hvorfor? Se likningene
    #m_10, Q_v2 = ukjente
    #dere burde gjøre utregningen for hånd, for å sjekke om det stemmer !!!!!!!!!!!!!!!!!!!!!   :)

    T_10 = T[9] + 273
    T_11 = T[10] + 273
    T_7 = V_1_likninger().x[0] #henter løsningen fra V-1
    T_3 = T[2] + 273
    m_7 = 917.23 #kg/s 
    dH_fra7_til3 = m_7*integral(cp_sol, T_7, T_3)
    Q_v2 = dH_fra7_til3 #denne er negativ, fordi her tapes det temperatur (T_7>T_3)
    m_10 = -Q_v2/integral(lambda T: cp(water_cp, T), T_10, T_11) 
    #dH_fra10_til11 = m_10*integral(lambda T: cp(water_cp, T), T_10, T_11) #en ny lambda, for å sørge for at den tar integral mhp tempertatur
    print(f"{m_10} | 787")
V_2_Likninger()
##### Kjøler V-3:

"""

Strøm 8: H2O(g) og CO2(g) #ENESTE strøm med h2o som gass. 
Strøm 12: H2O(l) og CO2(g)

Antagelser: Alt vann kondenserer, CO2 forblir i gassfase. Og temperaturuavhengig varmekapasitet for gasser

Kjøler => T_12 < T_8
T_8 = 122 + 273.15 K
T_12 = T_9 = 25 + 273.15 K

Q = dH; 

xc8*m_8*integral(cp(co2(g), T), T_8, T_12)
xh8*m_8*integral(cp(h2o(g), T), T_8, 100+273.15) #ned til kokepunkt
-d_vapH(h2o) = d_fus - d_sub = 6.0 - 50 kJ / mol  = -46 kJ/mol | data fra SI 
xh8*m_8*integral(cp(h2o(aq), T), 100+273.15, T_12)
"""

def V_3_Q():

    xc8 = 0.7 #molfraksjon
    xh8 = 0.3
    wc8 = xc8*Mw[0]/(xc8*Mw[0]+xh8*Mw[1])
    wh8 = 1-wc8
    cp_H2Ogass = 34 #J/Kmol ********************************
    cp_CO2gass = 37 #J/Kmol
    T_8 = 122 + 273
    T_12 = 25 + 273
    m_8 = 67

    a = wc8*m_8/(12.01+16*2)*cp_CO2gass*(T_12-T_8) #enheter: kg/s * mol/g * J/Kmol  * K = kW
    b = wh8*m_8/(18.016)*cp_H2Ogass*(373-T_8) #enheter: kg/s * mol/g * J/Kmol  * K = kW
    c = ((-46 / (18.016))*m_8*wh8)/1000 #enheter: kJ/mol * mol/g * kg/s / 1000 = 1000/1000 kW = kW
    d = wh8*m_8/(18.016)*integral(lambda T: cp(water_cp, T), 373, T_12)
    Q = a+b+c+d
    print(f"Q_v3 = {round(Q/1000, 2)} MW | -30.5")
V_3_Q()