import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
WAREHOUSE_DIR = BASE_DIR / "Warehouse"


def load_data():

    print("Lecture de listings...")
    listings = pd.read_csv(
        WAREHOUSE_DIR / "listings_clean.csv",
        engine="python"
    )
    print(f"✅ Listings : {listings.shape}")

    print("Lecture de calendar...")
    calendar = pd.read_csv(
        WAREHOUSE_DIR / "calendar_clean.csv",
        low_memory=False
    )
    print(f"✅ Calendar : {calendar.shape}")

    return listings, calendar