#!/usr/bin/env python3
"""GPX -> Google Maps Navigation-Link.

Google bietet keine öffentliche API für Live-Turn-by-Turn-Navigation.
Dieses Skript erzeugt einen Maps-Deep-Link mit Start/Ziel/Wegpunkten,
der die native Google Maps App (mit echter Navigation) öffnet.

Nutzung:
    python gpx_to_gmaps_nav.py route.gpx --open
"""

import argparse
import sys
import webbrowser
import xml.etree.ElementTree as ET

GPX_NS = {"gpx": "http://www.topografix.com/GPX/1/1"}


def parse_gpx(path):
    tree = ET.parse(path)
    root = tree.getroot()

    # Reihenfolge der Priorität: Track-Punkte > Routen-Punkte (z.B. Kurviger) > Wegpunkte
    for tag in ("trkpt", "rtept", "wpt"):
        points = [
            (float(p.get("lat")), float(p.get("lon")))
            for p in root.findall(f".//gpx:{tag}", GPX_NS)
        ]
        if points:
            return points

    sys.exit("Keine Track-/Routen-/Wegpunkte in GPX gefunden.")


def reduce_points(points, max_waypoints):
    """Start + Ende + gleichmäßig verteilte Zwischenpunkte (Google-Limit beachten)."""
    if len(points) <= max_waypoints + 2:
        return points
    start, end = points[0], points[-1]
    middle = points[1:-1]
    step = len(middle) / max_waypoints
    selected = [middle[int(i * step)] for i in range(max_waypoints)]
    return [start] + selected + [end]


def build_url(points, mode):
    origin = f"{points[0][0]},{points[0][1]}"
    destination = f"{points[-1][0]},{points[-1][1]}"
    waypoints = "|".join(f"{lat},{lon}" for lat, lon in points[1:-1])

    url = (
        "https://www.google.com/maps/dir/?api=1"
        f"&origin={origin}&destination={destination}&travelmode={mode}"
    )
    if waypoints:
        url += f"&waypoints={waypoints}"
    return url


def main():
    parser = argparse.ArgumentParser(description="GPX -> Google Maps Navigation-Link")
    parser.add_argument("gpx_file")
    parser.add_argument(
        "--max-waypoints",
        type=int,
        default=8,
        help="Max. Zwischenpunkte (Google-Limit ~9-10 für zuverlässigen App-Handoff)",
    )
    parser.add_argument(
        "--mode",
        choices=["driving", "walking", "bicycling"],
        default="driving",
    )
    parser.add_argument(
        "--open",
        action="store_true",
        help="Link direkt im Browser/App öffnen",
    )
    args = parser.parse_args()

    points = parse_gpx(args.gpx_file)
    points = reduce_points(points, args.max_waypoints)
    url = build_url(points, args.mode)

    print(url)
    with open("gmaps_nav_link.txt", "w") as f:
        f.write(url)

    if args.open:
        webbrowser.open(url)


if __name__ == "__main__":
    main()
