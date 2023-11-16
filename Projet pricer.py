import matplotlib.pyplot as plt
import math as m
from scipy.stats import norm
import tkinter as tk
from py_vollib.black_scholes_merton.greeks.analytical import gamma, delta, vega, theta, rho
import numpy as np


#interface
interface = tk.Tk()
interface.geometry("650x650")
interface.title("Pricing Option")

#choix entre le calcul d'un put ou d'un call
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

l1 = tk.Label(frame2, text="Volatilité (ex. 0.2):")
l1.grid(row=0, column=0, pady="5")
l2 = tk.Label(frame2, text="Spot :")
l2.grid(row=1, column=0, pady="5")
l3 = tk.Label(frame2, text="Taux d'intérêt (ex. 0.05):")
l3.grid(row=2, column=0, pady="5")
l4 = tk.Label(frame2, text="Strike :")
l4.grid(row=3, column=0, pady="5")
l5 = tk.Label(frame2, text="Maturité :")
l5.grid(row=4, column=0, pady="5")
l7 = tk.Label(frame2, text="Dividendes (yield ex. 0.07)) :")
l7.grid(row=5, column=0, pady="5")

#Entrée des différents paramètres de la formule BS
vol = tk.Entry(frame2)
vol.grid(row=0, column=1)
s0 = tk.Entry(frame2)
s0.grid(row=1, column=1)
r = tk.Entry(frame2)
r.grid(row=2, column=1)
k = tk.Entry(frame2)
k.grid(row=3, column=1)
t = tk.Entry(frame2)
t.grid(row=4, column=1)
div = tk.Entry(frame2)
div.grid(row=5, column=1)

frame2.pack(expand="YES", pady="40")


#Calcul du prix avec la formule BS et les greeks
def calc():
    global choix
    try:
        vol2 = float(vol.get())
        s02 = float(s0.get())
        r2 = float(r.get())
        k2 = float(k.get())
        t2 = float(t.get())
        div2 = float(div.get())

        d1 = (m.log(s02/k2)+(r2+vol2**2/2)*t2)/(vol2*m.sqrt(t2))
        d2 = d1 - vol2*m.sqrt(t2)

        if choix == 0:
            prix = s02*m.exp(-div2*t2)*norm.cdf(d1, 0, 1) - k2*m.exp(-r2*t2)*norm.cdf(d2, 0, 1)
            resultat["text"] = f"{round(prix, 3)} €"
            resultat["fg"] = "black"
            delta_val["text"] = round(delta("c", s02, k2, t2, r2, vol2, div2), 4)
            gamma_val["text"] = round(gamma("c", s02, k2, t2, r2, vol2, div2), 4)
            vega_val["text"] = round(vega("c", s02, k2, t2, r2, vol2, div2), 4)
            theta_val["text"] = round(theta("c", s02, k2, t2, r2, vol2, div2), 4)
            rho_val["text"] = round(rho("c", s02, k2, t2, r2, vol2, div2), 4)
            delta_val["fg"] = "black"
            gamma_val["fg"] = "black"
            vega_val["fg"] = "black"
            theta_val["fg"] = "black"
            rho_val["fg"] = "black"
        elif choix == 1:
            prix = k2*m.exp(-r2*t2)*norm.cdf(-d2, 0, 1) - s02*m.exp(-div2*t2)*norm.cdf(-d1, 0, 1)
            resultat["text"] = f"{round(prix, 3)} €"
            resultat["fg"] = "black"
            delta_val["text"] = round(delta("p", s02, k2, t2, r2, vol2, div2), 4)
            gamma_val["text"] = round(gamma("p", s02, k2, t2, r2, vol2, div2), 4)
            vega_val["text"] = round(vega("p", s02, k2, t2, r2, vol2, div2), 4)
            theta_val["text"] = round(theta("p", s02, k2, t2, r2, vol2, div2), 4)
            rho_val["text"] = round(rho("p", s02, k2, t2, r2, vol2, div2), 4)
            delta_val["fg"] = "black"
            gamma_val["fg"] = "black"
            vega_val["fg"] = "black"
            theta_val["fg"] = "black"
            rho_val["fg"] = "black"
            
    except ValueError:
        resultat["text"] = "Veuillez entrer des données valides"
        resultat["fg"] = "red"
        delta_val["text"] = ""
        gamma_val["text"] =""
        vega_val["text"] =""
        theta_val["text"] = ""
        rho_val["text"] = ""

