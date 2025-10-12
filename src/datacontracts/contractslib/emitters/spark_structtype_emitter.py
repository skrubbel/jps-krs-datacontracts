from pyspark.sql.types import StructField, StructType

from ..models.datatable import DataTableContract
from ..type_converter import to_spark_type


def datatable_contract_to_spark_schema(contract: DataTableContract) -> StructType:
    """Returns the contract schema as a Spark StructType object.

    Converts the table schema to a Spark StructType including column descriptions
    and other metadata.

    Returns:
        StructType: Spark StructType with column metadata.
    """
    spark_fields = []

    for column in contract.table.columns:
        # Create metadata dictionary
        # TODO: Find convention I am using "comment" as in SQL
        metadata_dict = {"comment": column.description}

        # Add sensitivity information if available
        if column.sensitivity_type:
            metadata_dict["sensitivity_type"] = column.sensitivity_type
        if column.sensitivity_level:
            metadata_dict["sensitivity_level"] = column.sensitivity_level

        # #TODO: Add tags if available
        # if column.tags:
        #     metadata_dict["tags"] = column.tags

        # Create the StructField with name, type, nullability and metadata
        spark_type = to_spark_type(column.data_type)
        field = StructField(
            name=column.column_name,
            dataType=spark_type,
            nullable=column.is_nullable,
            metadata=metadata_dict,  # PySpark accepts a dict directly as metadata
        )

        spark_fields.append(field)

    # Return the complete schema
    return StructType(spark_fields)
