import yaml
from pydantic import ValidationError

from ..models.datatable import DataTableContract


def datatable_contract_from_yaml_file(file_path: str) -> DataTableContract:
    """Returns a Pydantic DataTableContract class
    after parsing its definition from a yaml file.

    Args:
        file_path (str): Path to yaml contract file.

    Returns:
        DataTableContract: DataTableContract Pydantic class.
    """
    try:
        with open(file_path, "r") as file:
            data = yaml.safe_load(file)
    except FileNotFoundError as e:
        raise FileNotFoundError(f"File not found: {file_path}") from e
    except yaml.YAMLError as e:
        raise yaml.YAMLError(f"Invalid YAML content in {file_path}") from e
    except Exception as e:
        raise Exception(f"Unexpected error while reading {file_path}: {e}") from e

    try:
        return DataTableContract(**data)
    except ValidationError as e:
        raise ValidationError(f"Invalid data according to DataTableContract schema: {e}")
