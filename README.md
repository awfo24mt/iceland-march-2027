# Iceland March 2027 field guide

March 13–18, 2027 · four travellers · two rooms · Reykjavík base.

Planning edition: flights/hotel copied from user-supplied quotes, not independently re-quoted. Daily event times are suggestions. No booking is confirmed.

## Preview and build

Run `python3 build.py` from any directory (using the script's full path when outside the repository). Serve `dist` using any static web server. No build packages required.

Vercel import: Framework **Other**, Root Directory **./**. Checked-in config runs `python3 build.py` and serves `dist`. Importing the repository and verifying the resulting deployment remain separate steps.

`trip.json` is canonical data; `data.js` is its browser copy. `export_guide.py` uses ReportLab to regenerate the baseline PDF, CSV and self-contained offline HTML. Regenerate `data.js` after editing JSON, then rerun the exporter and build.

Browser notes, cost edits and checkboxes stay on that browser/device; export JSON to transfer them. PDF is the baseline; Print/PDF includes browser edits. Offline HTML includes code, photo and geographic outlines. Optional online street tiles and booking links require internet.

## Credits

Leaflet 1.9.4: BSD-2-Clause, https://leafletjs.com (license header retained in JavaScript). Offline outline: Natural Earth, public domain, distributed via https://github.com/datasets/geo-countries. Hotel image © Center Hotels, sourced from the official room page; illustrative room only. Optional tiles © OpenStreetMap contributors.

## Scope

No live fare inventory, 2027 tour departures or passport-specific entry determination. Restaurant-specific ratings/hours remain unresearched. Fare-watch status was not checked or changed.
