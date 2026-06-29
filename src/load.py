import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
WAREHOUSE_DIR = BASE_DIR / "Warehouse"

DB_PATH = WAREHOUSE_DIR / "airbnb_dw.db"


def save_tables(
    dim_property,
    dim_host,
    dim_location,
    dim_date,
    fact_availability
):
    """
    Sauvegarde les tables dans des CSV et dans SQLite.
    """

    print("\n===== Sauvegarde des CSV =====")

    dim_property.to_csv(
        WAREHOUSE_DIR / "dim_property.csv",
        index=False
    )

    dim_host.to_csv(
        WAREHOUSE_DIR / "dim_host.csv",
        index=False
    )

    dim_location.to_csv(
        WAREHOUSE_DIR / "dim_location.csv",
        index=False
    )

    dim_date.to_csv(
        WAREHOUSE_DIR / "dim_date.csv",
        index=False
    )

    fact_availability.to_csv(
        WAREHOUSE_DIR / "fact_availability.csv",
        index=False
    )

    print("✅ CSV sauvegardés")

    print("\n===== Sauvegarde SQLite =====")

    conn = sqlite3.connect(DB_PATH)

    dim_property.to_sql(
        "dim_property",
        conn,
        if_exists="replace",
        index=False
    )

    dim_host.to_sql(
        "dim_host",
        conn,
        if_exists="replace",
        index=False
    )

    dim_location.to_sql(
        "dim_location",
        conn,
        if_exists="replace",
        index=False
    )

    dim_date.to_sql(
        "dim_date",
        conn,
        if_exists="replace",
        index=False
    )

    fact_availability.to_sql(
        "fact_availability",
        conn,
        if_exists="replace",
        index=False
    )

    conn.close()

    print("✅ Base SQLite mise à jour")