import time
from extract import load_data
from load import save_tables
from transform import (
    create_dim_date,
    create_dim_host,
    create_dim_location,
    create_dim_property,
    create_fact_availability,
    create_fact_reviews,
    link_fact_availability,
)
from utils import check_dimension


def step(label, func, *args):
    """Exécute une étape et affiche son temps d'exécution (diagnostic perf)."""
    t0 = time.time()
    result = func(*args)
    print(f"⏱️  {label} : {time.time() - t0:.2f}s")
    return result


def main():
    start_time = time.time()
    print("🚀 DÉMARRAGE DU PIPELINE ETL\n" + "=" * 30)

    # -------------------------
    # 1. Extraction
    # -------------------------
    listings, calendar, reviews = step("Extraction (load_data)", load_data)

    # -------------------------
    # 2. Dimensions Parentes
    # -------------------------
    dim_host = step("create_dim_host", create_dim_host, listings)
    dim_location = step("create_dim_location", create_dim_location, listings)
    dim_date = step("create_dim_date", create_dim_date, calendar, reviews)

    # -------------------------
    # 3. Dimension Enfant (dépendante de Host et Location)
    # -------------------------
    dim_property = step(
        "create_dim_property", create_dim_property, listings, dim_host, dim_location
    )

    # -------------------------
    # 4. Tables de faits & Liaisons
    # -------------------------
    fact_availability = step(
        "create_fact_availability", create_fact_availability, calendar
    )

    fact_availability = step(
        "link_fact_availability",
        link_fact_availability,
        fact_availability,
        dim_property,
        dim_date,
    )

    fact_reviews = step(
        "create_fact_reviews", create_fact_reviews, reviews, dim_property, dim_date
    )

    # -------------------------
    # 5. Contrôles qualité
    # -------------------------
    print("\n🧪 Exécution des contrôles qualité...")
    check_dimension(dim_property, "property_key", "DIM_PROPERTY")
    check_dimension(dim_host, "host_key", "DIM_HOST")
    check_dimension(dim_location, "location_key", "DIM_LOCATION")
    check_dimension(dim_date, "date_key", "DIM_DATE")
    check_dimension(
        fact_availability,
        "fact_availability_key",
        "FACT_AVAILABILITY",
        foreign_keys=["property_key", "date_key"],
    )
    check_dimension(
        fact_reviews,
        "fact_review_key",
        "FACT_REVIEWS",
        foreign_keys=["property_key", "date_key"],
    )

    # -------------------------
    # 6. Sauvegarde
    # -------------------------
    step(
        "save_tables",
        save_tables,
        dim_property,
        dim_host,
        dim_location,
        dim_date,
        fact_availability,
        fact_reviews,
    )

    execution_time = time.time() - start_time
    print(f"\n========== PIPELINE TERMINÉ EN {execution_time:.2f}s ==========")
    print("Toutes les tables ont été créées, reliées et vérifiées avec succès.")


if __name__ == "__main__":
    main()