"""
Takes JSON files that have already been filtered down to long-distance,
non-cancelled trains (i.e. files in filtered-data/), and for each train:
  1. Removes timeTableRows entries where the train doesn't actually
     stop (trainStopping == False) or where the stop isn't for
     passengers (commercialStop == False).
  2. Counts the number of real, passenger-relevant stops and stores
     it as "numStops".
  3. Collapses the train down to just two rows: "origin" (first real
     stop) and "destination" (last real stop), dropping the rest of
     the timeTableRows list entirely.

This does NOT re-filter by trainCategory or cancelled - it assumes
that was already done (i.e. input files only contain long-distance,
non-cancelled trains already).

Usage:
    python collapse_stops.py input.json output.json
"""

import json
import sys


def is_real_stop(row: dict) -> bool:
    return row.get("trainStopping", True) and row.get("commercialStop", True)


def collapse_stops(input_path: str, output_path: str) -> None:
    with open(input_path, "r", encoding="utf-8") as f:
        trains = json.load(f)

    result = []
    skipped_no_rows = 0

    for train in trains:
        rows = train.get("timeTableRows", [])
        real_stops = [row for row in rows if is_real_stop(row)]

        if len(real_stops) < 2:
            # Not enough real stops to have both an origin and a
            # destination (e.g. malformed or edge-case entry) - skip it.
            skipped_no_rows += 1
            continue

        # Count unique stations among real stops (each station has an
        # ARRIVAL + DEPARTURE row, so count the station set, not rows).
        unique_stations = {row["stationShortCode"] for row in real_stops}
        num_stops = len(unique_stations)

        train["numStops"] = num_stops
        train["origin"] = real_stops[0]
        train["destination"] = real_stops[-1]

        # Drop the full row-by-row schedule - no longer needed.
        del train["timeTableRows"]

        result.append(train)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print(f"Trains in input file:              {len(trains)}")
    print(f"  of which skipped (<2 stops):     {skipped_no_rows}")
    print(f"Trains kept:                       {len(result)}")
    print(f"Written to:                        {output_path}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python collapse_stops.py <input.json> <output.json>")
        sys.exit(1)

    collapse_stops(sys.argv[1], sys.argv[2])
