import numpy as np
import matplotlib.pyplot as plt
import os

def K_H(T, a):
    c1, c2, c3, c4, c5 = 4.966563e2, 3.41697e5, 1.169131, 1.47225, 1.28338
    return (c1 + c2 * a / T) * np.exp(c3 * a**2 + c4 / T + c5 * a / (T**2))

def p(a, K_2, T):
    return ((K_H(T, a) * a**2) / (K_2 * (1 - 2 * a)**2))/100 #dele på 100 for å gjør om til bar

# Konstanter og verdier
temperaturer = np.array([273, 298, 313, 333, 353, 373, 393, 423])
likevektskonstanter_2 = np.array([3.93e5, 3.70e4, 1.14e4, 2.43e3, 5.78e2, 2.46e2, 4.08e1, 6.74])
alfa_verdier = np.linspace(0, 1, 8)  # 8 verdier, samme som temperaturer
colors = ['blue', 'red', 'green', 'orange', 'purple', 'brown', 'pink', 'gray']

plt.figure(figsize=(10, 8))  # Større figur for bedre lesbarhet

for idx, a in enumerate(alfa_verdier):  
    p_values = [p(a, likevektskonstanter_2[i], temperaturer[i]) for i in range(len(temperaturer))]  
    
    plt.scatter(temperaturer, p_values, color=colors[idx], label=f"a = {a:.2f}")
    plt.plot(temperaturer, p_values, color=colors[idx])

plt.title(r"$p(CO_2)$ som funksjon av Temperatur for gitt $\alpha$")
plt.xlabel("Temperatur [K]")
plt.ylabel(r"$p(CO_2)$ [bar]")
plt.legend()
plt.grid(True)
file_path = os.path.join(os.getcwd(), "p(T)_da=0.png")
plt.savefig(file_path, bbox_inches="tight")
print(f"Fil lagret på: {file_path}")
plt.show()

for idx, temp in enumerate(temperaturer):
    p_values = [p(alfa_verdier[i], likevektskonstanter_2[idx], temp) for i in range(len(alfa_verdier))]
    
    plt.scatter(alfa_verdier, p_values, color=colors[idx], label=f"T = {temp} K")
    plt.plot(alfa_verdier, p_values, color=colors[idx])

plt.title(r"$p(CO_2)$ som funksjon av $\alpha$ for gitt temperatur")
plt.xlabel(r"$\alpha$")
plt.ylabel(r"$p(CO_2)$ [bar]")
plt.legend()
plt.grid(True)
file_path = os.path.join(os.getcwd(), "p(a)_dT=0.png")
plt.savefig(file_path, bbox_inches="tight")
print(f"Fil lagret på: {file_path}")
plt.show()

for idx, a in enumerate(alfa_verdier):  
    forhold = [K_H(temperaturer[i],a)/likevektskonstanter_2[i] for i in range(len(temperaturer))]  
    plt.plot(alfa_verdier, forhold, color=colors[idx], label=f"T={temperaturer[idx]}")
plt.title(r"$\frac{K_H}{K_2}$")
plt.xlabel(r"$\alpha$")
plt.yscale("log")
plt.ylabel(r"$\frac{K_H}{K_2}$")
plt.legend()
plt.tight_layout()  # Hindrer at plott overlapper
file_path = os.path.join(os.getcwd(), "kh_over_k2.png")
plt.savefig(file_path, bbox_inches="tight")
print(f"Fil lagret på: {file_path}")
plt.show()
