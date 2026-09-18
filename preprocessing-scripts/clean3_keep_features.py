"""
Takes the collapsed train JSON files (with "numStops", "origin", and
"destination" fields, e.g. from filtered-data2/) and strips out all
fields that carry no useful information for the project, keeping only:

  Train-level:
    - trainNumber
    - departureDate
    - trainType
    - numStops

  origin (kept fields only):
    - stationShortCode
    - scheduledTime
    - differenceInMinutes

  destination (kept fields only):
    - stationShortCode
    - scheduledTime
    - differenceInMinutes   <- this is your prediction target/label

Usage:
    python clean_fields.py input.json output.json
"""

import json
import sys

ORIGIN_DEST_FIELDS_TO_KEEP = [
    "stationShortCode",
    "scheduledTime",
    "differenceInMinutes",
]


def clean_train(train: dict) -> dict:
    origin = train.get("origin", {})
    destination = train.get("destination", {})

    return {
        "trainNumber": train.get("trainNumber"),
        "departureDate": train.get("departureDate"),
        "trainType": train.get("trainType"),
        "numStops": train.get("numStops"),
        "origin": {k: origin.get(k) for k in ORIGIN_DEST_FIELDS_TO_KEEP},
        "destination": {k: destination.get(k) for k in ORIGIN_DEST_FIELDS_TO_KEEP},
    }


def clean_fields(input_path: str, output_path: str) -> None:
    with open(input_path, "r", encoding="utf-8") as f:
        trains = json.load(f)

    cleaned = [clean_train(train) for train in trains]

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(cleaned, f, ensure_ascii=False, indent=2)

    print(f"Trains cleaned:  {len(cleaned)}")
    print(f"Written to:      {output_path}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python clean_fields.py <input.json> <output.json>")
        sys.exit(1)

    clean_fields(sys.argv[1], sys.argv[2])
