from pyspark.sql.types import DecimalType, StructType

from ..models.base import Column, Table
from ..models.datatable import DataTableContract
from ..type_converter import from_spark_type


def datatable_contract_from_structtype(
    struct_type: StructType,
    catalog_name: str,
    schema_name: str,
    table_name: str,
    contract_description: str = None,
    lifecycle_status: str = None,
) -> DataTableContract:
    """Returns a minimal DataTableContract class
        from an instantiated StructType

    Args:
        struct_type (StructType): Spark StructType
        catalog_name (str): Name of catalog where table resides
        schema_name (str): Name of schema where table resides
        table_name (str):
        contract_description (str, optional): _description_. Defaults to None.
        lifecycle_status (str, optional): _description_. Defaults to None.

    Returns:
        DataTableContract: Pydantic DataTableContract class
    """
    columns = []
    for field in struct_type.fields:
        # get column description (comment) from metadata
        # TODO: This requires a convention I am prioritizing "comment" as in SQL
        metadata = {key.lower(): value for key, value in field.metadata.items()}
        description = metadata.get("comment") or metadata.get("description")

        # handle decimal scale/precision
        numeric_scale = None
        numeric_precision = None
        if isinstance(field.dataType, DecimalType):
            numeric_scale = field.dataType.scale
            numeric_precision = field.dataType.precision

        column = Column(
            column_name=field.name,
            data_type=from_spark_type(field.dataType),
            is_nullable=field.nullable,
            description=description,
            numeric_scale=numeric_scale,
            numeric_precision=numeric_precision,
        )
        columns.append(column)

    table = Table(
        catalog_name=catalog_name,
        schema_name=schema_name,
        table_name=table_name,
        columns=columns,
    )

    contract = DataTableContract(
        contract_description=contract_description, lifecycle_status=lifecycle_status, table=table
    )
    return contract
