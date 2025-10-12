# krs-datacontracts

## Usefull commands

``` bash
# Sort imports
ruff check --select I --fix

# Running the demos in the tools folder (module)
uv run -m tools.demo_load_and_emit
```

``` bash
├── databricks.yml  # Configuration file for databricks-connect settings
├── data_contracts  # Project root module
│   ├── contracts  # Contains Pydantic models and emitter and loader functions
│   │   ├── emitters  # Emitter function modules for each output type
│   │   │   ├── databricks_sql_emitter.py # Emits CREATE and ALTER Table SQL
│   │   │   ├── __init__.py
│   │   │   ├── json_schema_emitter.py  # Emits JSON schema
│   │   │   ├── markdown_docs_emitter.py  #Emits Markdown documentation
│   │   │   ├── spark_structtype_emitter.py  #Emits Spark StructType
│   │   │   ├── templates  # Jinja 2 templates for SQL and Markdown output
│   │   │   │   ├── databricks
│   │   │   │   │   ├── alter_table.sql.j2
│   │   │   │   │   └── create_table.sql.j2
│   │   │   │   └── docs
│   │   │   │       └── datatable_contract_docs.md.j2
│   │   │   └── yaml_emitter.py  # Emits YAML contract data
│   │   ├── __init__.py
│   │   ├── loaders  # Loaders used to instantiate the Pydantic DataTableContract class
│   │   │   ├── __init__.py
│   │   │   ├── structtype_loader.py  # Loads from a Spark StructType
│   │   │   └── yaml_loader.py  # Loads from a YAML contract definition
│   │   ├── models
│   │   │   ├── base.py  # Contains Pydantic contract components
│   │   │   ├── datatable.py  # Contains the DataTableContract class
│   │   │   ├── __init__.py
│   │   │   └── option_types.py  # Contains Enums for typing in contract
│   │   ├── type_converter.py  # Contains data type convertions for backends
│   │   └── validator.py  # An example of a min/max validator
│   ├── __init__.py
│   ├── json_schemas  # Containg JSON schema for contract, used for intellisense in yaml file
│   │   └── data-table-contract.schema.json
│   └── yaml  # Contains yaml contracts: [catalog_name]__[schema_name]__[table_name].yaml
│       └── service__hr__employee.yaml
├── pyproject.toml
├── README.md
├── requirements.txt
├── ruff.toml
├── tools
│   ├── demo_load_and_emit.py
│   └── __init__.py
└── uv.lock
```

