from enum import Enum


# Section: Enums for delimiters and data types
# =================================================
class DataType(str, Enum):
    """Enum representing possible data types for a column in a data table contract."""

    STRING = "string"
    INTEGER = "integer"
    LONG = "long"
    DOUBLE = "double"
    BOOLEAN = "boolean"
    TIMESTAMP = "timestamp"
    DATE = "date"
    FLOAT = "float"
    DECIMAL = "decimal"


class SqlDialect(str, Enum):
    """Enum representing possible SQL dialects."""

    DATABRICKS = "databricks"
    SPARK = "spark"
    MSSQL = "mssql"
    POSTGRES = "postgres"


class TimeResolutionUnit(str, Enum):
    """Enum representing possible time resolution units."""

    MILLISECONDS = "milliseconds"
    SECONDS = "seconds"
    MINUTES = "minutes"
    HOURS = "hours"
    DAYS = "days"
    MONTHS = "months"
    YEARS = "years"


class SensitivityLevel(str, Enum):
    """Enum representing data sensitivity levels."""

    PUBLIC = "public"  # Data that can be freely shared publicly
    INTERNAL = "internal"  # Data for internal use only, not meant for external sharing
    CONFIDENTIAL = "confidential"  # Sensitive business data requiring protection
    RESTRICTED = "restricted"  # Highly sensitive data requiring strict controls
    REGULATED = "regulated"  # Data subject to regulatory compliance requirements


class SensitivityType(str, Enum):
    """Enum representing types of sensitive data."""

    PII = "pii"  # Personally Identifiable Information
    PHI = "phi"  # Protected Health Information
    PPI = "ppi"  # Personal Payment Information
    FINANCIAL = "financial"  # Financial data (revenue, costs, etc.)
    PRICE = "price"  # Pricing data (costs, prices, etc.)
    STRATEGIC = "strategic"  # Strategic business information
    INTELLECTUAL_PROPERTY = "intellectual_property"  # IP, trade secrets
    CREDENTIALS = "credentials"  # Authentication data


class ContractType(str, Enum):
    """Enum representing types of data contracts"""

    DATATABLE_CONTRACT = "datatable_contract"  # A datatabel serialized as table or view
    DATASET_CONTRACT = "dataset_contract"  # A collection of tables for semantic models


class MaterializationType(str, Enum):
    """Enum representing materilazation type of table type objects"""

    TABLE = "table"  # Materialized as a table object
    VIEW = "view"  # Materialized as a view object


class LifecycleStatus(str, Enum):
    EXPERIMENTAL = "experimental"  # The object is under development and can change
    ACTIVE = "active"  # The object is published for use
    DEPRECATED = "deprecated"  # The object is deprecated and may be replaced
    EXPIRED = "expired"  # The object is expired and withdrawn from active use