frame3 = tk.Frame(interface, pady=15)

#Affichage du résultat
titre_resultat = tk.Label(frame3, text="Prix :", font=(23))
titre_resultat.grid(row=0, column=0, pady="3")
resultat = tk.Label(frame3, text="", font=(23))
resultat.grid(row=0, column=1)
titre_delta = tk.Label(frame3, text="Delta :", font=(23))
titre_delta.grid(row=1, column=0, pady="3")
delta_val = tk.Label(frame3, text="", font=(23))
delta_val.grid(row=1, column=1)
titre_gamma = tk.Label(frame3, text="Gamma :", font=(23))
titre_gamma.grid(row=2, column=0, pady="3")
gamma_val = tk.Label(frame3, text="", font=(23))
gamma_val.grid(row=2, column=1)
titre_vega = tk.Label(frame3, text="Vega :", font=(23))
titre_vega.grid(row=3, column=0, pady="3")
vega_val = tk.Label(frame3, text="", font=(23))
vega_val.grid(row=3, column=1)
titre_theta = tk.Label(frame3, text="Theta :", font=(23))
titre_theta.grid(row=4, column=0, pady="3")
theta_val = tk.Label(frame3, text="", font=(23))
theta_val.grid(row=4, column=1)
titre_rho = tk.Label(frame3, text="Rho :", font=(23))
titre_rho.grid(row=5, column=0, pady="3")
rho_val = tk.Label(frame3, text="", font=(23))
rho_val.grid(row=5, column=1)

boutoncalc = tk.Button(frame3, text="Calculer", font=(20), command=calc)
boutoncalc.grid(row=6, column=1, pady="10")


#Mise en graphique 
def launch_cd():
    #Création du plot Delta
    try:
        fig, axe = plt.subplots()
        fig.suptitle("Delta")
        vol2 = float(vol.get())
        s02 = float(s0.get())
        r2 = float(r.get())
        k2 = float(k.get())
        t2 = float(t.get())
        div2 = float(div.get())
        spotprices = np.linspace(0.01*k2, 5*k2, 1000)
        axe.axvline(x=k2, color="red", linestyle="--", label="Strike")
        axe.set_xlim([0.01*k2, 2*k2])
        y =[]
        if choix == 0:
            for x in spotprices:
                y.append(delta("c", x, k2, t2, r2, vol2, div2))
            axe.plot(spotprices, y, label="Delta du Call")
        elif choix == 1:
            for x in spotprices:
                y.append(delta("p", x, k2, t2, r2, vol2, div2))
            axe.plot(spotprices, y, label="Delta du Put")    
        axe.legend()    
        axe.set_xlabel("Spot price")
        plt.show()
    except ValueError:
        delta_val["text"] = "Données invalides"
        delta_val["fg"] = "red"


def launch_cg():
    #Création du plot Gamma
    try:
        fig, axe = plt.subplots()
        fig.suptitle("Gamma")
        vol2 = float(vol.get())
        s02 = float(s0.get())
        r2 = float(r.get())
        k2 = float(k.get())
        t2 = float(t.get())
        div2 = float(div.get())
        spotprices = np.linspace(0.01*k2, 5*k2, 1000)
        axe.axvline(x=k2, color="red", linestyle="--", label="Strike")
        axe.set_xlim([0.01*k2, 2*k2])
        y =[]
        if choix == 0:
            for x in spotprices:
                y.append(gamma("c", x, k2, t2, r2, vol2, div2))
            axe.plot(spotprices, y, label="Gamma du Call")
        elif choix == 1:
            for x in spotprices:
                y.append(gamma("p", x, k2, t2, r2, vol2, div2))
            axe.plot(spotprices, y, label="Gamma du Put")    
        axe.legend()    
        axe.set_xlabel("Spot price")
        plt.show()
    except ValueError:
        gamma_val["text"] = "Données invalides"
        gamma_val["fg"] = "red"      

