import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from collections import Counter
from itertools import combinations
import random
from datetime import datetime, timedelta
import numpy as np

# Configuration de la page
st.set_page_config(page_title="Analyse du Loto 🎰", page_icon="🍀", layout="wide")

# Fonctions utilitaires
@st.cache_data
def charger_donnees():
    df = pd.read_csv('loto.csv', parse_dates=['date_de_tirage'])
    df = df[df['numero_chance'] != -1]
    return df

def obtenir_top_n(compteur, n):
    return [item for item, _ in compteur.most_common(n)]

def analyser_combinaisons(df, n):
    combs = df[['boule_1', 'boule_2', 'boule_3', 'boule_4', 'boule_5']].apply(lambda x: tuple(sorted(x)), axis=1)
    return Counter([comb for draw in combs for comb in combinations(draw, n)])

# Chargement des données
df = charger_donnees()

# Fonction pour créer un graphique de fréquence
def creer_graphique_frequence(donnees, titre):
    fig = px.bar(x=list(donnees.keys()), y=list(donnees.values()),
                 labels={'x': 'Numéro', 'y': 'Fréquence'},
                 title=titre)
    fig.update_layout(showlegend=False)
    return fig

# Titre principal
st.title("🎰 Analyse du Loto")

# Création des onglets
tab1, tab2, tab3, tab4 = st.tabs(["📊 Analyse des Numéros", "🔮 Suggestions de Jeu", "🕰️ Résultats Récents", "📈 Statistiques Avancées"])

with tab1:
    st.header("📊 Analyse des Fréquences des Numéros")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🔢 Numéros Principaux")
        st.write("""
        Cette section présente la fréquence d'apparition de chaque numéro principal dans les tirages du Loto.
        Un graphique à barres montre combien de fois chaque numéro est sorti. 
        Les numéros les plus fréquents pourraient être considérés comme "chauds", 
        tandis que les moins fréquents pourraient être vus comme "froids" ou "dus".
        """)
        tous_numeros = df[['boule_1', 'boule_2', 'boule_3', 'boule_4', 'boule_5']].values.flatten()
        freq_numeros = Counter(tous_numeros)
        st.plotly_chart(creer_graphique_frequence(freq_numeros, "Fréquence des Numéros Principaux"), use_container_width=True)
    
    with col2:
        st.subheader("🍀 Numéros Chance")
        st.write("""
        Cette section montre la fréquence d'apparition de chaque numéro chance.
        Le graphique à barres illustre combien de fois chaque numéro chance est sorti.
        Ces informations peuvent être utiles pour choisir votre numéro chance,
        bien que chaque tirage reste indépendant et aléatoire.
        """)
        freq_bonus = Counter(df['numero_chance'])
        st.plotly_chart(creer_graphique_frequence(freq_bonus, "Fréquence des Numéros Chance"), use_container_width=True)

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🔝 Numéros les Plus Fréquents")
        st.write("""
            Cette section présente les numéros qui sont sortis le plus souvent dans l'histoire du Loto.
            Bien que les tirages passés n'influencent pas les tirages futurs, certains joueurs aiment inclure 
            ces numéros "chanceux" dans leurs grilles.
        """)
        cols = st.columns(5)
        for i, num in enumerate(obtenir_top_n(freq_numeros, 5)):
            cols[i].metric(f"Numéro {i+1}", num, f"{freq_numeros[num]} fois")

    with col2:
        st.subheader("🔝 Numéros Chance les Plus Fréquents")
        st.write("""
            Voici les numéros chance qui sont apparus le plus souvent. 
            Comme pour les numéros principaux, leur fréquence passée ne garantit pas leur apparition future,
            mais ces informations peuvent guider votre choix de numéro chance.
        """)
        cols = st.columns(5)
        for i, num in enumerate(obtenir_top_n(freq_bonus, 5)):
            cols[i].metric(f"Chance {i+1}", num, f"{freq_bonus[num]} fois")

