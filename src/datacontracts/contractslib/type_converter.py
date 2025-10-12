from typing import Any

from pyspark.sql.types import (
    BooleanType,
    DateType,
    DecimalType,
    DoubleType,
    FloatType,
    IntegerType,
    LongType,
    StringType,
    TimestampType,
)

from .models.option_types import DataType

# TODO: Extend these mappings as needed.


def from_spark_type(spark_type: Any) -> DataType:
    """Returns the corresponding Contract DataType
    from a Spark DataType.

    Args:
        spark_type (Any): Spark DataType e.g. StringType.

    Returns:
        DataType: Contract DataType
    """
    type_mapping = {
        "StringType": DataType.STRING,
        "IntegerType": DataType.INTEGER,
        "LongType": DataType.LONG,
        "DoubleType": DataType.DOUBLE,
        "BooleanType": DataType.BOOLEAN,
        "TimestampType": DataType.TIMESTAMP,
        "DateType": DataType.DATE,
        "FloatType": DataType.FLOAT,
        "DecimalType": DataType.DECIMAL,
    }

    try:
        spark_type_name = spark_type.__class__.__name__
        return type_mapping[spark_type_name]
    except TypeError:
        raise TypeError(f"Invalid spark_type passed to from_spark_type: {spark_type}")
    except KeyError:
        raise KeyError(f"Unsupported Spark data type: {spark_type_name}")


def to_spark_type(data_type: DataType) -> Any:
    """Returns the corresponding spark data type.

    Args:
        data_type (DataType): Contract DataType.

    Returns:
        Any: Spark DataType e.g. StringType().
    """
    type_mapping = {
        DataType.STRING: StringType(),
        DataType.INTEGER: IntegerType(),
        DataType.LONG: LongType(),
        DataType.DOUBLE: DoubleType(),
        DataType.BOOLEAN: BooleanType(),
        DataType.TIMESTAMP: TimestampType(),
        DataType.DATE: DateType(),
        DataType.FLOAT: FloatType(),
        DataType.DECIMAL: DecimalType(15, 5),  # Default precision/scale
    }

    try:
        spark_type = type_mapping[data_type]
        return spark_type
    except KeyError:
        raise KeyError(f"Unsupported data type given: {DataType}")


def to_databricks_sql_type(data_type: DataType, precision: int = 15, scale: int = 5) -> str:
    """Returns string representation of the corresponding
    SQL data type for a contract DataType.

    Args:
        data_type (DataType): Contract DataType
        precision (int, optional): Precision for Decimal type. Defaults to 10.
        scale (int, optional): Scale for Decimal type. Defaults to 5.

    Returns:
        str: String representation of SQL data type.
    """
    type_mapping = {
        DataType.STRING: "STRING",
        DataType.INTEGER: "INT",
        DataType.LONG: "BIGINT",
        DataType.DOUBLE: "DOUBLE",
        DataType.BOOLEAN: "BOOLEAN",
        DataType.TIMESTAMP: "TIMESTAMP",
        DataType.DATE: "DATE",
        DataType.FLOAT: "FLOAT",
        DataType.DECIMAL: "DECIMAL",
    }

    try:
        sql_type = type_mapping[data_type]
    except KeyError:
        raise ValueError(f"Unsupported DataType: {data_type}")

    # Handle precision & scale for Decimals
    if data_type == DataType.DECIMAL:
        return f"{sql_type}({precision},{scale})"

    return sql_type
