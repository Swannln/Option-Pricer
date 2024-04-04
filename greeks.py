import streamlit as st
from py_vollib.black_scholes_merton.greeks.analytical import gamma, delta, vega, theta, rho
from Home import calc, fonctions_greeks
import pandas as pd
import  numpy as np
import plotly.graph_objs as go

#Slider t, r, vol
try:
    st.session_state["entries"]["t"] = st.slider("Maturié", 0.25, 7.00, st.session_state["entries"]["t"], step=0.01)
    st.session_state["entries"]["vol"] = st.slider("Volatilité", 0.01, 0.80, st.session_state["entries"]["vol"], step=0.01)
except Exception as e:
    st.error(f"Erreur lors du calcul : {e}")

calc(st.session_state["entries"])

#Création du Dict pour y mettre toutes les valeurs des greeks en fonction du spot
if "dict_chart" not in st.session_state:
    st.session_state["dict_chart"] = {key: None for key in ["spot", *fonctions_greeks.keys()]}


#On remplit le dict des greeks en fonction de tous les spot qu'on a intégré dans le dict_chart
if st.session_state["result"]["prix"] is None:
    st.error("Veuillez entrer des données valides")
else:
    #On va calculer les greeks pour 1000 spots : allant de 1% du strike à 200% du strike
    st.session_state["dict_chart"]["spot"] = np.linspace(0.01*st.session_state["entries"]["k"], 2*st.session_state["entries"]["k"], 1000)
    
    if st.session_state["option_type"] == "Call":
        flag = "c"
    else:
        flag = "p"

    for greek, func in fonctions_greeks.items():
        st.session_state["dict_chart"][greek] = [func(flag, spot, st.session_state["entries"]["k"], st.session_state["entries"]["t"],st.session_state["entries"]["r"], st.session_state["entries"]["vol"], st.session_state["entries"]["div"]) for spot in st.session_state["dict_chart"]["spot"]]
    
    #Dict converti en dataframe
    chart_df = pd.DataFrame.from_dict(st.session_state["dict_chart"])

    #Plot les greeks, on ajoute une ligne pointillée pour avoir le strike
    for greek in fonctions_greeks.keys():
        fig = go.Figure([go.Scatter(x=chart_df["spot"], y=chart_df[greek])])
        fig.update_layout(title=f"{greek} du {st.session_state["option_type"]}", xaxis_title="Spot")
        fig.add_shape(
            type="line", 
            x0=st.session_state["entries"]["k"], 
            x1=st.session_state["entries"]["k"], 
            y0=min(st.session_state["dict_chart"][greek]), 
            y1=max(st.session_state["dict_chart"][greek]), 
            line=dict(color="Red", width=2, dash="dash")
        )
        fig.add_annotation(
            x=st.session_state["entries"]["k"],
            y=chart_df[greek].min(), 
            text="Strike",
            showarrow=False, #Pas de flèche,
            yshift=-15, #décale le texte vers le bas
            font=dict(size=16, color="Red")
        )
        st.plotly_chart(fig)
