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