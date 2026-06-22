# GPX → Google Maps

Convert a GPX route file into a Google Maps navigation deep link that opens turn-by-turn navigation on your phone.

## Why

GPS route planners like [Kurviger](https://kurviger.de) export `.gpx` files with hundreds of track points. Google Maps only accepts ~9–10 waypoints in a URL before the app hand-off breaks. This tool samples the route intelligently — keeping start and end, evenly distributing the rest — so the link always works.

Google doesn't offer a public API for live navigation, but a `maps/dir/` deep link opens the native Google Maps app with real turn-by-turn navigation.

## Usage

### Web (no install)

Open `index.html` in any browser:

1. Drop a `.gpx` file onto the page
2. Choose travel mode and max waypoints
3. Click **Generate Google Maps Link**
4. Copy the link or open it directly — on mobile it launches Google Maps navigation

Everything runs in your browser. No files are sent anywhere.

### CLI

```bash
python gpx_to_gmaps_nav.py route.gpx
```

Options:

| Flag | Default | Description |
|---|---|---|
| `--max-waypoints N` | `8` | Max intermediate waypoints (keep ≤ 9 for reliable app hand-off) |
| `--mode` | `driving` | `driving`, `walking`, or `bicycling` |
| `--open` | off | Open the link in the browser immediately |

The generated URL is printed to stdout and also saved to `gmaps_nav_link.txt`.

## How it works

1. **Parse** — reads `trkpt` (track), `rtept` (route), or `wpt` (waypoints) from the GPX, in that priority order.
2. **Reduce** — start and end points are always kept. Intermediate points are evenly sampled down to `--max-waypoints`.
3. **Build URL** — constructs a `https://www.google.com/maps/dir/?api=1&...` deep link with origin, destination, waypoints, and travel mode.
4. **Open** — the link opens Google Maps on any device and starts navigation immediately.

## Files

```
index.html            # Web interface (self-contained, no dependencies)
gpx_to_gmaps_nav.py   # Python CLI version
route.gpx             # Example GPX from Kurviger
gmaps_nav_link.txt    # Last generated link (CLI output)
```

## Requirements

**Web:** Any modern browser. No server, no dependencies.

**CLI:** Python 3.6+ (standard library only — no pip installs needed).
