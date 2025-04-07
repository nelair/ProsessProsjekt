from Massebalanser import massebalanser
from constanst8 import * #importerer alt fra constanst8.py
import pandas as pd #pandas bruker for å printe ut verdiene i en tabellform
from Energibalanser import V_1_likninger, V_2_Likninger, V_3_Q, cp, cp_sol
# Opplysninger
w_capture = 0.85
a_3 = 0.21
a_4 = 0.47
wc9 = 1 #vektfraksjon til karbon i strøm 9
xc8 = 0.7
w_MEA = 0.3 
xh8 = 1-xc8
wc8 = xc8*Mw[0]/(xc8*Mw[0]+xh8*Mw[1])
print(f"WC8: {wc8})")

# Initialbetingelser
m1 = 750
wc1 = 0.09
wh1 = 0.03
wn1 = 0.795
wo1 = 0.085

#Intuitive betingelser (som f.eks. wo4 = 0?)
wM9 = 0 # fordi wc9=1.00
wh9 = 0 # --//--
solution_massebalanser = massebalanser()

# Rund alle verdiene i løsningen til 2 desimaler
x = [round(i, 3) for i in solution_massebalanser.x]

T_6 = float(V_1_likninger().x[0])  # Kelvin

Temperaturer = [T[i] for i in range(6)] + [T_6 - 273.15] + [T[i] for i in range(7, 9)] #T[i] er importert fra constanst8.py
Temperaturer = [round(i + 273.15,2) for i in Temperaturer]  # Tilbake til Kelvin

massestrømmer = [m1] + [x[i] for i in range(3)] + [x[2], x[1], x[1], x[3]/wc8, x[3]]
entalpiverdier = [None]*9

entalpiverdier[6] = float(massestrømmer[6]*cp_sol(Temperaturer[6])) #endrer verdien til i strøm 7 fra None til den faktiske verdien
entalpiverdier[2] = float(massestrømmer[2]*cp_sol(Temperaturer[2])) #*************PER MOL SKAL HA PER KG**************************************


data = {
    "T [K]": Temperaturer,
    "p [bar]": [p[i] for i in range(9)], #importert fra constanst8.py
    "h [kJ/kg]": entalpiverdier,
    "m [kg/s]": [int(i) for i in massestrømmer],
    r"CO_2(g)": [wc1] + [x[4]] + [0.00]*5 + [wc8, wc9], 
    r"H_2O": [wh1] + [x[10]] + [0.00]*5 + [1 - wc8, 0.00],
    r"N_2": [wn1] + [x[7]] + [0.00]*7,
    r"O_2": [wo1] + [x[11]] + [0.00]*7,
    r"MEA": [0.00] + [0.00, x[8], x[9], x[9], x[8], x[8], 0.00, 0.00],
    r"CO_2(aq)": [0.00, 0.00, x[5], x[6], x[6], x[5], x[5], 0.00, 0.00],
}

df = pd.DataFrame(data, index=["m1", "m2", "m3", "m4", "m5", "m6", "m7", "m8", "m9"])
df = df.apply(lambda col: col.round(3))
print(df)