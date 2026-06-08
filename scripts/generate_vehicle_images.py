"""Generate local image paths for each vehicle in the inventory.

Images live in app/static/images/vehicle_{id}.webp.
This script creates the vehicle_images.json mapping each vehicle ID to its local path.
"""

import csv
import json
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
APP_DIR = Path(__file__).resolve().parent.parent / "app"
CSV_PATH = DATA_DIR / "vehicles.csv"
OUTPUT_PATH = APP_DIR / "vehicle_images.json"


def main():
    if not CSV_PATH.exists():
        print(f"Error: {CSV_PATH} not found.")
        return

    with open(CSV_PATH, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        vehicles = list(reader)

    images = {}
    for v in vehicles:
        vid = v["vehicle_id"]
        images[vid] = {
            "url": f"/images/vehicle_{vid}.webp",
            "year": v["year"],
            "make": v["make"],
            "model": v["model"],
            "color": v["color"],
            "vin": v["vin"],
        }

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(images, f, indent=2)

    print(f"Generated {len(images)} local image paths → {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
