"""Convert vehicles.csv into natural language inventory documents for the RAG knowledge base."""

import csv
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
KB_DIR = Path(__file__).resolve().parent.parent / "knowledge_base"

def vehicle_to_doc(row):
    status_note = {
        "Available": "is currently available and ready for a test drive",
        "Sold": "has been sold",
        "In Transit": "is in transit and expected soon",
        "In Service": "is in our service center",
        "Reserved": "is currently reserved for another customer",
    }.get(row["status"], f"has status: {row['status']}")

    features = []
    if row["fuel_type"] == "Electric":
        features.append("zero-emission electric vehicle")
    elif row["fuel_type"] == "Hybrid":
        features.append("fuel-efficient hybrid")
    elif row["fuel_type"] == "Plug-in Hybrid":
        features.append("plug-in hybrid with electric range")

    if int(row["doors"]) <= 2:
        features.append("sporty two-door design")
    if int(row["seats"]) >= 7:
        features.append("seats up to " + row["seats"] + " passengers")

    if row["condition"] == "Certified Pre-Owned":
        features.append("certified pre-owned with 150-point inspection")
    elif row["condition"] == "New":
        features.append("brand new with full factory warranty")

    feature_str = f" This {', '.join(features)}." if features else ""

    return f"""## {row['year']} {row['make']} {row['model']}
- **VIN:** {row['vin']}
- **Condition:** {row['condition']}
- **Mileage:** {int(row['mileage']):,} miles
- **Color:** {row['color']}
- **Transmission:** {row['transmission']}
- **Engine:** {row['engine']}
- **Fuel Type:** {row['fuel_type']}
- **Doors:** {row['doors']}
- **Seats:** {row['seats']}
- **Price:** ${float(row['price']):,.0f}
- **MSRP:** ${float(row['msrp']):,.0f}
- **Status:** {row['status']}

{row['year']} {row['make']} {row['model']} in {row['color'].lower()} with a {row['engine']} engine and {row['transmission'].lower()} transmission. It has {int(row['mileage']):,} miles and is priced at ${float(row['price']):,.0f}. This vehicle {status_note}.{feature_str}

---
"""

def main():
    input_path = DATA_DIR / "vehicles.csv"
    output_path = KB_DIR / "07_inventory.md"

    if not input_path.exists():
        print(f"Error: {input_path} not found. Run generate_synthetic_data.py first.")
        return

    with open(input_path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        vehicles = list(reader)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("# T&C AUTOS Vehicle Inventory\n\n")
        f.write(f"This document contains our current inventory of {len(vehicles)} vehicles.\n\n")
        f.write("---\n\n")
        for v in vehicles:
            f.write(vehicle_to_doc(v))

    print(f"Written {len(vehicles)} vehicle entries to {output_path}")

if __name__ == "__main__":
    main()
