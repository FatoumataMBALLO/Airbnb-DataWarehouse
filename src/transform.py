import pandas as pd


def create_dim_property(listings):
    """
    Crée la dimension des logements (dim_property).
    """

    dim_property = listings[
        [
            "id",
            "name",
            "property_type",
            "room_type",
            "accommodates",
            "bedrooms",
            "beds",
            "neighbourhood_cleansed",
        ]
    ].copy()

    dim_property.rename(columns={"id": "listing_id"}, inplace=True)

    dim_property.insert(
        0,
        "property_key",
        range(1, len(dim_property) + 1)
    )

    print(f"✅ dim_property créée ({len(dim_property)} lignes)")

    return dim_property


# ----------------------------------------------------
# Creation im_host
# ----------------------------------------------------

def create_dim_host(listings):
    """
    Crée la dimension des hôtes (dim_host).
    """

    dim_host = listings[
        [
            "host_id",
            "host_name",
            "host_since",
            "host_is_superhost",
            "host_response_rate",
        ]
    ].drop_duplicates().copy()

    # Conversion de la date
    dim_host["host_since"] = pd.to_datetime(
        dim_host["host_since"],
        errors="coerce"
    )

    # Conversion du taux de réponse
    dim_host["host_response_rate"] = (
        dim_host["host_response_rate"]
        .str.replace("%", "", regex=False)
    )

    dim_host["host_response_rate"] = pd.to_numeric(
        dim_host["host_response_rate"],
        errors="coerce"
    )

    # Création de la clé technique
    dim_host.insert(
        0,
        "host_key",
        range(1, len(dim_host) + 1)
    )

    print(f"✅ dim_host créée ({len(dim_host)} lignes)")

    return dim_host

    
# ----------------------------------------------------
# Création dim_location
# ----------------------------------------------------

def create_dim_location(listings):
    """
    Crée la dimension des localisations.
    """

    dim_location = listings[
        [
            "neighbourhood_cleansed",
            "latitude",
            "longitude",
        ]
    ].drop_duplicates().copy()

    # Création de la clé technique
    dim_location.insert(
        0,
        "location_key",
        range(1, len(dim_location) + 1)
    )

    print(f"✅ dim_location créée ({len(dim_location)} lignes)")

    return dim_location
    # ----------------------------------------------------
# Création fact_availability
# ----------------------------------------------------

def create_fact_availability(calendar):
    """
    Crée la table de faits des disponibilités.
    """

    fact_availability = calendar[
        [
            "listing_id",
            "date",
            "available",
            "price"
        ]
    ].copy()

    # Conversion de la date
    fact_availability["date"] = pd.to_datetime(
        fact_availability["date"],
        errors="coerce"
    )

    # Nettoyage du prix
    fact_availability["price"] = (
        fact_availability["price"]
        .astype(str)
        .str.replace("$", "", regex=False)
        .str.replace(",", "", regex=False)
    )

    fact_availability["price"] = pd.to_numeric(
        fact_availability["price"],
        errors="coerce"
    )

    # Conversion disponibilité
    fact_availability["available"] = (
        fact_availability["available"]
        .map({"t": 1, "f": 0})
    )

    # Clé technique
    fact_availability.insert(
        0,
        "fact_availability_key",
        range(1, len(fact_availability) + 1)
    )

    print(f"✅ fact_availability créée ({len(fact_availability)} lignes)")

    return fact_availability

    # ----------------------------------------------------
# Création dim_date
# ----------------------------------------------------

def create_dim_date(calendar):
    """
    Crée la dimension des dates.
    """

    dim_date = pd.DataFrame()

    dim_date["date"] = pd.to_datetime(
        calendar["date"],
        errors="coerce"
    )

    dim_date = dim_date.drop_duplicates()

    dim_date["year"] = dim_date["date"].dt.year
    dim_date["month"] = dim_date["date"].dt.month
    dim_date["month_name"] = dim_date["date"].dt.month_name()
    dim_date["quarter"] = dim_date["date"].dt.quarter
    dim_date["week"] = dim_date["date"].dt.isocalendar().week
    dim_date["day"] = dim_date["date"].dt.day
    dim_date["day_name"] = dim_date["date"].dt.day_name()

    dim_date.insert(
        0,
        "date_key",
        range(1, len(dim_date) + 1)
    )

    print(f"✅ dim_date créée ({len(dim_date)} lignes)")

    return dim_date
    # ----------------------------------------------------
# Liaison Fact ↔ Dimensions
# ----------------------------------------------------

def link_fact_availability(
    fact_availability,
    dim_property,
    dim_date
):
    """
    Remplace les identifiants métier par les clés techniques.
    """

    # ---------- Jointure Property ----------
    fact_availability = fact_availability.merge(
        dim_property[["property_key", "listing_id"]],
        on="listing_id",
        how="left"
    )

    # ---------- Jointure Date ----------
    fact_availability = fact_availability.merge(
        dim_date[["date_key", "date"]],
        on="date",
        how="left"
    )

    # ---------- Suppression des clés métier ----------
    fact_availability.drop(
        columns=[
            "listing_id",
            "date"
        ],
        inplace=True
    )

    print("✅ Fact_availability reliée aux dimensions")

    return fact_availability

    # ----------------------------------------------------
# Liaison fact_availability ↔ dimensions
# ----------------------------------------------------

def link_fact_availability(
    fact_availability,
    dim_property,
    dim_date
):
    """
    Remplace les identifiants métier par les clés techniques.
    """

    # Jointure avec dim_property
    fact_availability = fact_availability.merge(
        dim_property[
            [
                "listing_id",
                "property_key"
            ]
        ],
        on="listing_id",
        how="left"
    )

    # Jointure avec dim_date
    fact_availability = fact_availability.merge(
        dim_date[
            [
                "date",
                "date_key"
            ]
        ],
        on="date",
        how="left"
    )

    # On garde uniquement les clés techniques
    fact_availability = fact_availability[
        [
            "fact_availability_key",
            "property_key",
            "date_key",
            "available",
            "price"
        ]
    ]

    print("✅ Liaison avec les dimensions effectuée")

    return fact_availability

    from pathlib import Path


def create_fact_reviews():

    """
    Création de fact_reviews en lecture par morceaux.
    """

    BASE_DIR = Path(__file__).resolve().parent.parent
    WAREHOUSE_DIR = BASE_DIR / "Warehouse"

    chunks = []

    print("Lecture des reviews par morceaux...")

    for chunk in pd.read_csv(
        WAREHOUSE_DIR / "reviews_clean.csv",
        chunksize=100000,
        low_memory=False
    ):

        fact = chunk[
            [
                "listing_id",
                "id",
                "date"
            ]
        ].copy()

        fact.rename(
            columns={
                "id": "review_id",
                "date": "review_date"
            },
            inplace=True
        )

        fact["review_date"] = pd.to_datetime(
            fact["review_date"],
            errors="coerce"
        )

        chunks.append(fact)

        print(f"   {len(chunks)} chunk(s) traité(s)...")

    fact_reviews = pd.concat(
        chunks,
        ignore_index=True
     )

    fact_reviews.insert(
        0,
        "fact_review_key",
        range(1, len(fact_reviews)+1)
    )

    print(f"✅ fact_reviews créée ({len(fact_reviews)} lignes)")

    return fact_reviews