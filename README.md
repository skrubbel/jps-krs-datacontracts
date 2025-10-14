# datacontracts

[TOC]

## Usefull commands

``` bash
# Sort imports
ruff check --select I --fix

# Running the demos in the tools folder (module)
uv run -m tools.demo_load_and_emit
```

``` bash
├── docs
├── examples
├── Pipfile
├── Pipfile.lock
├── pyproject.toml
├── README.md
├── src
│   ├── datacontracts
│   │   ├── contracts
│   │   │   ├── json_schemas
│   │   │   │   └── data-table-contract.schema.json
│   │   │   ├── service_hr_address.yaml
│   │   │   └── service__hr__employee.yaml
│   │   ├── contractslib
│   │   │   ├── emitters
│   │   │   │   ├── databricks_sql_emitter.py
│   │   │   │   ├── __init__.py
│   │   │   │   ├── json_schema_emitter.py
│   │   │   │   ├── markdown_docs_emitter.py
│   │   │   │   ├── spark_structtype_emitter.py
│   │   │   │   ├── templates
│   │   │   │   │   ├── databricks
│   │   │   │   │   │   ├── alter_table.sql.j2
│   │   │   │   │   │   └── create_table.sql.j2
│   │   │   │   │   └── docs
│   │   │   │   │       └── datatable_contract_docs.md.j2
│   │   │   │   └── yaml_emitter.py
│   │   │   ├── __init__.py
│   │   │   ├── loaders
│   │   │   │   ├── __init__.py
│   │   │   │   ├── structtype_loader.py
│   │   │   │   └── yaml_loader.py
│   │   │   ├── models
│   │   │   │   ├── base.py
│   │   │   │   ├── datatable.py
│   │   │   │   ├── __init__.py
│   │   │   │   └── option_types.py
│   │   │   ├── type_converter.py
│   │   │   └── validator.py
│   │   └── __init__.py
│   └── datacontracts.egg-info
│       ├── dependency_links.txt
│       ├── PKG-INFO
│       ├── requires.txt
│       ├── SOURCES.txt
│       └── top_level.txt
```

