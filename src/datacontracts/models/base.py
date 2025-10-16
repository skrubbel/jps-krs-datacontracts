from typing import List, Optional, Any, Union

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    computed_field,
    model_serializer,
    model_validator,
)

from .option_types import (
    CheckSeverity,
    CheckType,
    DataType,
    MaterializationType,
    SensitivityLevel,
    SensitivityType,
)


class TableCheck(BaseModel):
    """A data quality check at the table level."""

    check_name: str = Field(..., description="Unique name for this check")
    check_type: CheckType = Field(..., description="Type of check to perform")
    severity: CheckSeverity = Field(
        default=CheckSeverity.ERROR, description="Severity of check failure"
    )

    # For row count checks
    min_row_count: Optional[int] = Field(None, description="Minimum expected row count")
    max_row_count: Optional[int] = Field(None, description="Maximum expected row count")

    # For custom SQL checks
    sql_expression: Optional[str] = Field(
        None, description="Custom SQL expression that should return rows violating the rule"
    )

    # For freshness checks
    freshness_column: Optional[str] = Field(None, description="Column to check for data freshness")
    max_age_hours: Optional[int] = Field(None, description="Maximum age of data in hours")

    description: Optional[str] = Field(None, description="Description of what this check validates")

    model_config = ConfigDict(use_enum_values=True)


class ColumnCheck(BaseModel):
    """A data quality check for a specific column."""

    check_name: str = Field(..., description="Unique name for this check")
    check_type: CheckType = Field(..., description="Type of check to perform")
    column_name: str = Field(..., description="Column to check")
    severity: CheckSeverity = Field(
        default=CheckSeverity.ERROR, description="Severity of check failure"
    )

    # Optional parameters for different check types
    accepted_values: Optional[List[Any]] = Field(
        None, description="List of accepted values (for accepted_values check)"
    )
    regex_pattern: Optional[str] = Field(
        None, description="Regex pattern to match (for regex_match check)"
    )
    date_format: Optional[str] = Field(
        None, description="Expected date format string (e.g., '%Y-%m-%d')"
    )
    min_value: Optional[Union[int, float]] = Field(
        None, description="Minimum acceptable value (for range check)"
    )
    max_value: Optional[Union[int, float]] = Field(
        None, description="Maximum acceptable value (for range check)"
    )
    min_length: Optional[int] = Field(None, description="Minimum string length")
    max_length: Optional[int] = Field(None, description="Maximum string length")
    reference_table: Optional[str] = Field(
        None, description="Reference table for foreign key checks"
    )
    reference_column: Optional[str] = Field(
        None, description="Reference column for foreign key checks"
    )

    description: Optional[str] = Field(None, description="Description of what this check validates")

    model_config = ConfigDict(use_enum_values=True)