def launch_cv():
    #Création du plot Vega
    try:
        fig, axe = plt.subplots()
        fig.suptitle("Vega")
        vol2 = float(vol.get())
        s02 = float(s0.get())
        r2 = float(r.get())
        k2 = float(k.get())
        t2 = float(t.get())
        div2 = float(div.get())
        spotprices = np.linspace(0.01*k2, 5*k2, 1000)
        axe.axvline(x=k2, color="red", linestyle="--", label="Strike")
        axe.set_xlim([0.01*k2, 2*k2])
        y =[]
        if choix == 0:
            for x in spotprices:
                y.append(vega("c", x, k2, t2, r2, vol2, div2))
            axe.plot(spotprices, y, label="Vega du Call")
        elif choix == 1:
            for x in spotprices:
                y.append(vega("p", x, k2, t2, r2, vol2, div2))
            axe.plot(spotprices, y, label="Vega du Put")    
        axe.legend()    
        axe.set_xlabel("Spot price")
        plt.show()
    except ValueError:
        vega_val["text"] = "Données invalides"
        vega_val["fg"] = "red"

def launch_ct():
    #Création du plot Theta
    try:
        fig, axe = plt.subplots()
        fig.suptitle("Theta")
        vol2 = float(vol.get())
        s02 = float(s0.get())
        r2 = float(r.get())
        k2 = float(k.get())
        t2 = float(t.get())
        div2 = float(div.get())
        spotprices = np.linspace(0.01*k2, 5*k2, 1000)
        axe.axvline(x=k2, color="red", linestyle="--", label="Strike")
        axe.set_xlim([0.01*k2, 2*k2])
        y =[]
        if choix == 0:
            for x in spotprices:
                y.append(theta("c", x, k2, t2, r2, vol2, div2))
            axe.plot(spotprices, y, label="Theta du Call")
        elif choix == 1:
            for x in spotprices:
                y.append(theta("p", x, k2, t2, r2, vol2, div2))
            axe.plot(spotprices, y, label="Theta du Put")    
        axe.legend()    
        axe.set_xlabel("Spot price")
        plt.show()
    except ValueError:
        theta_val["text"] = "Données invalides"
        theta_val["fg"] = "red"

def launch_cr():
    #Création du plot rho
    try:
        fig, axe = plt.subplots()
        fig.suptitle("Rho")
        vol2 = float(vol.get())
        s02 = float(s0.get())
        r2 = float(r.get())
        k2 = float(k.get())
        t2 = float(t.get())
        div2 = float(div.get())
        spotprices = np.linspace(0.01*k2, 5*k2, 1000)
        axe.axvline(x=k2, color="red", linestyle="--", label="Strike")
        axe.set_xlim([0.01*k2, 2*k2])
        y =[]
        if choix == 0:
            for x in spotprices:
                y.append(rho("c", x, k2, t2, r2, vol2, div2))
            axe.plot(spotprices, y, label="Rho du Call")
        elif choix == 1:
            for x in spotprices:
                y.append(rho("p", x, k2, t2, r2, vol2, div2))
            axe.plot(spotprices, y, label="Rho du Put")    
        axe.legend()    
        axe.set_xlabel("Spot price")
        plt.show()
    except ValueError:
        rho_val["text"] = "Données invalides"
        rho_val["fg"] = "red"

#Boutons pour lancer les courbes
bouton_delta = tk.Button(frame3, text="Courbe Delta/Spot", command=launch_cd)
bouton_delta.grid(row=1, column=2)
bouton_gamma = tk.Button(frame3, text="Courbe Gamma/Spot", command=launch_cg)
bouton_gamma.grid(row=2, column=2)
bouton_vega = tk.Button(frame3, text="Courbe Vega/Spot", command=launch_cv)
bouton_vega.grid(row=3, column=2)
bouton_theta = tk.Button(frame3, text="Courbe Theta/Spot", command=launch_ct)
bouton_theta.grid(row=4, column=2)
bouton_rho = tk.Button(frame3, text="Courbe Rho/Spot", command=launch_cr)
bouton_rho.grid(row=5, column=2)

frame3.pack(side="top", expand="YES")


tk.mainloop()

