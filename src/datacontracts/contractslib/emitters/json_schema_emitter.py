import json

from ..models.datatable import DataTableContract


# BOOKMARK: Placed here for consistency but easily used directly from class
def datatable_contract_to_json_schema(contract: DataTableContract) -> json:
    """Returns the JSON schema for a DataTableContract

    Args:
        contract (DataTableContract): Pydantic DataTableContract class

    Returns:
        json: JSON Schema (formatted) for the DataTableContract
    """

    return DataTableContract.model_json_schema()
