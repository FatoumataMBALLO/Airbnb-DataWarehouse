import pandas as pd

# ----------------------------------------------------
# Dimensions
# ----------------------------------------------------


def create_dim_host(listings):
    """Crée la dimension des hôtes (dim_host)."""
    dim_host = listings[
        [
            "host_id",
            "host_name",
            "host_since",
            "host_is_superhost",
            "host_response_rate",
        ]
    ].drop_duplicates()

    dim_host = dim_host.copy()

    # host_since est déjà en datetime (parsé dans extract.py), pas besoin
    # de repasser par pd.to_datetime ici.

    # Nettoyage et conversion du taux de réponse ("95%" -> 95.0)
    dim_host["host_response_rate"] = pd.to_numeric(
        dim_host["host_response_rate"].str.rstrip("%"),
        errors="coerce",
    )

    # Création de la clé technique
    dim_host.insert(0, "host_key", range(1, len(dim_host) + 1))

    print(f"✅ dim_host créée ({len(dim_host)} lignes)")
    return dim_host


def create_dim_location(listings):
    """Crée la dimension des localisations."""
    dim_location = listings[
        ["neighbourhood_cleansed", "latitude", "longitude"]
    ].drop_duplicates(subset=["neighbourhood_cleansed"]).copy()

    # Création de la clé technique
    dim_location.insert(0, "location_key", range(1, len(dim_location) + 1))

    print(f"✅ dim_location créée ({len(dim_location)} lignes)")
    return dim_location


def create_dim_property(listings, dim_host, dim_location):
    """Crée la dimension des logements connectée à Host et Location."""
    dim_property = listings[
        [
            "id",
            "host_id",
            "neighbourhood_cleansed",
            "name",
            "property_type",
            "room_type",
            "accommodates",
            "bedrooms",
            "beds",
        ]
    ].rename(columns={"id": "listing_id"})

    # Ajout de host_key
    dim_property = dim_property.merge(
        dim_host[["host_id", "host_key"]],
        on="host_id",
        how="left",
        validate="many_to_one",
    )

    # Ajout de location_key
    dim_property = dim_property.merge(
        dim_location[["neighbourhood_cleansed", "location_key"]],
        on="neighbourhood_cleansed",
        how="left",
        validate="many_to_one",
    )

    # Suppression des colonnes métiers pour garder le modèle propre
    dim_property = dim_property.drop(
        columns=["host_id", "neighbourhood_cleansed"]
    )

    # Création de la clé technique
    dim_property.insert(0, "property_key", range(1, len(dim_property) + 1))

    print(f"✅ dim_property créée ({len(dim_property)} lignes)")
    return dim_property


def create_dim_date(calendar, reviews):
    """
    Crée la dimension des dates (dim_date) en une plage CONTINUE de jours,
    du plus ancien au plus récent parmi calendar et reviews.
    """
    all_dates = pd.concat(
        [calendar["date"], reviews["date"]], ignore_index=True
    ).dropna()

    date_min = all_dates.min()
    date_max = all_dates.max()

    dim_date = pd.DataFrame(
        {"date": pd.date_range(start=date_min, end=date_max, freq="D")}
    )

    # Extraction des attributs de temps
    dim_date["year"] = dim_date["date"].dt.year
    dim_date["month"] = dim_date["date"].dt.month
    dim_date["month_name"] = dim_date["date"].dt.month_name()
    dim_date["month_year"] = (
        dim_date["month_name"] + " " + dim_date["year"].astype(str)
    )
    dim_date["month_year_sort"] = (
        dim_date["year"] * 100 + dim_date["date"].dt.month
    )
    dim_date["quarter"] = dim_date["date"].dt.quarter
    dim_date["day"] = dim_date["date"].dt.day
    dim_date["day_of_week"] = dim_date["date"].dt.day_name()
    dim_date["is_weekend"] = dim_date["date"].dt.dayofweek >= 5

    _mois_fr = {
        1: "Jan", 2: "Fev", 3: "Mar", 4: "Avr", 5: "Mai", 6: "Juin",
        7: "Juil", 8: "Aou", 9: "Sep", 10: "Oct", 11: "Nov", 12: "Dec",
    }
    dim_date["month_abbr_fr"] = dim_date["date"].dt.month.map(_mois_fr)

    _jours_fr = {
        0: "Lundi", 1: "Mardi", 2: "Mercredi", 3: "Jeudi",
        4: "Vendredi", 5: "Samedi", 6: "Dimanche",
    }
    dim_date["day_of_week_fr"] = dim_date["date"].dt.dayofweek.map(_jours_fr)
    dim_date["day_of_week_sort"] = dim_date["date"].dt.dayofweek + 1

    dim_date.insert(0, "date_key", range(1, len(dim_date) + 1))

    print(
        f"dim_date creee ({len(dim_date)} lignes, continue de "
        f"{date_min.date()} a {date_max.date()})"
    )
    return dim_date


# ----------------------------------------------------
# Tables de faits
# ----------------------------------------------------


def create_fact_availability(calendar):
    """Crée la table de faits brute de disponibilité (avant liaison aux clés)."""
    fact_availability = calendar[["listing_id", "date", "available"]].copy()

    # 't' / 'f' -> 1 / 0 (entier plutôt que booléen : évite les soucis de
    # compatibilité de type booléen rencontrés dans certaines mesures DAX
    # Power BI). Permet d'utiliser directement SUM() côté DAX au lieu
    # d'un CALCULATE avec filtre = TRUE.
    fact_availability["available"] = (
        fact_availability["available"].astype(str).eq("t").astype("int8")
    )

    print(f"✅ fact_availability (brute) créée ({len(fact_availability)} lignes)")
    return fact_availability


def link_fact_availability(fact_availability, dim_property, dim_date):
    """Relie fact_availability à dim_property et dim_date via les clés techniques."""
    fact_availability = fact_availability.merge(
        dim_property[["listing_id", "property_key"]],
        on="listing_id",
        how="left",
        validate="many_to_one",
    )

    fact_availability = fact_availability.merge(
        dim_date[["date", "date_key"]],
        on="date",
        how="left",
        validate="many_to_one",
    )

    fact_availability = fact_availability.drop(columns=["listing_id", "date"])

    fact_availability.insert(
        0, "fact_availability_key", range(1, len(fact_availability) + 1)
    )

    print(f"✅ fact_availability liée ({len(fact_availability)} lignes)")
    return fact_availability


def create_fact_reviews(reviews, dim_property, dim_date):
    """
    Crée et relie fact_reviews en une seule passe (create + link fusionnés,
    comme pour fact_availability, mais ici sans étape intermédiaire car
    reviews est déjà minimal : listing_id, review_id, date).
    """
    fact_reviews = reviews.merge(
        dim_property[["listing_id", "property_key"]],
        on="listing_id",
        how="left",
        validate="many_to_one",
    )

    fact_reviews = fact_reviews.merge(
        dim_date[["date", "date_key"]],
        on="date",
        how="left",
        validate="many_to_one",
    )

    fact_reviews = fact_reviews.drop(columns=["listing_id", "date"])

    fact_reviews.insert(0, "fact_review_key", range(1, len(fact_reviews) + 1))

    print(f"✅ fact_reviews créée et liée ({len(fact_reviews)} lignes)")
    return fact_reviews