# datacontracts

[TOC]

A library for implementing and validating data contract content.

The libray contains methods to parse/load contracts in yaml format and validate the structure of the contract.

The library also contains functionality to emit Spark StructTypes, Databricks SQL for Creating and altering tables from specifications in the contract and Markdown documentation of the contract content.

Validation of data in Spark data frames is still a work in progress, and will be added at a later stage.

## Usefull pipenv commands

``` bash
# Initial setup - this reads from pyproject.toml
pipenv install -e ".[dev]"

# Running examples
# Uncomment the function you would like to test in demo_load_and_emit.py
pipenv run python src/examples/demo_load_and_emit.py

# Check formatting without changes
pipenv run black --check src/

# Format code
pipenv run black src/

# Sort imports
pipenv run isort src/
```

## Usefull uv and ruff commands

``` bash
# Sort imports
ruff check --select I --fix

# Running the demos in the tools folder (module)
uv run -m src/examples/demo_load_and_emit.py
```

## Project structure

``` bash
.
├── docs
├── examples
│   └── demo_load_and_emit.py
├── Pipfile
├── Pipfile.lock
├── pyproject.toml
├── README.md
└── src
    └── datacontracts
        ├── contracts
        │   ├── json_schemas
        │   │   └── data-table-contract.schema.json
        │   └── yaml
        │       ├── service_hr_address.yaml
        │       └── service__hr__employee.yaml
        ├── contractslib
        │   ├── emitters
        │   │   ├── databricks_sql_emitter.py
        │   │   ├── __init__.py
        │   │   ├── json_emitter.py
        │   │   ├── markdown_docs_emitter.py
        │   │   ├── spark_structtype_emitter.py
        │   │   ├── templates
        │   │   │   ├── databricks
        │   │   │   │   ├── alter_table.sql.j2
        │   │   │   │   └── create_table.sql.j2
        │   │   │   └── docs
        │   │   │       └── datatable_contract_docs.md.j2
        │   │   └── yaml_emitter.py
        │   ├── __init__.py
        │   ├── loaders
        │   │   ├── __init__.py
        │   │   ├── structtype_loader.py
        │   │   └── yaml_loader.py
        │   ├── models
        │   │   ├── base.py
        │   │   ├── datatable.py
        │   │   ├── __init__.py
        │   │   └── option_types.py
        │   ├── type_converter.py
        │   └── validation.py
        └── __init__.py
```
