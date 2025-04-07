# ----------------------------------------------------------------------
# purpose: CONSTANTS for CO2 CAPTURE PROJECT 2015
# author:  camilla.berge.vik@ntnu.no (CBV)
# author:  ole.h.bjorkedal@ntnu.no   (OHB)
# date:    03.05.2013
# revised: 07.03.2014, 09.01.2015, 23.01.2015, 07.03.2017
# note:    Adapted from matlab to python-syntax by OHB 07.03.2017
# set 8
# ----------------------------------------------------------------------

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


# pressure
# ----------------------------------------------------------------------
p = [None]*9
p[0] = 1       # bar        stream 1
p[1] = 1       # bar        stream 2
p[2] = 1       # bar        stream 3
p[3] = 1       # bar        stream 4
p[4] = 2       # bar        stream 5
p[5] = 2       # bar        stream 6
p[6] = 2       # bar        stream 7
p[7] = p[4]    # bar        stream 8
p[8] = 2       # bar        stream 9

# molar masses
# ----------------------------------------------------------------------
Mw = [None]*4
Mw[0] = 44.01      # g/mole     CO2
Mw[1] = 18.015     # g/mole     H2O
Mw[2] = 28.015     # g/mole     N2
Mw[3] = 31.998     # g/mole     O2
MwMEA = 61.08      # g/mole     MEA

# enthalpies 
# ---------------------------------------------------------------------
hf = [None]*4
hf[0] =    -8933 # kJ/kg      std enth. of formation of CO2
hf[1] = -13423.3 # kJ/kg      std enth. of formation of H2O
hf[2] = 	   0 # kJ/kg      std enth. of formation of N2
hf[3] =        0 # kJ/kg      std enth. of formation of O2
hfsol =   -13599 # kJ/kg      std enth. of formation of 30 wt# MEA-sol
habs_m =      80 # kJ/mol(abs.CO2) delta h absorption per mol absorbed co2

# heat capacity (pure gases)
# ---------------------------------------------------------------------
cpg = [None]*4
cpg[0] = 0.868    # kJ/(kgK)   heat capacity at 40 deg C for CO2
cpg[1] = 1.866    # kJ/(kgK)   heat capacity at 40 deg C for H2O
cpg[2] = 1.040    # kJ/(kgK)   heat capacity at 40 deg C for N2
cpg[3] = 0.919    # kJ/(kgK)   heat capacity at 40 deg C for O2

# heat capacity constants (water)
# ---------------------------------------------------------------------
Aw =     5.0536  # kJ/(kg K)
Bw = -5.6552e-3  # kJ/(kg K^2)
Cw =  9.1400e-6  # kJ/(kg K^3)

# heat capacity constants (pure monoethanolamine)
# ---------------------------------------------------------------------
Aa =      -0.64878 # kJ/(kg K)
Ba =     1.6992e-2 # kJ/(kg K^2)
Ca =       -1.9e-5 # kJ/(kg K^3)

# heat capacity constants (monoethanolamine + water solution)
# ---------------------------------------------------------------------
As = -4.9324    # kJ/(kg K)
Bs = 0.01469    # kJ/(kg K^2)
Cs = 69.6243    # kJ/(kg K^(-0.5859)) 

# heat capacity constants (co2 in monoethanolamine + water solution)
# ---------------------------------------------------------------------
Ac = 0.585      # kJ/(kg K)
Bc = 0.0009     # kJ/(kg K^2)

# henry's constant as a function of temperature
# ---------------------------------------------------------------------
Hc = [None]*5
Hc[0] = 4.96563e2 # kPa m^3 mol^-1      c1
Hc[1] = 3.41697e5 # kPa m^3 mol^-1 K    c2
Hc[2] = 1.69131e0 # -                   c3
Hc[3] = 1.47225e3 # K                   c4
Hc[4] = 1.28338e5 # K^2                 c5

# enthalpy of vaporisation (condensation) for water at 298 K
# ---------------------------------------------------------------------
dHfus = 6.0       # kJ mol^-1 
dHsub = 50        # kJ mol^-1

# misc. constants
# ----------------------------------------------------------------------
Tref_K   = 298   # K            reference temperature, K
Tref_C   =  25   # C            reference temperature, C
gasConst = 8.314 # J/(K mol)    universal gas constant