import matplotlib.pyplot as plt
from scipy.stats import norm
import tkinter as tk
from py_vollib.black_scholes_merton.greeks.analytical import gamma, delta, vega, theta, rho
import numpy as np


#interface
interface = tk.Tk()
interface.geometry("650x650")
interface.title("Pricing Option")

#Choix entre le calcul d'un put ou d'un call
choix = 0
def call():
    global choix
    choix = 0
    boutoncalc["text"] = "Calculer le prix du Call"
def put():
    global choix
    choix = 1
    boutoncalc["text"] = "Calculer le prix du Put"

#Mise en forme de l'interface
frame = tk.Frame(interface)

boutonc = tk.Button(frame, text="Call", font=(20), command=call)
boutonc.grid(row=0, column=0, padx="30")
boutonp = tk.Button(frame, text="Put", font=(20),command=put)
boutonp.grid(row=0, column=1)

frame.pack(expand="YES", pady="40")

frame2 = tk.Frame(interface)

#Titres des entrées
labels_f2 = [
    "Volatilité (ex. 0.2):",
    "Spot :",
    "Taux d'intérêt (ex. 0.05):",
    "Strike :",
    "Maturité :",
    "Dividendes (yield ex. 0.07)) :"
]
for i, text in enumerate(labels_f2):
    label = tk.Label(frame2, text=text)
    label.grid(row=i, column=0, pady="5")

#Entrer les différents pararmètres de BS
entry_names = ["vol_entr", "s0_entr", "r_entr", "k_entr", "t_entr", "div_entr"]
entries = {}

for i, name in enumerate(entry_names):
    entry = tk.Entry(frame2)
    entry.grid(row=i, column=1)
    entries[name] = entry

frame2.pack(expand="YES", pady="40")


#Calcul du prix avec la formule BS et les greeks
def calc():
    global choix
    try:
        vol, s0, r, k, t, div = map(float, [entries["vol_entr"].get(), entries["s0_entr"].get(), entries["r_entr"].get(), entries["k_entr"].get(), entries["t_entr"].get(), entries["div_entr"].get()])
        d1 = (np.log(s0/k)+(r+(vol**2)/2)*t)/(vol*np.sqrt(t))
        d2 = d1 - vol*np.sqrt(t)

        option_type = "c" if choix == 0 else "p"
        if choix == 0:  # Call
            prix = s0 * np.exp(-div * t) * norm.cdf(d1) - k * np.exp(-r * t) * norm.cdf(d2)
        else:  # Put
            prix = k * np.exp(-r * t) * norm.cdf(-d2) - s0 * np.exp(-div * t) * norm.cdf(-d1)

        update_result(prix, delta(option_type, s0, k, t, r, vol, div), 
                      gamma(option_type, s0, k, t, r, vol, div), vega(option_type, s0, k, t, r, vol, div),
                      theta(option_type, s0, k, t, r, vol, div), rho(option_type, s0, k, t, r, vol, div))
            
    except ValueError:
        display_error("Veuillez entrer des données valides")

def update_result(prix, delta_value, gamma_value, vega_value, theta_value, rho_value):
    prix, delta_value, gamma_value, vega_value, theta_value, rho_value = map(lambda x: round(x, 4), [prix, delta_value, gamma_value, vega_value, theta_value, rho_value])

    resultats["resultat"]["text"] = f"{prix} €"
    resultats["resultat"]["fg"] = "black"
    resultats["delta_val"]["text"], resultats["gamma_val"]["text"], resultats["vega_val"]["text"], resultats["theta_val"]["text"], resultats["rho_val"]["text"] = delta_value, gamma_value, vega_value, theta_value, rho_value
    for label in ["delta_val", "gamma_val", "vega_val", "theta_val", "rho_val"]:
        resultats[label]["fg"] = "black"

def display_error(message):
    resultats["resultat"]["text"] = message
    resultats["resultat"]["fg"] = "red"
    for label in ["delta_val", "gamma_val", "vega_val", "theta_val", "rho_val"]:
        resultats[label]["text"] = ""

frame3 = tk.Frame(interface, pady=15)

#Affichage du résultat
    #Affichage des titres
labels_f3 = ["Prix :","Delta :","Gamma :","Vega :","Theta :","Rho :"]

for i, text in enumerate(labels_f3):
    label = tk.Label(frame3, text=text, font=(23))
    label.grid(row=i, column=0, pady="3")

    #Affichage des résultats
resultat_f3 = ["resultat", "delta_val", "gamma_val", "vega_val", "theta_val", "rho_val"]
resultats = {}

for i, name in enumerate(resultat_f3):
    res = tk.Label(frame3, text="", font=(23))
    res.grid(row=i, column=1)
    resultats[name]= res

boutoncalc = tk.Button(frame3, text="Calculer", font=(20), command=calc)
boutoncalc.grid(row=6, column=1, pady="10")


def launch_greek_plt(greek_function, greek_name):
    global choix
    try:
        #Recup données
        vol, s0, r, k, t, div = map(float, [entries["vol_entr"].get(), entries["s0_entr"].get(), entries["r_entr"].get(), entries["k_entr"].get(), entries["t_entr"].get(), entries["div_entr"].get()])
        spotprices = np.linspace(0.01*k, 5*k, 1000)

        #Plot
        fig, axe = plt.subplots()
        fig.suptitle(greek_name)
        axe.axvline(x=k, color="red", linestyle="--", label="Strike")
        axe.set_xlim([0.01*k, 2*k])

        #Calcul
        y = [greek_function("c" if choix == 0 else "p", x, k, t, r, vol, div) for x in spotprices]

        #Tracer le graphique
        axe.plot(spotprices, y, label=f"{greek_name} du {'Call' if choix == 0 else 'Put'}")
        axe.legend()
        axe.set_xlabel("Spot price")
        plt.show()

    except ValueError:
        resultats[greek_name.lower()+"_val"]["text"] = "Données invalides"
        resultats[greek_name.lower()+"_val"]["fg"] ="red"


#Boutons pour lancer les courbes
bouton_delta = tk.Button(frame3, text="Courbe Delta/Spot", command=lambda: launch_greek_plt(delta, "Delta"))
bouton_delta.grid(row=1, column=2)
bouton_gamma = tk.Button(frame3, text="Courbe Gamma/Spot", command=lambda: launch_greek_plt(gamma, "Gamma"))
bouton_gamma.grid(row=2, column=2)
bouton_vega = tk.Button(frame3, text="Courbe Vega/Spot", command=lambda: launch_greek_plt(vega, "Vega"))
bouton_vega.grid(row=3, column=2)
bouton_theta = tk.Button(frame3, text="Courbe Theta/Spot", command=lambda: launch_greek_plt(theta, "Theta"))
bouton_theta.grid(row=4, column=2)
bouton_rho = tk.Button(frame3, text="Courbe Rho/Spot", command=lambda: launch_greek_plt(rho, "Rho"))
bouton_rho.grid(row=5, column=2)

frame3.pack(side="top", expand="YES")

tk.mainloop()
