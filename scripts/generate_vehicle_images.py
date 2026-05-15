"""Generate premium Pollinations.ai image URLs for each vehicle in the inventory."""

import csv
import json
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
APP_DIR = Path(__file__).resolve().parent.parent / "app"
CSV_PATH = DATA_DIR / "vehicles.csv"
OUTPUT_PATH = APP_DIR / "vehicle_images.json"


def build_image_url(row):
    year = row["year"]
    make = row["make"]
    model = row["model"]
    color = row["color"]
    condition = row["condition"]

    aesthetic_prompt = (
        f"{year} {make} {model} in {color} "
        f"professional automotive photography studio lighting dramatic angle "
        f"ultra realistic 4K showroom condition detailed reflections sharp focus"
    )
    encoded = aesthetic_prompt.replace(" ", "%20")
    return f"https://image.pollinations.ai/prompt/{encoded}"


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
            "url": build_image_url(v),
            "year": v["year"],
            "make": v["make"],
            "model": v["model"],
            "color": v["color"],
            "vin": v["vin"],
        }

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(images, f, indent=2)

    print(f"Generated {len(images)} image URLs → {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
