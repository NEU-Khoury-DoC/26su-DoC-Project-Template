# `database-files` Folder

When the `db` container is **first created**, every `.sql` file here runs in **alphabetical order**.

## Init files (run automatically)

| File | Purpose |
|------|---------|
| `01_ngo_database.sql` | Creates `ngo_db` (matches `api/.env` `DB_NAME`) |
| `02_zeus_core.sql` | `users`, `household_profiles` + demo seed rows |
| `03_gas_storage_schema.sql` | `gas_storage_daily`, `gas_storage_winters`, `gas_storage_model` (empty daily/winter tables until seeded; model weights inserted here) |
| `04_zeus_persona_features.sql` | `saved_articles`, `snapshots`, `notes` (future UI) |

**Personas in schema:** `household_owner`, `journalist` only.

## After first boot — load gas storage CSV data

Schema alone does not insert AGSI rows. Run once:

```bash
docker compose exec api python scripts/seed_gas_storage.py
```

Sources (seed only, not runtime): `datasets/apsi/agsi_clean.csv`, `datasets/apsi/dataset.csv`.

## Re-run SQL after edits

Changes to these files are **not** applied on restart alone. Recreate the db container:

```bash
docker compose down && docker compose up -d
docker compose exec api python scripts/seed_gas_storage.py
```

The project uses tmpfs for MySQL data, so `docker compose down` is enough locally (no `-v` required).