# Section: Data Contract Component Classes
# =================================================
class Column(BaseModel):
    """Represents a column schema in a data contract."""

    # Mandatory fields
    column_name: str = Field(..., description="Column name")
    data_type: DataType = Field(..., description="Data type of the column")
    is_nullable: bool = Field(..., description="Is the column nullable?")

    # Optional fields
    numeric_scale: Optional[int] = Field(
        None, description="Numeric scale value for decimals", le=38
    )
    numeric_precision: Optional[int] = Field(
        None, description="Numeric precision value for decimals", le=38
    )
    min_value: Optional[int] = Field(None, description="Minimum value of column content")
    max_value: Optional[int] = Field(None, description="Maximum value of column content")
    description: Optional[str] = Field(None, description="Description of the column")
    is_id: Optional[bool] = Field(None, description="Is this an identity column")
    is_primary_key: Optional[bool] = Field(None, description="Is the column a primary key?")
    is_business_key: Optional[bool] = Field(None, description="Is this column a business key")
    is_foreign_key: Optional[bool] = Field(None, description="Is this a foreign key column")
    sensitivity_level: Optional[SensitivityLevel] = Field(
        None, description="Data sensitivity classification"
    )
    sensitivity_type: Optional[SensitivityType] = Field(
        None, description="Type of sensitive data contained in the column"
    )

    # Validate Primary Key columns are not nullable
    @model_validator(mode="after")
    def ensure_primary_key_not_nullable(self) -> "Column":
        """Ensure primary keys are not nullable by automatically setting is_nullable to False."""
        if self.is_primary_key:
            # Modify the instance directly
            object.__setattr__(self, "is_nullable", False)
        return self

    # Validate decimal precision and scale values
    @model_validator(mode="after")
    def validate_decimal_fields(self):
        """Ensure correct scale and precision values for decimal types"""
        if self.data_type == DataType.DECIMAL:
            if self.numeric_precision is None or self.numeric_scale is None:
                raise ValueError(
                    "numeric_precision and numeric_scale are required when data_type is 'decimal'."
                )
            if self.numeric_scale > self.numeric_precision:
                raise ValueError(
                    "numeric_scale must be less than or equal to numeric_precision for decimal columns."
                )
        return self

    # Validate min - max range
    @model_validator(mode="after")
    def validate_min_max(self):
        if self.min_value and self.max_value:
            if self.max_value < self.min_value:
                raise ValueError("max_value must be larger than or equal to min_value!")
        return self

    @model_serializer
    def serialize_model(self):
        """Control serialization order."""
        return {
            "column_name": self.column_name,
            "data_type": self.data_type,
            "is_nullable": self.is_nullable,
            "numeric_scale": self.numeric_scale,
            "numeric_precision": self.numeric_precision,
            "min_value": self.min_value,
            "max_value": self.max_value,
            "description": self.description,
            "is_id": self.is_id,
            "is_primary_key": self.is_primary_key,
            "is_business_key": self.is_business_key,
            "is_foreign_key": self.is_foreign_key,
            "sensitivity_level": self.sensitivity_level,
            "sensitivity_type": self.sensitivity_type,
        }

    model_config = ConfigDict(
        validate_by_name=True,
        validate_by_alias=True,
        use_enum_values=True,
    )


class Table(BaseModel):
    """Represents a table schema in a data contract."""

    # Mandatory fields
    catalog_name: str = Field(..., description="Catalog name")
    schema_name: str = Field(..., description="Schema name")
    table_name: str = Field(..., description="Table name")
    columns: List[Column] = Field(..., description="List of columns in the table")

    # Optional fields
    materialization_type: Optional[MaterializationType] = Field(
        None, description="Materialization Type"
    )
    description: Optional[str] = Field(None, description="Table description")
    discovery_tags: Optional[List[str]] = Field(None, description="Search tags for table discovery")

    partition_by: Optional[List[str]] = Field(None, description="Columns to partition the table by")
    change_track_columns: Optional[List[str]] = Field(
        None, description="Columns to track for SCD changes"
    )

    @computed_field(description="Does the table contain sensitive data?")
    @property
    def has_sensitive_data(self) -> bool:
        return len(self.sensitive_columns) > 0

    @computed_field(description="Sensitivity labelled columns in the table")
    @property
    def sensitive_columns(self) -> List[str]:
        return [
            column.column_name for column in self.columns if column.sensitivity_type is not None
        ]

    @computed_field(description="Discovery tags as a comma separated string")
    @property
    def discovery_tags_string(self) -> str:
        if self.discovery_tags:
            return ", ".join(self.discovery_tags)

    @model_serializer
    def serialize_model(self):
        """Control serialization order."""
        return {
            "catalog_name": self.catalog_name,
            "schema_name": self.schema_name,
            "table_name": self.table_name,
            "description": self.description,
            "materialization_type": self.materialization_type,
            "discovery_tags": self.discovery_tags,
            "discovery_tags_string": self.discovery_tags_string,
            "partition_by": self.partition_by,
            "change_track_columns": self.change_track_columns,
            "has_sensitive_data": self.has_sensitive_data,
            "sensitive_columns": self.sensitive_columns,
            "columns": [col.model_dump() for col in self.columns],
        }

    model_config = ConfigDict(
        validate_by_name=True,
        validate_by_alias=True,
        use_enum_values=True,
    )
