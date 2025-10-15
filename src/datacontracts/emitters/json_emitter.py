import json

from ..models.datatable import DataTableContract


def datatable_contract_to_json(contract: DataTableContract, exclude_unset_fields=False) -> str:
    """Returns the contract schema as a formatted JSON string."""

    return contract.model_dump_json(indent=2, exclude_unset=exclude_unset_fields)


# BOOKMARK: Placed here for consistency but easily used directly from class
def datatable_contract_to_json_schema(contract: DataTableContract) -> json:
    """Returns the JSON schema for a DataTableContract

    Args:
        contract (DataTableContract): Pydantic DataTableContract class

    Returns:
        json: JSON Schema (formatted) for the DataTableContract
    """

    return DataTableContract.model_json_schema()
