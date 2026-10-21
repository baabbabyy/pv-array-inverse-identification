# Synthetic data

`sample_site_0.csv` is a one-year, 30-minute clear-sky panel from the pvlib forward model.

Regenerate a larger training panel (gitignored):

```bash
python src/generate_synthetic.py --n-sites 100 --seed 42
```

Output: `data/synthetic/generated/sample_data_site_{i}.csv`.

`pv_dc_kwp` is a random label and is **not** used when computing irradiance. That is a documented limitation of the original pipeline, not a hidden feature.
