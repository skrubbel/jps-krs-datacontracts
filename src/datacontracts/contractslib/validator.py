from functools import reduce
from operator import or_

from pyspark.sql import DataFrame
from pyspark.sql import functions as F

from .models.datatable import DataTableContract


# TODO: This is an example implementation of min/max range validation
def validate_dataframe_min_max(df: DataFrame, contract: DataTableContract) -> DataFrame:
    """Returns a DataFrame of invalid rows based on min/max
    rules defined in the DataTableContract

    Args:
        df (DataFrame): Spark DataFrame
        contract (DataTableContract): Pydandic DataTableContract class

    Returns:
        DataFrame: Dataframe with invalid rows from df
    """
    violation_conditions = []
    for col in contract.columns:
        if col.min_value is not None:
            violation_conditions.append(F.col(col.column_name) < col.min_value)
        if col.max_value is not None:
            violation_conditions.append(F.col(col.column_name) > col.max_value)

    if not violation_conditions:
        # TODO: Replace with proper console logging
        print("No min/max validations to enforce, returning empty DataFrame")
        return df.limit(0)

    # Combine conditions with OR logic
    combined_condition = reduce(or_, violation_conditions)
    invalid_rows = df.filter(combined_condition)
    return invalid_rows
