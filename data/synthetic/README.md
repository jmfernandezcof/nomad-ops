# Asteria synthetic data

This directory contains only generated fictional data for the NOMAD Ops demonstration.

- `source/` is the canonical dataset.
- `exports/` contains derived views for simulated enterprise systems.
- `scenarios/` links the records used by the six approved demonstrations.
- `reports/` contains the validation report and dataset fingerprint.

Regenerate everything from the repository root:

```bash
python3 scripts/generate_synthetic_data.py
```

Do not edit generated JSON files manually. Change the generator and regenerate them.
