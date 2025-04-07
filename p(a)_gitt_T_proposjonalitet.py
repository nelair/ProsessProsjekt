import numpy as np
import matplotlib.pyplot as plt

# Definer x-verdier, unngå x=1 for å unngå deling på null
x1 = np.linspace(0, 0.49, 50)  # Før asymptoten
x2 = np.linspace(0.51, 1, 50)  # Etter asymptoten
x3 = np.array([i for i in np.linspace(0,1, 100) if i!=0.5]) #en x1 + x2, men denne gjør at funksjonen ser kontinuerlig ut over asymptoten fordi den hopper over 0.5


# Definer funksjonen
f = lambda x: (x**2) / ((1 - 2*x)**2)

# Plott funksjonen på begge sider av asymptoten
plt.plot(x1, f(x1), label=r"$\frac{\alpha^2}{(1-2\alpha)^2}$", color="blue")
#plt.plot(x2, f(x2), color="blue")
#plt.plot(x3, f(x3), label=r"$\frac{\alpha^2}{(1-2\alpha)^2}$", color="blue")

# Tegn asymptoten
plt.axvline(x=0.5, color="red", linestyle="dashed", label=r"Asymptote at $\alpha$=0.5")

# Legg til etiketter og tittel
plt.xlabel(r"$\alpha$")
plt.ylabel(r"$p(CO_2)$")
plt.yscale("log")
plt.title(r"Plot av $p(CO_2)$ som funk av $\alpha$")
plt.legend()
plt.grid()

# Vis plottet
plt.show()
