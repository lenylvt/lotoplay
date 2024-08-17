# 🎰 Analyse du Loto 🍀

Ce projet utilise Streamlit pour créer une application interactive permettant d'analyser les tirages du Loto. L'application offre plusieurs fonctionnalités pour explorer les fréquences des numéros, générer des grilles basées sur des stratégies, et visualiser des statistiques avancées.

Lien publique : https://lotoplay.streamlit.app/

## Fonctionnalités

### 1. Analyse des Numéros
- **Fréquence des Numéros Principaux :** Affichage des numéros les plus fréquemment tirés.
- **Fréquence des Numéros Chance :** Visualisation de la fréquence d'apparition des numéros chance.
- **Numéros les Plus Fréquents :** Présentation des numéros principaux et des numéros chance les plus fréquents sous forme de métriques.

### 2. Suggestions de Jeu
- **Combinaisons Fréquentes :** Analyse des paires, trios, quatuors, et quintets de numéros qui apparaissent le plus souvent ensemble.
- **Prédiction basée sur les Tendances Récentes :** Identification des numéros les plus probables en fonction des tirages récents.
- **Générateur de Grilles :** Génération de grilles de Loto selon différentes stratégies (numéros fréquents, stratégie mixte, combinaisons fréquentes, stratégie équilibrée).

### 3. Résultats Récents
- Affichage des derniers résultats du Loto avec un slider pour choisir le nombre de résultats à afficher.

### 4. Statistiques Avancées
- **Analyse des Écarts :** Visualisation des écarts moyens entre les apparitions d'un numéro spécifique.
- **Analyse de la Parité :** Étude de la distribution des numéros pairs et impairs dans les tirages.
- **Analyse des Sommes :** Distribution des sommes des 5 numéros tirés.
- **Analyse des Séquences :** Fréquence des séquences de numéros consécutifs dans les tirages.
- **Analyse des Retards :** Temps écoulé depuis la dernière apparition de chaque numéro.

## Installation

1. **Cloner le dépôt :**
   ```bash
   git clone https://github.com/votre_utilisateur/analyse-loto.git
   cd analyse-loto
   ```

2. **Installer les dépendances :**
   ```bash
   pip install -r requirements.txt
   ```

3. **Lancer l'application :**
   ```bash
   streamlit run app.py
   ```

## Fichiers

- `app.py` : Le fichier principal de l'application Streamlit.
- `loto.csv` : Le fichier CSV contenant les résultats des tirages du Loto (à placer dans le même répertoire que `app.py`).
- `README.md` : Ce fichier, décrivant le projet.

## Données

Le fichier `loto.csv` doit contenir les colonnes suivantes :
- `date_de_tirage` : Date du tirage
- `boule_1`, `boule_2`, `boule_3`, `boule_4`, `boule_5` : Les numéros principaux tirés
- `numero_chance` : Le numéro chance tiré

## Remarques

- **Stabilité** : L'application est stable mais toujours en développement. N'hésitez pas à soumettre des issues ou des pull requests pour améliorer le projet.
- **Confidentialité** : Aucune donnée personnelle n'est collectée. L'analyse est entièrement basée sur les résultats publics du Loto.