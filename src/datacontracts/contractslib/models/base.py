from typing import List, Optional

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    computed_field,
    model_validator,
)

from .option_types import DataType, MaterializationType, SensitivityLevel, SensitivityType


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

    @model_validator(mode="after")
    def ensure_primary_key_not_nullable(self) -> "Column":
        """Ensure primary keys are not nullable by automatically setting is_nullable to False."""
        if self.is_primary_key:
            # Modify the instance directly
            object.__setattr__(self, "is_nullable", False)
        return self

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

    model_config = ConfigDict(
        validate_by_name=True,
        validate_by_alias=True,
        use_enum_values=True,
        model_fields_set_order=[
            "catalog_name",
            "schema_name",
            "table_name",
            "description",
            "tags",
            # ... other fields in desired order
        ],
    )
