
from pathlib import Path
import re
import pandas as pd

INPUT = Path("properties.csv")
OUTPUT = Path("data/processed/properties_cleaned.csv")


def clean_properties(raw):
    df = raw.copy()

    # 1. Rename the exported index
    df = df.rename(
        columns={"Unnamed: 0": "source_row_id"}
    )

    # 2. Standardise text values
    df["location"] = (
        df["location"]
        .astype("string")
        .str.strip()
        .replace("", pd.NA)
    )

    df["dataPosted"] = (
        df["dataPosted"]
        .astype("string")
        .str.replace(r"\s+", " ", regex=True)
        .str.strip()
    )

    for col in ["pricing", "typeOfProperty"]:
        df[col] = df[col].astype("string").str.strip()

    # 3. Convert bedrooms and bathrooms to numeric
    for col in ["noOfBedrooms", "noOfBathrooms"]:
        df[col] = pd.to_numeric(
            df[col], errors="coerce"
        )

    # 4. Standardise land area to square metres
    area = df["landArea"].astype("string").str.strip()

    parts = area.str.extract(
        r"^([\d,]+(?:\.\d+)?)\s*(m2|ha)$",
        flags=re.IGNORECASE
    )

    area_value = pd.to_numeric(
        parts[0].str.replace(",", "", regex=False),
        errors="coerce"
    )

    df["land_area_m2"] = area_value.copy()

    hectares = parts[1].str.lower().eq("ha").fillna(False)

    df.loc[hectares, "land_area_m2"] *= 10000

    # 5. Extract numeric advertised prices
    extracted_price = df["pricing"].str.extract(
        r"\$\s*([\d,]+(?:\.\d+)?)",
        expand=False
    )

    df["advertised_price_nzd"] = pd.to_numeric(
        extracted_price.str.replace(
            ",", "", regex=False
        ),
        errors="coerce"
    )

    # 6. Preserve the type of advertised price
    df["price_method"] = "no_numeric_price"

    df.loc[
        df["advertised_price_nzd"].notna(),
        "price_method"
    ] = "numeric_price_or_guide"

    for phrase, category in [
        ("Enquiries Over", "enquiries_over"),
        ("Offers Over", "offers_over"),
        ("Asking Price", "asking_price")
    ]:
        mask = df["pricing"].str.contains(
            phrase, case=False, na=False
        )
        df.loc[mask, "price_method"] = category

    # 7. Data quality flags
    df["missing_location"] = df["location"].isna()

    df["missing_land_area"] = (
        df["land_area_m2"].isna()
    )

    df["unusually_many_rooms"] = (
        df["noOfBedrooms"].gt(10)
        | df["noOfBathrooms"].gt(10)
    )

    # 8. Flag possible duplicates, do not delete
    comparison_cols = [
        "location",
        "noOfBedrooms",
        "noOfBathrooms",
        "landArea",
        "dataPosted",
        "typeOfProperty",
        "pricing"
    ]

    df["possible_duplicate"] = df.duplicated(
        subset=comparison_cols,
        keep=False
    )

    return df


if __name__ == "__main__":
    raw = pd.read_csv(INPUT)
    cleaned = clean_properties(raw)

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    cleaned.to_csv(OUTPUT, index=False)

    assert len(raw) == len(cleaned)

    print("Original records:", len(raw))
    print("Processed records:", len(cleaned))

    print(
        "Parsed land areas:",
        cleaned["land_area_m2"].notna().sum()
    )

    print(
        "Numeric advertised prices:",
        cleaned["advertised_price_nzd"].notna().sum()
    )

    print(
        "Possible duplicate rows:",
        cleaned["possible_duplicate"].sum()
    )

    print(
        "Unusually high room counts:",
        cleaned["unusually_many_rooms"].sum()
    )

    print("\nPrice methods:")
    print(cleaned["price_method"].value_counts())

    print("\nSaved to:", OUTPUT)
