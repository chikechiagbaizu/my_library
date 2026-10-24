# My Library (`my_library`)

A library management module for **Odoo 19.0**, built while following the *Odoo 14 Development Cookbook* and porting its (outdated) Odoo 14 code to Odoo 19.

> Work in progress. The book targets Odoo 14, so most chapters need changes before they run on 19.0. See [Migration Notes](#migration-notes-odoo-14--190).

## Current Features

- **Books** (`library.book`): book records with list/form views, action, and menus
- **Book categories** (`library.book.category`)
- **Partner extension** (`res.partner`): extends partners for library use (e.g. authors/publishers)
- **Security**: custom user groups (`res_groups.xml`) and model access rules (`ir.model.access.csv`)

### Planned / Next

- [ ] Publishers
- [ ] Search view, filters, and group-by
- [ ] Demo data
- [ ] Tests
- [ ] Reports

## Tech Stack

| Component | Version |
|-----------|---------|
| Odoo | 19.0 (official Docker image) |
| PostgreSQL | 16 |
| Docker Compose | v2 |

## Module Structure

```
my_library/
├── README.md
├── __init__.py
├── __manifest__.py
├── models/
│   ├── __init__.py
│   ├── library_book.py
│   ├── library_book_category.py
│   └── res_partner.py
├── security/
│   ├── ir.model.access.csv
│   └── res_groups.xml
├── static/
│   └── description/
│       ├── icon.png
│       └── index.html
└── views/
    ├── library_book_action.xml
    ├── library_book_views.xml
    └── library_menus.xml
```

> Load order in `__manifest__.py` matters: security files first, then actions, then views, then menus (menus reference actions).

## Project Layout (Docker)

The module lives inside a larger lab folder:

```
odoo-lab/
├── docker-compose.yml
├── config/
│   └── odoo.conf
└── custom_addons/
    └── my_library/
```

### Example `docker-compose.yml`

```yaml
services:
  db:
    image: postgres:16
    environment:
      POSTGRES_DB: postgres
      POSTGRES_USER: odoo
      POSTGRES_PASSWORD: odoo
    volumes:
      - db-data:/var/lib/postgresql/data

  odoo:
    image: odoo:19.0
    depends_on:
      - db
    ports:
      - "8069:8069"
    environment:
      HOST: db
      USER: odoo
      PASSWORD: odoo
    volumes:
      - odoo-data:/var/lib/odoo
      - ./config:/etc/odoo
      - ./custom_addons:/mnt/extra-addons

volumes:
  db-data:
  odoo-data:
```

### Example `config/odoo.conf`

```ini
[options]
addons_path = /mnt/extra-addons,/usr/lib/python3/dist-packages/odoo/addons
admin_passwd = change_me
db_host = db
db_user = odoo
db_password = odoo
```

## Getting Started

```bash
# From the odoo-lab/ folder
docker compose up -d
docker compose logs -f odoo
```

Open <http://localhost:8069>, create a database, and enable **Developer Mode** (Settings → Activate the developer mode).

## Installing / Updating the Module

From the UI: **Apps → Update Apps List → search "My Library" → Install**.

From the CLI:

```bash
# Install
docker compose run --rm odoo odoo -d <db_name> -i my_library --stop-after-init

# Update after changing Python/XML
docker compose run --rm odoo odoo -d <db_name> -u my_library --stop-after-init

# Restart to reload Python changes
docker compose restart odoo
```

Dev mode with auto-reload:

```bash
docker compose run --rm --service-ports odoo odoo -d <db_name> --dev=all
```

### Running Tests

```bash
docker compose run --rm odoo odoo -d <test_db> -i my_library --test-enable --test-tags /my_library --stop-after-init
```

## Useful Commands

```bash
# Odoo shell
docker compose run --rm odoo odoo shell -d <db_name>

# psql shell
docker compose exec db psql -U odoo -d <db_name>

# Reset everything (⚠ deletes databases and filestore)
docker compose down -v
```

## Migration Notes (Odoo 14 → 19.0)

Changes encountered while porting cookbook code. Verify against the [Odoo 19 docs](https://www.odoo.com/documentation/19.0/) and source, as APIs keep moving.

### Python

| Odoo 14 (cookbook) | Odoo 19 |
|---|---|
| `@api.multi` | Removed; delete the decorator |
| `@api.model def create(self, vals)` | `@api.model_create_multi` with `vals_list` |
| `name_get()` | Override `_compute_display_name()` |
| `name_search()` / `_name_search()` | `_search_display_name()` / `_rec_names_search` |
| `_sql_constraints = [...]` | `models.Constraint(...)` class attributes |
| `check_access_rights()` + `check_access_rule()` | `check_access()` |
| `read_group()` | `_read_group()` / `formatted_read_group()` |
| Raw SQL strings in `cr.execute` | `odoo.tools.SQL` objects |

### XML views

| Odoo 14 | Odoo 19 |
|---|---|
| `<tree>` | `<list>` |
| `view_mode="tree,form"` | `view_mode="list,form"` |
| `attrs="{'invisible': [('state','=','draft')]}"` | `invisible="state == 'draft'"` |
| `attrs` for `readonly` / `required` | `readonly="..."` / `required="..."` Python-style expressions |
| `states="draft,done"` | `invisible="state not in ('draft','done')"` |
| `<div class="oe_chatter">...</div>` | `<chatter/>` |
| `<odoo><data>...</data></odoo>` | `<data>` wrapper no longer needed |

### Security

- Group and category definitions changed between 17 and 19 (e.g. `groups_id` / `group_ids` on users and the newer privilege model). Check the current `base` module for exact fields before copying cookbook XML into `res_groups.xml`.
- `ir.model.access.csv` header is unchanged:
  `id,name,model_id:id,group_id:id,perm_read,perm_write,perm_create,perm_unlink`
- Model XML IDs follow `model_<model_name_with_underscores>`, e.g. `model_library_book`.

### Manifest

- Version format: `19.0.1.0.0`
- Set `'license'` (e.g. `LGPL-3`)
- List every data file under `data` / `demo`, in dependency order

### JavaScript / Frontend

- The legacy widget system (`web.Widget`, `odoo.define`) is gone; use **OWL** components and ES modules.
- Cookbook JS chapters need to be rewritten, not patched.

### Controllers

- `type='json'` routes are `type='jsonrpc'` in recent versions.

## Cookbook Progress

## Troubleshooting

- **Module not showing in Apps**: check that `./custom_addons` is mounted at `/mnt/extra-addons`, `addons_path` includes it, then **Update Apps List** (dev mode on) and remove the "Apps" filter.
- **`ParseError` / `Invalid view` on install**: usually a leftover `<tree>`, `attrs=`, or `states=`.
- **Access errors on a model**: add a row to `ir.model.access.csv` and update with `-u my_library`.
- **Python changes not applied**: restart the container or use `--dev=all`.
- **Menu or action not found**: check manifest order (actions before menus).

## References

- [Odoo 19.0 Developer Documentation](https://www.odoo.com/documentation/19.0/developer.html)
- [Odoo 19.0 Source (GitHub)](https://github.com/odoo/odoo/tree/19.0)
- [Odoo Docker image](https://hub.docker.com/_/odoo)
- *Odoo 14 Development Cookbook*, Parth Gajjar & Alexandre Fayolle (Packt)

## License

LGPL-3.0 (match the `license` key in `__manifest__.py`).