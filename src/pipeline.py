from extract import load_data

from transform import (
    create_dim_property,
    create_dim_host,
    create_dim_location,
    create_dim_date,
    create_fact_availability,
    link_fact_availability
)

from utils import check_dimension
from load import save_tables


def main():

    # -------------------------
    # Extraction
    # -------------------------
    listings, calendar = load_data()

    # -------------------------
    # Dimensions
    # -------------------------
    dim_property = create_dim_property(listings)
    dim_host = create_dim_host(listings)
    dim_location = create_dim_location(listings)
    dim_date = create_dim_date(calendar)

    # -------------------------
    # Table de faits
    # -------------------------
    fact_availability = create_fact_availability(calendar)

    # -------------------------
    # Liaison des clés
    # -------------------------
    fact_availability = link_fact_availability(
        fact_availability,
        dim_property,
        dim_date
    )

    # -------------------------
    # Contrôles qualité
    # -------------------------
    check_dimension(
        dim_property,
        "property_key",
        "DIM_PROPERTY"
    )

    check_dimension(
        dim_host,
        "host_key",
        "DIM_HOST"
    )

    check_dimension(
        dim_location,
        "location_key",
        "DIM_LOCATION"
    )

    check_dimension(
        dim_date,
        "date_key",
        "DIM_DATE"
    )

    check_dimension(
        fact_availability,
        "fact_availability_key",
        "FACT_AVAILABILITY"
    )

    # -------------------------
    # Sauvegarde
    # -------------------------
    save_tables(
        dim_property,
        dim_host,
        dim_location,
        dim_date,
        fact_availability
    )

    print("\n========== PIPELINE TERMINÉ ==========")
    print("Toutes les tables ont été créées avec succès.")


if __name__ == "__main__":
    main()