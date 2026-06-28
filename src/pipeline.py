from extract import load_data
from transform import (
    create_dim_property,
    create_dim_host,
    create_dim_location
)
from utils import check_dimension


def main():
    # Extraction
    listings, reviews, calendar = load_data()

    # Transformations
    dim_property = create_dim_property(listings)
    dim_host = create_dim_host(listings)
    dim_location = create_dim_location(listings)

    check_dimension(dim_property, "listing_id", "DIM_PROPERTY")
    check_dimension(dim_host, "host_id", "DIM_HOST")
    check_dimension(dim_location, "location_key", "DIM_LOCATION")

if __name__ == "__main__":
    main()