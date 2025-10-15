from typing import Optional

from pydantic import BaseModel, ConfigDict

from .base import Field, Table
from .option_types import ContractType, LifecycleStatus


class DataTableContract(BaseModel):
    contract_type: ContractType = Field(
        ContractType.DATATABLE_CONTRACT, description="The contract type", frozen=True
    )

    contract_description: Optional[str] = Field(
        None, description="Description of the Datatable contract"
    )

    lifecycle_status: Optional[LifecycleStatus] = Field(
        None, description="Lifecycle status of the contract"
    )

    table: Table = Field(..., description="The table in the contract")

    model_config = ConfigDict(
        validate_by_name=True,
        validate_by_alias=True,
        use_enum_values=True,
    )
