import streamlit as st
import numpy as np
from py_vollib.black_scholes_merton.greeks.analytical import gamma, delta, vega, theta, rho
from scipy.stats import norm
import plotly.graph_objs as go

st.set_page_config("Option Pricer", layout="centered")
st.write("## Option Pricer")

col1, col2 = st.columns(2)

# Initialisation du type de l'option, mémorisation dans session_state pour garder l'info même au changement de la page
if "option_type" not in st.session_state or st.session_state["option_type"] == "Call":
    st.session_state["option_type"] = col1.radio("Option Type", ("Call", "Put"), index=0)
else:
    st.session_state["option_type"] = col1.radio("Option Type", ("Call", "Put"), index=1)

# Affichage basé sur la sélection
if st.session_state["option_type"] == "Call":
    col1.write("Calculer le prix d'un Call")
else:
    col1.write("Calculer le prix d'un Put")


# Entrer des différents paramètres de BS
# Labels et variables de stockage (keys) des entrées
param_entries = [
    ("Volatilité (ex. 0.2):","vol"),
    ("Spot :","s0"),
    ("Taux d'intérêt (ex. 0.05):","r"),
    ("Strike :","k"),
    ("Maturité :","t"),
    ("Dividendes (yield ex. 0.07)) :","div")
]

# Initialiser les entrées dans st.session_state si elles n'existent pas déjà
if "entries" not in st.session_state:
    st.session_state["entries"] = {key: None for _, key in param_entries}

# Utiliser les valeurs stockées dans st.session_state pour initialiser les champs d'entrée et les mettre à jour
for label, key in param_entries:
    # Utiliser la valeur actuelle de st.session_state['entries'][key] comme valeur par défaut si elle n'est pas None
    default_value = st.session_state["entries"][key] if st.session_state["entries"][key] is not None else 0.00
    entry = col1.number_input(label, value=default_value)
    st.session_state["entries"][key] = entry


fonctions_greeks = {
    "delta": delta,
    "gamma": gamma,
    "vega": vega,
    "theta": theta,
    "rho": rho
}

# Initialisation du résultat dans sessions_state
if "result" not in st.session_state:
    st.session_state["result"] = {key: None for key in ["prix", *fonctions_greeks.keys()]}

#Calcul du prix de l'option
def calc(entries):
    try:
        vol, s0, r, k, t, div = entries["vol"], entries["s0"], entries["r"], entries["k"], entries["t"], entries["div"]
        if vol<= 0 or s0 <= 0 or k <= 0 or t <= 0:
            st.error("Les paramètres doivent être positifs.")

        d1 = (np.log(s0/k)+(r+(vol**2)/2)*t)/(vol*np.sqrt(t))
        d2 = d1 - vol*np.sqrt(t)

        if st.session_state["option_type"] == "Call":
            flag = "c"
            st.session_state["result"]["prix"] = s0 * np.exp(-div * t) * norm.cdf(d1) - k * np.exp(-r*t) * norm.cdf(d2)
        else:
            flag = "p"
            st.session_state["result"]["prix"] = k * np.exp(-r * t) * norm.cdf(-d2) - s0 * np.exp(-div*t) * norm.cdf(-d1)
        for nom, fonc in fonctions_greeks.items():
            st.session_state["result"][nom] = fonc(flag, s0, k, t, r, vol, div)

    except Exception as e:
        st.error(f"Erreur lors du calcul : {e}")
    
calc(st.session_state["entries"])

def display_price():
    if st.session_state["result"]["prix"] is None:
        st.error("Veuillez entrer des données valides")
    else:
        for key, value in st.session_state["result"].items():
            col2.write(f"Le {key} est {round(value, 3)}{" €" if key == "prix" else ""}")

calc_button = col2.button("Calculate", on_click=display_price)