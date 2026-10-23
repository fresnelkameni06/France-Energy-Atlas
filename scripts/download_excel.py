"""Fetch a user-maintained Excel file via HTTPS; does not call RTE APIs."""
import os
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.parse import urlparse

URL = os.environ.get("EXCEL_SOURCE_URL", "").strip()
if not URL or urlparse(URL).scheme != "https":
    raise SystemExit("EXCEL_SOURCE_URL must be a direct HTTPS download URL for your updated XLSX.")
path = Path(__file__).resolve().parents[1] / "data" / "france_energy_2020_2026.xlsx"
path.parent.mkdir(parents=True, exist_ok=True)
request = Request(URL, headers={"User-Agent": "FranceEnergyAtlas/1.0"})
with urlopen(request, timeout=180) as resp, path.open("wb") as file:
    while chunk := resp.read(1024 * 1024):
        file.write(chunk)
if path.stat().st_size < 5000 or path.open("rb").read(2) != b"PK":
    path.unlink(missing_ok=True)
    raise RuntimeError("Downloaded file is not a valid XLSX ZIP container.")
print(f"Excel downloaded: {path} ({path.stat().st_size / 1024 ** 2:.1f} MB)")
