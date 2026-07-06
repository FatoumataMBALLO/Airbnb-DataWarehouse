# 🏠 Data Warehouse Airbnb – Pipeline ETL & Tableau de bord Power BI

> Conception d'un **Data Warehouse** à partir de données Airbnb en mettant en œuvre un pipeline **ETL en Python**, une modélisation **en schéma en étoile** et un tableau de bord interactif sous **Power BI**.

---

## 📌 Présentation du projet

Dans le cadre d'un projet de Data Engineering / Business Intelligence, l'objectif était de transformer des données brutes Airbnb en un **entrepôt de données** permettant de produire des indicateurs décisionnels.

Le projet couvre l'ensemble de la chaîne de traitement des données :

- Extraction des données
- Nettoyage et transformation
- Modélisation dimensionnelle
- Chargement dans une base SQLite
- Visualisation dans Power BI

---

## 🎯 Objectifs

- Développer un pipeline ETL en Python
- Construire un Data Warehouse selon un schéma en étoile
- Créer des dimensions et des tables de faits
- Automatiser le chargement dans SQLite
- Concevoir un tableau de bord interactif avec Power BI

---

# 🛠 Technologies utilisées

| Technologie | Utilisation |
|-------------|-------------|
| Python | Pipeline ETL |
| Pandas | Nettoyage et transformation des données |
| SQLite | Base de données |
| Power BI | Visualisation |
| Git | Gestion de versions |
| GitHub | Hébergement du projet |

---

# 📂 Architecture du projet

```
Airbnb-DataWarehouse/

├── Warehouse/
│   ├── airbnb_dw.db
│   ├── dim_property.csv
│   ├── dim_host.csv
│   ├── dim_location.csv
│   ├── dim_date.csv
│   ├── fact_availability.csv
│   └── fact_reviews.csv
│
├── Images/
│
├── src/
│   ├── extract.py
│   ├── transform.py
│   ├── load.py
│   ├── pipeline.py
│   └── utils.py
│
├── README.md
└── .gitignore
```

---

# ⚙️ Pipeline ETL

## 1️⃣ Extraction

Lecture des fichiers sources :

- Listings
- Calendar
- Reviews

---

## 2️⃣ Transformation

Création des dimensions :

- **DIM_PROPERTY**
- **DIM_HOST**
- **DIM_LOCATION**
- **DIM_DATE**

Création des tables de faits :

- **FACT_AVAILABILITY**
- **FACT_REVIEWS**

Traitements réalisés :

- nettoyage des données
- conversion des dates
- suppression des doublons
- création des clés techniques
- modélisation dimensionnelle

---

## 3️⃣ Chargement

Les données transformées sont automatiquement enregistrées :

- en fichiers CSV
- dans une base SQLite

---

# ⭐ Modèle de données

Le Data Warehouse repose sur un **schéma en étoile**.

```
                    DIM_HOST
                       │
                       │
DIM_LOCATION ─ DIM_PROPERTY ─ FACT_AVAILABILITY
                       │
                       │
                  FACT_REVIEWS
                       │
                    DIM_DATE
```

---

# 📊 Tableau de bord Power BI

Le rapport Power BI permet d'analyser :

- 📌 le nombre total de logements
- 🏘️ la répartition des logements par quartier
- 📅 les disponibilités des logements
- ⭐ les avis déposés
- 📈 l'évolution des données dans le temps
- 🎛️ des filtres interactifs (quartier, type de logement…)

---

# 📸 Aperçu du tableau de bord

## Vue d'ensemble

*(Ajouter une capture d'écran)*

---

## Analyse par quartier

*(Ajouter une capture d'écran)*

---

## Disponibilités

*(Ajouter une capture d'écran)*

---

# 💼 Compétences mises en œuvre

### Data Engineering

- Développement d'un pipeline ETL
- Nettoyage et transformation des données
- Modélisation dimensionnelle
- Création d'un Data Warehouse
- Gestion des clés techniques

### Analyse de données

- Manipulation de données avec Pandas
- Contrôle qualité
- Structuration des données

### Business Intelligence

- Création d'un tableau de bord Power BI
- Conception de KPI
- Visualisations interactives

### Développement

- Python
- Git
- GitHub
- SQLite

---

# ▶️ Exécution du projet

### Cloner le dépôt

```bash
git clone https://github.com/VOTRE-PSEUDO/Airbnb-DataWarehouse.git
```

### Installer les dépendances

```bash
pip install pandas
```

### Lancer le pipeline

```bash
cd src
python pipeline.py
```

---

# 🚀 Améliorations possibles

- Chargement incrémental des données
- Migration vers PostgreSQL
- Orchestration avec Apache Airflow
- Conteneurisation avec Docker
- Déploiement sur le Cloud

---

# 👩‍💻 À propos

**Fatoumata Ballo**

Passionnée par la Data, je développe des projets autour de l'analyse de données, des pipelines ETL et de la Business Intelligence afin de transformer des données brutes en informations exploitables pour la prise de décision.

## Compétences

- Python
- SQL
- Pandas
- Power BI
- SQLite
- Data Warehouse
- ETL
- Git & GitHub

📧 Email : *à compléter*

💼 LinkedIn : *à compléter*

🌐 GitHub : *à compléter*