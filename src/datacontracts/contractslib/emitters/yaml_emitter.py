import yaml

from ..models.datatable import DataTableContract


def datatable_contract_to_yaml(contract: DataTableContract, exclude_unset_fields=False) -> str:
    """Returns the contract schema as a formatted YAML string."""

    return yaml.dump(
        contract.model_dump(exclude_unset=exclude_unset_fields),
        sort_keys=False,
        default_flow_style=False,
    )
