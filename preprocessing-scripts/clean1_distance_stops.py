"""
Filters a Digitraffic /trains/<date> JSON file down to only
long-distance passenger trains (trainCategory == "Long-distance")
that were NOT cancelled (cancelled == False), and removes any
timeTableRows entries where the train doesn't actually stop
(trainStopping == False).

Usage:
    python filter_long_distance.py input.json output.json
"""

import json
import sys


def filter_long_distance(input_path: str, output_path: str) -> None:
    with open(input_path, "r", encoding="utf-8") as f:
        trains = json.load(f)

    long_distance_trains = [
        train for train in trains
        if train.get("trainCategory") == "Long-distance"
        and not train.get("cancelled", False)
    ]

    # Remove timeTableRows entries where the train doesn't actually stop.
    # (trainStopping == False rows carry no useful info and are never
    # the first/last row of a train's journey.)
    rows_removed_total = 0
    for train in long_distance_trains:
        original_rows = train.get("timeTableRows", [])
        kept_rows = [
            row for row in original_rows
            if row.get("trainStopping", True)
        ]
        rows_removed_total += len(original_rows) - len(kept_rows)
        train["timeTableRows"] = kept_rows

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(long_distance_trains, f, ensure_ascii=False, indent=2)

    total_long_distance = sum(
        1 for train in trains if train.get("trainCategory") == "Long-distance"
    )
    cancelled_removed = total_long_distance - len(long_distance_trains)

    print(f"Total trains in file:              {len(trains)}")
    print(f"Long-distance trains (all):        {total_long_distance}")
    print(f"  of which cancelled (removed):    {cancelled_removed}")
    print(f"Long-distance trains kept:         {len(long_distance_trains)}")
    print(f"Non-stopping rows removed:         {rows_removed_total}")
    print(f"Written to:                        {output_path}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python filter_long_distance.py <input.json> <output.json>")
        sys.exit(1)

    filter_long_distance(sys.argv[1], sys.argv[2])