with tab2:
    st.header("🔮 Suggestions de Jeu")
    
    st.write("""
    Bienvenue dans la section des suggestions de jeu ! Ici, vous trouverez différentes approches 
    pour générer des numéros de Loto basées sur diverses stratégies. Rappelez-vous que ces suggestions 
    sont basées sur des analyses statistiques et ne garantissent en aucun cas un gain. Le Loto reste 
    un jeu de hasard, et chaque tirage est indépendant des précédents.
    """)

    st.subheader("🔢 Combinaisons Fréquentes")

    st.write("""
        Analyse des paires, trios, quatuors, et quintets de numéros qui apparaissent le plus souvent ensemble.
        Ces combinaisons peuvent vous aider à choisir vos grilles en tenant compte des tendances historiques.
    """)

    # Setting up dynamic column creation based on the number of top combinations you want to display
    n_top_combi = 4  # Number of top combinations to display
    cols = st.columns(n_top_combi)

    for i in range(2, 5):
        freq_combi = analyser_combinaisons(df, i)
        top_combis = freq_combi.most_common(n_top_combi)

        for idx, (combi, freq) in enumerate(top_combis):
            #  Convert tuple to string for display
            combi_str = ', '.join(map(str, combi))
            # Each column represents one top combination for the given number grouping
            cols[idx].metric(f"Top {idx + 1} des combinaisons de {i} numéros", combi_str, f"{freq} fois")

    st.divider()

    st.subheader("🔮 Prédiction basée sur les Tendances Récentes")
    st.write("""
    Cette fonction analyse les tirages récents pour identifier les numéros qui pourraient être "chauds".
    Notez que les tirages passés n'influencent pas les tirages futurs dans un jeu de hasard.
    """)
    periode = st.slider("Choisissez la période d'analyse (en jours):", 30, 365, 90)
    date_limite = df['date_de_tirage'].max() - timedelta(days=periode)
    df_recent = df[df['date_de_tirage'] > date_limite]
    
    freq_recent = Counter(df_recent[['boule_1', 'boule_2', 'boule_3', 'boule_4', 'boule_5']].values.flatten())
    prediction = sorted(obtenir_top_n(freq_recent, 5))
    st.write(f"Basé sur les {periode} derniers jours, les numéros les plus probables sont:")
    st.write(f"🔢 {', '.join(map(str, prediction))}")

    st.divider()
        
    st.subheader("📊 Générateur de Grilles")
    st.write("""
    Ci-dessous, vous pouvez générer des grilles de Loto basées sur différentes stratégies. 
    Chaque stratégie utilise une approche unique pour sélectionner les numéros, 
    en se basant sur les données historiques des tirages.
    """)

    def generer_grille(strategie):
        if strategie == "fréquents":
            return sorted(random.sample(obtenir_top_n(freq_numeros, 15), 5))
        elif strategie == "mixte":
            top_moitie = obtenir_top_n(freq_numeros, 25)
            bottom_moitie = [num for num in range(1, 50) if num not in top_moitie]
            return sorted(random.sample(top_moitie, 3) + random.sample(bottom_moitie, 2))
        elif strategie == "combo":
            base = list(random.choice(obtenir_top_n(analyser_combinaisons(df, 3), 10)))
            reste = [num for num in range(1, 50) if num not in base]
            return sorted(base + random.sample(reste, 2))
        elif strategie == "equilibree":
            pairs = random.sample([num for num in range(1, 50) if num % 2 == 0], 2)
            impairs = random.sample([num for num in range(1, 50) if num % 2 != 0], 3)
            grille = pairs + impairs
            numeros_chauds = obtenir_top_n(freq_numeros, 10)
            numeros_froids = obtenir_top_n(Counter({k: -v for k, v in freq_numeros.items()}), 10)
            if not any(num in numeros_chauds for num in grille):
                grille[random.randint(0, 4)] = random.choice(numeros_chauds)
            if not any(num in numeros_froids for num in grille):
                grille[random.randint(0, 4)] = random.choice(numeros_froids)
            return sorted(grille)

    if st.button("🎲 Générer des Grilles"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("### 💡 Stratégie des Numéros Fréquents")
            st.write("""
            Cette stratégie sélectionne les numéros parmi les 15 qui sont sortis le plus souvent.
            L'idée est de miser sur les numéros qui ont été "chanceux" par le passé.
            """)
            grille1 = generer_grille("fréquents")
            st.write(f"🔢 Principaux: {', '.join(map(str, grille1))}")
            st.write(f"🍀 Chance: {random.choice(obtenir_top_n(freq_bonus, 3))}")
            
            st.write("### 🔀 Stratégie Mixte")
            st.write("""
            Cette approche combine des numéros fréquents et moins fréquents.
            Elle vise à équilibrer entre les numéros "chauds" et "froids".
            """)
            grille2 = generer_grille("mixte")
            st.write(f"🔢 Principaux: {', '.join(map(str, grille2))}")
            st.write(f"🍀 Chance: {random.choice(obtenir_top_n(freq_bonus, 5))}")
        
        with col2:
            st.write("### 🧩 Stratégie des Combinaisons Fréquentes")
            st.write("""
            Cette stratégie se base sur les combinaisons de 3 numéros qui sont souvent sorties ensemble,
            puis complète la grille avec des numéros aléatoires.
            """)
            grille3 = generer_grille("combo")
            st.write(f"🔢 Principaux: {', '.join(map(str, grille3))}")
            st.write(f"🍀 Chance: {random.randint(1, 10)}")
            
            st.write("### ⚖️ Stratégie Équilibrée")
            st.write("""
            Cette stratégie vise à créer une grille équilibrée en tenant compte de plusieurs facteurs :
            - Un mélange de numéros pairs et impairs
            - Une combinaison de numéros "chauds" (fréquents) et "froids" (moins fréquents)
            - Une distribution sur différentes parties de la grille de Loto
            """)
            grille4 = generer_grille("equilibree")
            st.write(f"🔢 Principaux: {', '.join(map(str, grille4))}")
            st.write(f"🍀 Chance: {random.randint(1, 10)}")

with tab3:
    st.header("🕰️ Résultats Récents")
    
    nombre_resultats = st.slider("Nombre de résultats récents à afficher", 5, 50, 10)
    st.dataframe(df.head(nombre_resultats))

with tab4:
    st.header("📈 Statistiques Avancées")
    
    # Fonction 1: Analyse des écarts
    st.subheader("⏳ Analyse des Écarts")
    st.write("""
    Cette analyse montre combien de tirages s'écoulent en moyenne entre deux apparitions d'un numéro spécifique.
    Un écart long pourrait suggérer qu'un numéro est "dû", mais rappelez-vous que chaque tirage est indépendant.
    """)
    def analyser_ecarts(serie):
        ecarts = []
        dernier_tirage = 0
        for i, tirage in enumerate(serie):
            if tirage:
                ecarts.append(i - dernier_tirage)
                dernier_tirage = i
        return ecarts

    numero_ecart = st.selectbox("Choisissez un numéro pour analyser ses écarts:", range(1, 50), key='ecarts')
    ecarts = analyser_ecarts((df['boule_1'] == numero_ecart) | (df['boule_2'] == numero_ecart) |
                             (df['boule_3'] == numero_ecart) | (df['boule_4'] == numero_ecart) |
                             (df['boule_5'] == numero_ecart))
    
    fig_ecarts = px.histogram(ecarts, nbins=20, labels={'value': 'Écart', 'count': 'Fréquence'},
                              title=f"Distribution des écarts pour le numéro {numero_ecart}")
    st.plotly_chart(fig_ecarts)
    
    # Fonction 2: Analyse de la parité
    st.subheader("🔄 Analyse de la Parité")
    st.write("""
    Cette section examine la distribution des numéros pairs et impairs dans les tirages.
    Un équilibre entre pairs et impairs est souvent recherché par les joueurs.
    """)
    parite = df[['boule_1', 'boule_2', 'boule_3', 'boule_4', 'boule_5']].apply(lambda x: sum(i % 2 for i in x), axis=1)
    fig_parite = px.histogram(parite, nbins=6, labels={'value': 'Nombre de numéros impairs', 'count': 'Fréquence'},
                              title="Distribution de la parité dans les tirages")
    st.plotly_chart(fig_parite)
    
    # Fonction 3: Analyse des sommes
    st.subheader("➕ Analyse des Sommes")
    st.write("""
    Cette analyse montre la distribution de la somme des 5 numéros tirés.
    Certains joueurs croient que certaines plages de sommes sont plus fréquentes que d'autres.
    """)
    sommes = df[['boule_1', 'boule_2', 'boule_3', 'boule_4', 'boule_5']].sum(axis=1)
    fig_sommes = px.histogram(sommes, nbins=30, labels={'value': 'Somme des numéros', 'count': 'Fréquence'},
                              title="Distribution de la somme des numéros dans les tirages")
    st.plotly_chart(fig_sommes)
    
    # Fonction 4: Analyse des séquences
    st.subheader("🔗 Analyse des Séquences")
    st.write("""
    Cette section examine la fréquence des séquences de numéros consécutifs dans les tirages.
    Par exemple, 3-4-5 serait une séquence de 3 numéros consécutifs.
    """)
    def compter_sequences(tirage):
        tirage_trie = sorted(tirage)
        return sum(1 for i in range(len(tirage_trie)-1) if tirage_trie[i+1] - tirage_trie[i] == 1)

    sequences = df[['boule_1', 'boule_2', 'boule_3', 'boule_4', 'boule_5']].apply(compter_sequences, axis=1)
    fig_sequences = px.histogram(sequences, nbins=5, labels={'value': 'Nombre de séquences', 'count': 'Fréquence'},
                                 title="Distribution du nombre de séquences dans les tirages")
    st.plotly_chart(fig_sequences)
    
    # Fonction 5: Analyse des retards
    st.subheader("⏰ Analyse des Retards")
    st.write("""
    Cette analyse montre depuis combien de tirages chaque numéro n'est pas sorti.
    Un long retard pourrait suggérer qu'un numéro est "dû", mais chaque tirage reste indépendant.
    """)
    retards = {i: 0 for i in range(1, 50)}
    for _, row in df.iterrows():
        tirages = set(row[['boule_1', 'boule_2', 'boule_3', 'boule_4', 'boule_5']])
        for num in retards:
            if num in tirages:
                retards[num] = 0
            else:
                retards[num] += 1
    
    fig_retards = px.bar(x=list(retards.keys()), y=list(retards.values()),
                         labels={'x': 'Numéro', 'y': 'Retard'},
                         title="Retard actuel de chaque numéro")
    st.plotly_chart(fig_retards)