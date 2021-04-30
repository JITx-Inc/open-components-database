import os
import re
from dataclasses import dataclass
from typing import List, Optional

ROOT_DIRECTORY = "open-components-database/"
OUTPUT_DIRECTORY = "test-evaluate/"
PREFIX_FILE_NAME = "../"    # This points to the root when in the OUTPUT_DIRECTORY
COMPONENT_FILENAME = "test-components.stanza"
COMPONENT_PACKAGE_NAME = "test/evaluate-components"
File = List[str]
PACKAGE_REGEX = "[\w!?/-]+"
VARIABLE_REGEX = "[\w!?-]+"
TYPE_REGEX = "(?:Char|String|Byte|Int|Long|Float|Double|(?:True|False))"
TYPE_SAMPLE = {
    "Char": '"c"',
    "String": '"hello world"',
    "Byte": 'to-byte(1)',
    "Int": '1',
    "Long": '1L',
    "Float": '1.0F',
    "Double": '1.0',
    "True|False": 'true'
}

def read_file(filename: str) -> File:
    with open(filename, "r") as f:
        return f.readlines()

def write_file(filename: str, file: File):
    with open(filename, "w") as f:
        f.write("".join(file))

def write_output_file(filename: str, file: File):
    write_file(OUTPUT_DIRECTORY + filename, file)

def is_stanza_file(filename: str) -> bool:
    return filename[-7:] == ".stanza"

@dataclass
class Component:
    name: str
    argument_type: Optional[str]

def parse_components(file: File) -> List[Component]:
    return [Component(m.group(1), m.group(2))
                for line in file
                    if (m := re.match(f"^public +pcb-component +({VARIABLE_REGEX}) *(?:\( *{VARIABLE_REGEX} *: *({TYPE_REGEX}) *\))? *:", line))]

def parse_package_name(file: File):
    for line in file:
        if m := re.match(f"^defpackage +({PACKAGE_REGEX})", line):
            return m.group(1)

    raise Exception("No defpackage statement")

def generate_test_file(components: List[str], tested_package_name: str):
    test_package_name = "test/components/" + tested_package_name
    file = ["#use-added-syntax(tests)\n",
           f"defpackage {test_package_name}:\n",
           f"  import {tested_package_name}\n",
            "  import jitx/commands\n",
            "\n"]

    for component in components:
        file.extend([f"deftest {test_name}:\n",
                     f"  print-def({component})"])

@dataclass
class PackageInfo:
    package_name: str
    file_name: str

def write_stanza_dot_proj(package_infos: List[PackageInfo]):
    PACKAGE_TEMPLATE = 'package {package_name} defined-in "{file_name}"\n'
    file = [PACKAGE_TEMPLATE.format(package_name=COMPONENT_PACKAGE_NAME, file_name=COMPONENT_FILENAME)]
    for info in package_infos:
        file.append(PACKAGE_TEMPLATE.format(package_name=info.package_name, file_name=info.file_name))

    write_output_file("stanza.proj", file)


if __name__ == "__main__":
    os.makedirs(OUTPUT_DIRECTORY, exist_ok=True)
    package_infos = []
    # Should use Jinja2 templating engine
    component_file = ["#use-added-syntax(tests)\n",
                     f"defpackage {COMPONENT_PACKAGE_NAME}:\n",
                      "  import jitx/commands\n",
                      "\n"]
    for directory, _, filenames in os.walk(ROOT_DIRECTORY):
        for filename in filenames:
            if is_stanza_file(filename):
                file_path = os.path.join(directory, filename)
                file = read_file(file_path)
                components = parse_components(file)
                if components:
                    package_name = parse_package_name(file)
                    package_infos.append(PackageInfo(package_name, PREFIX_FILE_NAME + file_path))
                    for component in components:
                        resolved_component = f"{package_name}/{component.name}"
                        test_name = "test-" + resolved_component.replace('/', '_')
                        if component.argument_type is None:
                            argument = ""
                        else:
                            argument = f"({TYPE_SAMPLE[component.argument_type]})"
                        evaluated_component = f"{resolved_component}{argument}"
                        component_file.extend([f"deftest {test_name}:\n",
                                               f"  print-def({evaluated_component})\n"
                                                "\n"])
                        print(f"> Found component {evaluated_component}")

    write_output_file(COMPONENT_FILENAME, component_file)
    write_stanza_dot_proj(package_infos)
