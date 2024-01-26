import os
import yaml
from pathlib import Path
from jinja2 import (
    Environment, 
    BaseLoader, 
    FileSystemLoader, 
    Template
)
from typing import Any


def parse_conf_yml(
    searchpath: str = "conf",
    template_file: str = "deployment.yml",
    variables_filepath: str = "conf/topic_sources.yaml",
) -> None:
    loader: BaseLoader | None = FileSystemLoader(searchpath=searchpath)
    env: Environment = Environment(loader=loader)
    template: Template = env.get_template(name=template_file)

    variables: Any = yaml.safe_load(
        stream=Path(variables_filepath).read_text(encoding="utf-8")
    )
    output_from_parsed_template: str = template.render(env=os.environ, var=variables)

    # to save the results
    skip: str | None = os.getenv(key="SKIP_DATA_PREP")
    print(skip)
    filename: str = f"my_newfile_{skip}.yml"
    with open(file=filename, mode="w") as fh:
        print(f"Writing to {filename}...")
        fh.write(output_from_parsed_template)
        print("done")
