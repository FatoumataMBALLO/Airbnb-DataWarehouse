from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
WAREHOUSE_DIR = BASE_DIR / "Warehouse"


# ----------------------------------------------------
# Dtypes explicites : évite que pandas devine (lent) et
# réduit fortement l'empreinte mémoire (category, int32...)
# ----------------------------------------------------

LISTINGS_DTYPES = {
    "id": "int64",
    "host_id": "int64",
    "host_name": "object",
    # host_since est parsé en date directement par read_csv (parse_dates)
    "host_is_superhost": "category",
    "host_response_rate": "object",  # contient un "%", converti plus tard
    "neighbourhood_cleansed": "category",
    "latitude": "float32",
    "longitude": "float32",
    "name": "object",
    "property_type": "category",
    "room_type": "category",
    "accommodates": "int16",
    "bedrooms": "float32",
    "beds": "float32",
}

CALENDAR_DTYPES = {
    "listing_id": "int64",
    "available": "category",  # valeurs 't' / 'f'
}

# IMPORTANT : on n'inclut volontairement PAS "comments" ni "reviewer_name".
# reviews_clean.csv fait ~726 Mo à cause du texte des commentaires, alors
# que fact_reviews n'a besoin que de listing_id, id (identifiant de la
# review) et date pour être reliée à dim_property et dim_date.
REVIEWS_DTYPES = {
    "listing_id": "int64",
    "id": "int64",
}


def load_data():

    print("Lecture de listings...")

    listings = pd.read_csv(
        WAREHOUSE_DIR / "listings_clean.csv",
        usecols=list(LISTINGS_DTYPES.keys()) + ["host_since"],
        dtype=LISTINGS_DTYPES,
        parse_dates=["host_since"],
    )

    print(f"✅ Listings : {listings.shape}")

    print("Lecture de calendar...")

    calendar = pd.read_csv(
        WAREHOUSE_DIR / "calendar_clean.csv",
        usecols=list(CALENDAR_DTYPES.keys()) + ["date"],
        dtype=CALENDAR_DTYPES,
        parse_dates=["date"],
    )

    print(f"✅ Calendar : {calendar.shape}")

    print("Lecture de reviews (comments exclu volontairement)...")

    reviews = pd.read_csv(
        WAREHOUSE_DIR / "reviews_clean.csv",
        usecols=list(REVIEWS_DTYPES.keys()) + ["date"],
        dtype=REVIEWS_DTYPES,
        parse_dates=["date"],
    )
    reviews = reviews.rename(columns={"id": "review_id"})

    print(f"✅ Reviews : {reviews.shape}")

    return listings, calendar, reviews