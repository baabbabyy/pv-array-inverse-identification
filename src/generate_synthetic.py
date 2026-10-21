"""Generate synthetic clear-sky PV generation panels with pvlib.

Each site is a year of 30-minute plane-of-array irradiance over a random
European (lat, lon), random tilt and azimuth. Capacity is stored as a
label only; it is not used in the forward irradiance calculation. That
mismatch is intentional documentation of the original lab pipeline.

Start dates are fixed (not wall-clock UTC) so a given seed is reproducible.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timedelta
from pathlib import Path

import numpy as np
import pandas as pd
import pvlib

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUT = REPO_ROOT / "data" / "synthetic" / "generated"
SAMPLE_PATH = REPO_ROOT / "data" / "synthetic" / "sample_site_0.csv"


def generate_sites(
    n: int,
    seed: int = 42,
    start_date: str = "2022-01-01",
) -> list[dict]:
    """Return n site dictionaries with UTC timestamps and POA power."""
    rng = np.random.default_rng(seed)
    base_start = datetime.fromisoformat(start_date)

    sites: list[dict] = []
    for _ in range(n):
        lat = float(rng.uniform(35.0, 70.0))
        lon = float(rng.uniform(-10.0, 40.0))
        # Offset within ~5 years so sites are not perfectly aligned, but
        # still deterministic given seed and start_date.
        site_start = base_start + timedelta(days=int(rng.integers(0, 5 * 365)))
        site_start = site_start.replace(hour=0, minute=0, second=0, microsecond=0)
        tilt = float(rng.uniform(0, 90))
        azimuth = float(rng.uniform(0, 360))

        times = pd.date_range(
            start=site_start,
            end=site_start + timedelta(days=365),
            freq="30min",
            inclusive="left",
            tz="UTC",
        )
        solar_position = pvlib.solarposition.get_solarposition(
            times,
            lat,
            lon,
            altitude=0,
            pressure=101325,
            temperature=12,
        )
        irradiance = pvlib.irradiance.get_total_irradiance(
            surface_tilt=tilt,
            surface_azimuth=azimuth,
            solar_zenith=solar_position["apparent_zenith"],
            solar_azimuth=solar_position["azimuth"],
            dni=1000,
            ghi=800,
            dhi=200,
            albedo=0.3,
        )
        system_loss = 0.15
        power = (irradiance["poa_global"] * (1 - system_loss)).to_numpy()

        sites.append(
            {
                "latitude": round(lat, 4),
                "longitude": round(lon, 4),
                "start_date_utc": site_start.strftime("%Y-%m-%dT%H:%M:%SZ"),
                "tilt": round(tilt, 2),
                "azimuth": round(azimuth, 2),
                "timestamps": times,
                "power": power,
            }
        )
    return sites


def sites_to_frames(sites: list[dict], seed: int = 42) -> list[pd.DataFrame]:
    """Attach site metadata and a random kWp label; convert W/m^2 to kW-like units."""
    rng = np.random.default_rng(seed)
    frames = []
    for i, sample in enumerate(sites):
        df = pd.DataFrame(
            {
                "timestamp_utc": sample["timestamps"],
                "site_id": i,
                "latitude": sample["latitude"],
                "longitude": sample["longitude"],
                "pv_dc_kwp": round(float(rng.uniform(1, 5)), 2),
                "pv_array_tilt": sample["tilt"],
                "pv_array_a_orientation": sample["azimuth"],
                "solar_gen_kwh": np.round(sample["power"] / 1000.0, 5),
            }
        )
        frames.append(df)
    return frames


def write_sites(frames: list[pd.DataFrame], out_dir: Path, also_sample: bool = True) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    for i, df in enumerate(frames):
        path = out_dir / f"sample_data_site_{i}.csv"
        df.to_csv(path, index=False)
    if also_sample and frames:
        SAMPLE_PATH.parent.mkdir(parents=True, exist_ok=True)
        frames[0].to_csv(SAMPLE_PATH, index=False)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--n-sites", type=int, default=1)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--start-date", default="2022-01-01")
    parser.add_argument("--out-dir", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--no-sample", action="store_true")
    args = parser.parse_args()

    sites = generate_sites(args.n_sites, seed=args.seed, start_date=args.start_date)
    frames = sites_to_frames(sites, seed=args.seed)
    write_sites(frames, args.out_dir, also_sample=not args.no_sample)
    print(f"Wrote {len(frames)} site CSV(s) to {args.out_dir}")
    if not args.no_sample:
        print(f"Copied site 0 to {SAMPLE_PATH}")


if __name__ == "__main__":
    main()
