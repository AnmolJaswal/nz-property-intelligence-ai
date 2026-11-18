
import pandas as pd
from clean_properties import clean_properties


def sample_data():
    return pd.DataFrame({
        "Unnamed: 0": [0, 1, 2, 3],
        "location": [
            "Auckland",
            None,
            "Wellington",
            "Wellington"
        ],
        "noOfBedrooms": [3, None, 12, 12],
        "noOfBathrooms": [2, None, 2, 2],
        "landArea": [
            "500m2",
            "1.5ha",
            None,
            None
        ],
        "dataPosted": [
            "1 day ago",
            "2 days ago",
            "3 days ago",
            "3 days ago"
        ],
        "typeOfProperty": [
            "House",
            "Section",
            "House",
            "House"
        ],
        "pricing": [
            "$699,000",
            "Auction",
            "Offers Over $899,000",
            "Offers Over $899,000"
        ]
    })


def test_record_count_preserved():
    raw = sample_data()
    cleaned = clean_properties(raw)

    assert len(cleaned) == len(raw)


def test_land_area_conversion():
    cleaned = clean_properties(sample_data())

    assert cleaned.loc[0, "land_area_m2"] == 500
    assert cleaned.loc[1, "land_area_m2"] == 15000


def test_missing_values_preserved():
    cleaned = clean_properties(sample_data())

    assert cleaned.loc[1, "missing_location"]
    assert pd.isna(cleaned.loc[2, "land_area_m2"])


def test_price_extraction():
    cleaned = clean_properties(sample_data())

    assert cleaned.loc[0, "advertised_price_nzd"] == 699000
    assert pd.isna(
        cleaned.loc[1, "advertised_price_nzd"]
    )
    assert cleaned.loc[2, "advertised_price_nzd"] == 899000


def test_price_categories():
    cleaned = clean_properties(sample_data())

    assert cleaned.loc[1, "price_method"] == "no_numeric_price"
    assert cleaned.loc[2, "price_method"] == "offers_over"


def test_outlier_flag():
    cleaned = clean_properties(sample_data())

    assert cleaned.loc[2, "unusually_many_rooms"]


def test_duplicate_flag():
    cleaned = clean_properties(sample_data())

    # Records 2 and 3 have the same property fields
    assert cleaned.loc[2, "possible_duplicate"]
    assert cleaned.loc[3, "possible_duplicate"]
