import os

from jinja2 import Environment, FileSystemLoader

from ..models.datatable import DataTableContract


def datatable_contract_to_markdown_docs(contract: DataTableContract) -> str:
    """Returns a markdown document string of the DataTableContract.

    Args:
        contract (DataTableContract): DataTableContract Pydantic class.

    Returns:
        str: Formatted markdown string with contract documentation.
    """
    template_folder = os.path.join(os.path.dirname(__file__), "templates", "docs")
    template_folder = os.path.normpath(template_folder)
    template_file = "datatable_contract_docs.md.j2"
    env = Environment(
        loader=FileSystemLoader(template_folder), trim_blocks=True, lstrip_blocks=True
    )

    template = env.get_template(template_file)

    contract_data = contract.model_dump()

    return template.render(contract_data)
