
import pandas as pd

# Load the uploaded property dataset
df = pd.read_csv("C:\\Users\\jaswa\\OneDrive\\Desktop\\ROADMAP\\DAY2\\properties.csv")
print("DATASET SHAPE")
print(df.shape)

print("\nCOLUMN NAMES")
print(df.columns.tolist())

print("\nDATA TYPES")
print(df.dtypes)

print("\nMISSING VALUES")
print(df.isnull().sum())

print("\nMISSING PERCENTAGES")
print((df.isnull().mean() * 100).round(2))

# Ignore the exported index when finding duplicates
data_columns = [
    col for col in df.columns
    if not col.startswith("Unnamed:")
]

print("\nREPEATED RECORDS")
print(df.duplicated(subset=data_columns).sum())

print("\nPROPERTY TYPES")
print(df["typeOfProperty"].value_counts())

print("\nPRICING CATEGORIES")
print(df["pricing"].value_counts().head(15))

# Identify listings containing numerical prices
has_price = df["pricing"].str.contains(
    "$", regex=False, na=False
)

print("\nLISTINGS WITH A DOLLAR PRICE")
print(has_price.sum())

print("\nNUMERICAL SUMMARY")
print(df[[
    "noOfBedrooms",
    "noOfBathrooms"
]].describe())

