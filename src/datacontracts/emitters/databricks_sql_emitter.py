import os
import re

from jinja2 import Environment, FileSystemLoader

from ..models.datatable import DataTableContract
from ..type_converter import to_databricks_sql_type

SAFE_IDENTIFIER_REGEX = re.compile(r"^[a-zA-Z_][a-zA-Z0-9_]*$")

UNSAFE_PATTERNS = [
    r"\bDROP\s+TABLE\b",
    r"\bTRUNCATE\s+TABLE\b",
    r"\bDELETE\s+FROM\b",
    r";",  # Disallow semicolons if possible
    r"--",  # Disallow SQL comments
    r"/\*",  # Disallow block comments
]


def check_for_unsafe_sql(value):
    for pattern in UNSAFE_PATTERNS:
        if re.search(pattern, value, flags=re.IGNORECASE):
            raise ValueError(f"Dangerous SQL pattern found in value: {value}")


def validate_tags_and_column_properties(table_dict: dict):
    """_summary_

    Args:
        table_dict (dict): _description_
    """
    for tag in table_dict.get("discovery_tags", []):
        check_for_unsafe_sql(tag)
    for col in table_dict["columns"]:
        for field in ["description", "sensitivity_type", "sensitivity_level"]:
            val = col.get(field)
            if val:
                check_for_unsafe_sql(str(val))


def validate_identifiers(table_dict: dict):
    """Validates dict representation of a DataTableContract
    to prevent SQL Injection.

    Args:
        table_dict (dict): Dict representation of DataTableContract.
    """
    for key in ["catalog_name", "schema_name", "table_name"]:
        if key not in table_dict:
            raise KeyError(f"Missing required key: {key}")
        if not SAFE_IDENTIFIER_REGEX.match(str(table_dict[key])):
            raise ValueError(f"Unsafe SQL identifier: {table_dict[key]}")
    if "columns" not in table_dict or not isinstance(table_dict["columns"], list):
        raise KeyError("Missing or invalid 'columns' list in table definition")
    for col in table_dict["columns"]:
        if not isinstance(col, dict):
            raise ValueError(f"Column should be a dict: {col}")
        if "column_name" not in col:
            raise KeyError("Missing required key: 'column_name' in a column")
        if not SAFE_IDENTIFIER_REGEX.match(str(col["column_name"])):
            raise ValueError(f"Unsafe column name: {col['column_name']}")


def datatable_contract_to_create_table_sql(contract: DataTableContract) -> str:
    """Returns a SQL string to create a table
    based on the definition i the DataTableContract.

    Args:
        contract (DataTableContract): DataTableContract Pydantic class.

    Returns:
        str: SQL string for table creation.
    """
    template_folder = os.path.join(os.path.dirname(__file__), "templates", "databricks")
    template_folder = os.path.normpath(template_folder)
    template_file = "create_table.sql.j2"
    env = Environment(
        loader=FileSystemLoader(template_folder), trim_blocks=True, lstrip_blocks=True
    )

    template = env.get_template(template_file)

    contract_data = contract.model_dump()
    # Isolate table dict part for validation against SQL inject
    table_dict = contract_data["table"]
    validate_identifiers(table_dict=table_dict)
    validate_tags_and_column_properties(table_dict=table_dict)

    for column in contract_data["table"]["columns"]:
        try:
            column["target_data_type"] = to_databricks_sql_type(column["data_type"])
        except KeyError:
            raise ValueError(f"Unsupported type for Databricks: {column['data_type']}")

    return template.render(contract_data)


def datatable_contract_to_alter_table_sql(contract: DataTableContract) -> str:
    """_summary_

    Args:
        contract (DataTableContract): _description_

    Returns:
        str: _description_
    """
    template_folder = os.path.join(os.path.dirname(__file__), "templates", "databricks")
    template_folder = os.path.normpath(template_folder)
    template_file = "alter_table.sql.j2"
    env = Environment(
        loader=FileSystemLoader(template_folder), trim_blocks=True, lstrip_blocks=True
    )

    template = env.get_template(template_file)

    contract_data = contract.model_dump()
    # Isolate table dict part for validation against SQL inject
    table_dict = contract_data["table"]
    validate_identifiers(table_dict=table_dict)
    validate_tags_and_column_properties(table_dict=table_dict)

    for column in contract_data["table"]["columns"]:
        try:
            column["target_data_type"] = to_databricks_sql_type(column["data_type"])
        except KeyError:
            raise ValueError(f"Unsupported type for Databricks: {column['data_type']}")

    return template.render(contract_data)
