import json


from pyspark.sql.types import (
    DecimalType,
    FloatType,
    IntegerType,
    StringType,
    StructField,
    StructType,
)

from datacontracts import (
    databricks_sql_emitter,
    json_emitter,
    markdown_docs_emitter,
    spark_structtype_emitter,
    yaml_emitter,
    structtype_loader,
    yaml_loader,
    DataTableContract,
)


CONTRACTS_HOME = "./src/datacontracts/contracts/yaml"


def demo_load_yaml_emit_yaml(exclude_unset_fields: bool = False) -> DataTableContract:
    """Demonstrates how to load and emit a DataTableContract
    from a yaml file definition to a yaml contract.
    """

    # Instantiate DataTableContract class by reading yaml file
    contract = yaml_loader.datatable_contract_from_yaml_file(
        f"{CONTRACTS_HOME}/service__hr__employee.yaml"
    )

    # Print the YAML representation of the contract using yaml_emitter
    yaml_contract = yaml_emitter.datatable_contract_to_yaml(
        contract=contract, exclude_unset_fields=exclude_unset_fields
    )
    print(yaml_contract)


def demo_load_yaml_emit_json(exclude_unset_fields: bool = False) -> DataTableContract:
    """Demonstrates how to load and emit a DataTableContract
    from a yaml file definition to a yaml contract.
    """
    # Instantiate DataTableContract class by reading yaml file
    contract = yaml_loader.datatable_contract_from_yaml_file(
        f"{CONTRACTS_HOME}/service__hr__employee.yaml"
    )

    json_contract = json_emitter.datatable_contract_to_json(
        contract=contract, exclude_unset_fields=exclude_unset_fields
    )
    print(json_contract)


def demo_structtype_loader():
    """Demonstrates how to load a DataTableContract
    from a Spark StructType.
    """
    # Set up the StructType or infer it from a table
    schema = StructType(
        [
            StructField(
                "employee_id", IntegerType(), False, {"comment": "Employee Id"}
            ),
            StructField(
                "employee_name", StringType(), False, {"comment": "Employee Name"}
            ),
            StructField(
                "salary",
                DecimalType(precision=10, scale=5),
                False,
                {"comment": "Employee Salary"},
            ),
        ]
    )

    # Instantiate DataTableContract class from StructType
    contract = structtype_loader.datatable_contract_from_structtype(
        struct_type=schema,
        catalog_name="service",
        schema_name="hr",
        table_name="employee",
    )

    # Convert to yaml (if we should serialize a DataTableContract from StructType)
    yaml_contract = yaml_emitter.datatable_contract_to_yaml(contract=contract)

    # Display the yaml representation
    print(yaml_contract)


def demo_databricks_sql_emitter():
    """Demonstrates how to generate SQL for
    table creation, based on a yaml contract.
    """

    # Load DataTableContract from yaml file
    contract = yaml_loader.datatable_contract_from_yaml_file(
        f"{CONTRACTS_HOME}/service__hr__employee.yaml"
    )

    # SQL for creating table
    create_sql = databricks_sql_emitter.datatable_contract_to_create_table_sql(
        contract=contract
    )

    # SQL for altering table
    alter_sql = databricks_sql_emitter.datatable_contract_to_alter_table_sql(
        contract=contract
    )

    # Display SQL output
    print(create_sql)
    print("")
    print(alter_sql)


def demo_json_schema_emitter():
    """Demonstrates how to generate a JSON schema
    from a DataTableContract.
    """

    # Instantiate DataTableContract class by reading yaml file
    contract = yaml_loader.datatable_contract_from_yaml_file(
        f"{CONTRACTS_HOME}/service__hr__employee.yaml"
    )

    # Emit the DataTableContract to a JSON Schema (used for intellisense/validation in yaml)
    json_schema = json_emitter.datatable_contract_to_json_schema(contract=contract)

    # Display the JSON Schema
    print(json_schema)

    schema_file_path = f".{CONTRACTS_HOME}/json_schemas/data-table-contract.schema.json"

    # Can be saved to file with something like this:
    # schema_file_name = "data-table-contract.schema.json"

    with open(f"{schema_file_path}", "w") as f:
        json.dump(json_schema, f, indent=2)


def demo_markdown_docs_emitter():
    """Demonstrates how to generate markdown
    documentation from DataTableContract content.
    """

    # Instantiate DataTableContract class by reading yaml file
    contract = yaml_loader.datatable_contract_from_yaml_file(
        f"{CONTRACTS_HOME}/service__hr__employee.yaml"
    )

    # Use the markdown_docs_emitter to get the markdown string
    markdown_string = markdown_docs_emitter.datatable_contract_to_markdown_docs(
        contract=contract
    )

    # Display the output
    print(markdown_string)

    # This could be written to a markdown file and used
    # in a static site generator like Hugo or MKDocs


def demo_spark_structtype_emitter():
    """Demonstrates how to generate a Spark StructType
    from a DataTableContract (parsed from yaml).
    """

    # Instantiate DataTableContract class by reading yaml file
    contract = yaml_loader.datatable_contract_from_yaml_file(
        f"{CONTRACTS_HOME}/service__hr__employee.yaml"
    )

    # Get the StructType representation of the contract
    struct = spark_structtype_emitter.datatable_contract_to_spark_schema(
        contract=contract
    )

    # Print the struct tree (simple structure output)
    print(struct.treeString())

    # Print the JSON representation (Contains metadata)
    print(struct.jsonValue())


if __name__ == "__main__":
    # Run these demos as module with: uv run -m tools.demo_load_and_emit
    # Uncomment the one you would like to test :-)

    # demo_load_yaml_emit_yaml()
    demo_load_yaml_emit_yaml()
    demo_load_yaml_emit_json()
    # demo_structtype_loader()
    # demo_databricks_sql_emitter()
    # demo_json_schema_emitter()
    # demo_markdown_docs_emitter()
    # demo_spark_structtype_emitter()
