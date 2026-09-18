"""
Takes an already-processed train JSON file (e.g. from filtered-data2/
or final-data/) and removes trains that are not actual passenger
traffic, based on trainType:

  MV  = Kaukoliikenteen tyhjävaunujuna (long-distance empty stock move)
  V   = Henkiloliikenteen tyhjavaunujuna (passenger-service empty stock move)
  MUS = Museojunat (museum trains)

Usage:
    python remove_non_passenger.py input.json output.json
"""

import json
import sys

NON_PASSENGER_TYPES = {"MV", "V", "MUS"}


def remove_non_passenger(input_path: str, output_path: str) -> None:
    with open(input_path, "r", encoding="utf-8") as f:
        trains = json.load(f)

    kept = [
        train for train in trains
        if train.get("trainType") not in NON_PASSENGER_TYPES
    ]

    removed_by_type = {}
    for train in trains:
        t = train.get("trainType")
        if t in NON_PASSENGER_TYPES:
            removed_by_type[t] = removed_by_type.get(t, 0) + 1

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(kept, f, ensure_ascii=False, indent=2)

    print(f"Trains in input file:   {len(trains)}")
    for t in sorted(NON_PASSENGER_TYPES):
        print(f"  removed ({t}):        {removed_by_type.get(t, 0)}")
    print(f"Trains kept:            {len(kept)}")
    print(f"Written to:             {output_path}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python remove_non_passenger.py <input.json> <output.json>")
        sys.exit(1)

    remove_non_passenger(sys.argv[1], sys.argv[2])
