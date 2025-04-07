import pandas as pd
from scipy.optimize import root

def WtFracCO2(a):
    return (44.01*a)/((1+0.7/0.3)*61.084)

# Opplysninger
w_capture = 0.85
a_3 = 0.21
a_4 = 0.47
wc9 = 1 #vektfraksjon til karbon i strøm 9
wc8 = 0.7
w_MEA = 0.3 

# Initialbetingelser
m1 = 750
wc1 = 0.09
wh1 = 0.03
wn1 = 0.795
wo1 = 0.085

#Intuitive betingelser (som f.eks. wo4 = 0?)
wM9 = 0 # fordi wc9=1.00
wh9 = 0 # --//--

"""
m3 - m7, #vi kan gjøre det lettere for python ved å fjerne m6 og m7, og simpelt sette inn verdier i ettertid, fordi disse strømmene er LIKE
m3 - m6, #min preposition; vi regner BARE for m3 og m4 (samme for vektfraksjonene) da blir de vektfraksjonene under alt vi trenger; 
m4 - m5,

Disse endringene har jeg implementert i massebalansene, (f.eks. wc6 = wc3)

I TILLEGG har jeg implementert disse: 
#Intuitive betingelser (som f.eks. wo4 = 0?)
wM9 = 0 # fordi wc9=1.00
wh9 = 0 # --//--
#All nitrogen og oksygen går til m2 => wo3 = wn3 = wo4 = wn4 =0
wM1 = 0 (bare i selve absorbererkolonnen og i strøm 4->)
wM2 = 0 (det blir ikke sendt ut som avfall)

wh3 = wh4 = 0 (vann dukker bare opp i strøm 8 -- hva er en Stripper/Destillasjonskolonne?) #reflukstanken samler opp vannet i væskeform (separerer vann fra CO2)
vann kommer inn som gass fra m1, slik at den går rett ut i m2 (wh4=0)
"""
def massebalanser():
    def likninger(ukjente):
        m2, m3, m4, m9, wc2, wc3, wc4, wn2, wM3, wM4, wh2, wo2 = ukjente

        return [
        m2*wc2 + m4*wc4 - (m1*wc1 + m3*wc3), #Absorberer;
        m4*wM4 - (m3*wM3),
        m2*wn2 - (m1*wn1),
        m2*wo2 - (m1*wo1),
        m2*wh2 - (m1*wh1),

        m3*wc3 + m9*wc9 - (m4*wc4), #Stripper;
        m3*wM3 - (m4*wM4),

        wc3 + wM3 - 1, #mer for å sørge for at vektfraksjonene går opp
        wc4 + wM4 - 1, 

        m2*wc2 - (1-w_capture)*m1*wc1, 

        wc3 - WtFracCO2(a_3),
        wc4 - WtFracCO2(a_4),

        m4 - (m3 + m9), #m5 = m6 + m9
        m1 + m3 - (m4 + m2), 
        ]

    initialgjett = [650, 1500, 1500, 100, 0.05, 0.05, 0.05, 0.8, 0.95, 0.95, 0.05, 0.10]

    solution = root(likninger, initialgjett, method="lm")

    """
    m9 = m8 uten vann, og m8 inneholder bare vann og CO_2
    m8*wc8 = m9*wc9 = m9
    """
    return solution