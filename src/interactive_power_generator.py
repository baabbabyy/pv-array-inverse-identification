"""Interactive pvlib overlay on a synthetic observed generation series.

Sliders for latitude, longitude, tilt, orientation and capacity update a
clear-sky plane-of-array curve. The overlay is a calibration demo, not an
optimiser: there is no least-squares or Bayesian fit.

Observed series defaults to data/synthetic/sample_site_0.csv so a public
clone runs without proprietary site data.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import pandas as pd
import pvlib
from matplotlib.widgets import Slider

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OBSERVED = REPO_ROOT / "data" / "synthetic" / "sample_site_0.csv"

# Maps pvlib POA irradiance (W/m^2) * capacity into a comparable kWh-like
# scale. This is a display fudge from the original lab demo, not a physical
# inverter model.
DEFAULT_SHRINKAGE = 0.0005


def create_data(
    start: pd.Timestamp,
    n_periods: int,
    latitude: float,
    longitude: float,
    tilt: float,
    orientation: float,
    capacity: float,
    shrinkage_factor: float = DEFAULT_SHRINKAGE,
) -> pd.DataFrame:
    location = pvlib.location.Location(latitude=latitude, longitude=longitude, tz="UTC")
    times = pd.date_range(start=start, periods=n_periods, freq="30min", tz="UTC")
    solar_position = location.get_solarposition(times)
    clearsky = location.get_clearsky(times)
    irradiance = pvlib.irradiance.get_total_irradiance(
        surface_tilt=tilt,
        surface_azimuth=orientation,
        solar_zenith=solar_position["apparent_zenith"],
        solar_azimuth=solar_position["azimuth"],
        dni=clearsky["dni"],
        ghi=clearsky["ghi"],
        dhi=clearsky["dhi"],
    )
    return pd.DataFrame(
        {
            "timestamp_utc": times,
            "irradiance": irradiance["poa_global"].to_numpy() * capacity * shrinkage_factor,
        }
    )


def load_observed(path: Path = DEFAULT_OBSERVED) -> pd.DataFrame:
    df = pd.read_csv(path)
    df["timestamp_utc"] = pd.to_datetime(df["timestamp_utc"], utc=True)
    return df


def run_demo(observed_path: Path = DEFAULT_OBSERVED) -> None:
    observed = load_observed(observed_path)
    init_lat = float(observed["latitude"].iloc[0])
    init_lon = float(observed["longitude"].iloc[0])
    init_tilt = float(observed["pv_array_tilt"].iloc[0])
    init_orientation = float(observed["pv_array_a_orientation"].iloc[0])
    init_capacity = float(observed["pv_dc_kwp"].iloc[0])
    start = observed["timestamp_utc"].iloc[0]
    n_periods = len(observed)

    modelled = create_data(
        start, n_periods, init_lat, init_lon, init_tilt, init_orientation, init_capacity
    )

    fig, ax = plt.subplots(figsize=(10, 6))
    plt.subplots_adjust(left=0.1, bottom=0.5)
    (line_model,) = ax.plot(
        modelled["timestamp_utc"], modelled["irradiance"], label="pvlib clear-sky", alpha=0.6
    )
    ax.plot(
        observed["timestamp_utc"],
        observed["solar_gen_kwh"],
        label="Observed (synthetic sample)",
        alpha=0.7,
    )
    ax.xaxis.set_major_locator(mdates.MonthLocator(bymonthday=1))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
    plt.xticks(rotation=45)
    plt.xlabel("Timestamp UTC")
    plt.ylabel("Generation (display units)")
    plt.legend()

    ax_lat = plt.axes([0.1, 0.3, 0.65, 0.03])
    ax_lon = plt.axes([0.1, 0.25, 0.65, 0.03])
    ax_tilt = plt.axes([0.1, 0.2, 0.65, 0.03])
    ax_ori = plt.axes([0.1, 0.15, 0.65, 0.03])
    ax_cap = plt.axes([0.1, 0.1, 0.65, 0.03])
    ax_shr = plt.axes([0.1, 0.05, 0.65, 0.03])

    slider_lat = Slider(ax_lat, "Latitude", 35, 70, valinit=init_lat)
    slider_lon = Slider(ax_lon, "Longitude", -10, 40, valinit=init_lon)
    slider_tilt = Slider(ax_tilt, "Tilt", 0, 90, valinit=init_tilt)
    slider_ori = Slider(ax_ori, "Orientation", 0, 360, valinit=init_orientation)
    slider_cap = Slider(ax_cap, "Capacity", 0.1, 10, valinit=init_capacity)
    slider_shr = Slider(ax_shr, "Shrinkage", 0.0001, 0.001, valinit=DEFAULT_SHRINKAGE)

    def update(_val: float) -> None:
        updated = create_data(
            start,
            n_periods,
            slider_lat.val,
            slider_lon.val,
            slider_tilt.val,
            slider_ori.val,
            slider_cap.val,
            slider_shr.val,
        )
        line_model.set_ydata(updated["irradiance"])
        fig.canvas.draw_idle()

    for slider in (slider_lat, slider_lon, slider_tilt, slider_ori, slider_cap, slider_shr):
        slider.on_changed(update)

    plt.show()


if __name__ == "__main__":
    run_demo()
