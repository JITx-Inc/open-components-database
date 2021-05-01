import enum
import os
import re
from dataclasses import dataclass
from typing import List, Optional, Iterable


ROOT_DIRECTORY = "open-components-database/"
OUTPUT_DIRECTORY = "test-evaluate/"
PREFIX_FILE_NAME = "../"    # This points to the root when in the OUTPUT_DIRECTORY
TEST_ENTRYPOINT_FILE_NAME = "api.stanza"
TEST_ENTRYPOINT_PACKAGE_NAME = "test/evaluate/api"
TEST_FILE_NAME = "{top_level}s.stanza"
TEST_PACKAGE_NAME = "test/evaluate/{top_level}s"
EXCLUDED_FILES = ["modules/backplanes.stanza"]
File = List[str]

class TopLevel(enum.Enum):
    Module = "module"
    Component = "component"
    Symbol = "symbol"
    Landpattern = "landpattern"
    Bundle = "bundle"
    Material = "material"
    Stackup = "stackup"
    Pad = "pad"
    Rules = "rules"
    Board = "board"

@dataclass
class PcbObject:
    type: TopLevel
    name: str
    argument_type: Optional[str]

@dataclass
class PackageInfo:
    package_name: str
    file_name: str

def or_regex(strings: Iterable[str]) -> str:
    return "(?:" + "|".join([s.replace("|", "\|") for s in strings]) + ")"

PACKAGE_REGEX = "[\w!?/-]+"
VARIABLE_REGEX = "[\w!?-]+"
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
TYPE_REGEX = or_regex(TYPE_SAMPLE.keys())

OBJECT_REGEX = or_regex([o.value for o in TopLevel])
PCB_OBJECT_REGEX = f"^public +pcb-({OBJECT_REGEX}) +({VARIABLE_REGEX}) *(?:\( *{VARIABLE_REGEX} *: *({TYPE_REGEX}) *\))? *:"
DEFPACKAGE_REGEX = f"^defpackage +({PACKAGE_REGEX})"
PACKAGE_TEMPLATE = 'package {package_name} defined-in "{file_name}"\n'
# Use Jinja2
TEST_FILE_HEADER = ["#use-added-syntax(tests)\n",
                    "defpackage {package_name}:\n",
                    "  import jitx/commands\n",
                    "\n"]
DEFTEST_TEMPLATE = ["deftest {test_name}:\n",
                    "  print-def({evaluated_pcb_object})\n"
                    "\n"]

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

def parse_pcb_objects(file: File) -> List[PcbObject]:
    return [PcbObject(TopLevel(m.group(1)), m.group(2), m.group(3))
                for line in file
                    if (m := re.match(PCB_OBJECT_REGEX, line))]

def parse_package_name(file: File):
    for line in file:
        if m := re.match(DEFPACKAGE_REGEX, line):
            return m.group(1)

    raise Exception("No defpackage statement")

def write_stanza_dot_proj(package_infos: List[PackageInfo]):
    file = [PACKAGE_TEMPLATE.format(package_name=TEST_ENTRYPOINT_PACKAGE_NAME,
                                    file_name=TEST_ENTRYPOINT_FILE_NAME)]
    for top_level in TopLevel:
        file.append(PACKAGE_TEMPLATE.format(package_name=test_package_name(top_level),
                                            file_name=test_file_name(top_level)))
    for info in package_infos:
        file.append(PACKAGE_TEMPLATE.format(package_name=info.package_name, file_name=info.file_name))

    write_output_file("stanza.proj", file)

def format_file_template(file_template: File, **kwargs):
    return [line.format(**kwargs) for line in file_template]

def test_package_name(top_level: TopLevel):
    return TEST_PACKAGE_NAME.format(top_level=top_level.value)

def test_file_name(top_level: TopLevel):
    return TEST_FILE_NAME.format(top_level=top_level.value)

def generate_test_entrypoint_file() -> File:
    file = [f"defpackage {TEST_ENTRYPOINT_PACKAGE_NAME}:\n",]
    for top_level in TopLevel:
        file.append(f"  import {test_package_name(top_level)}\n")

    return file

if __name__ == "__main__":
    os.makedirs(OUTPUT_DIRECTORY, exist_ok=True)
    package_infos = []
    evaluated_excluded_files = [ROOT_DIRECTORY + file for file in EXCLUDED_FILES]
    # Should use Jinja2 templating engine
    test_files = {top_level: format_file_template(TEST_FILE_HEADER, package_name=test_package_name(top_level)) for top_level in TopLevel}
    for directory, _, filenames in os.walk(ROOT_DIRECTORY):
        for filename in filenames:
            if is_stanza_file(filename):
                file_path = os.path.join(directory, filename)
                if file_path in evaluated_excluded_files:
                    break
                file = read_file(file_path)
                pcb_objects = parse_pcb_objects(file)
                if pcb_objects:
                    package_name = parse_package_name(file)
                    package_infos.append(PackageInfo(package_name, PREFIX_FILE_NAME + file_path))
                    for pcb_object in pcb_objects:
                        resolved_pcb_object = f"{package_name}/{pcb_object.name}"
                        test_name = "test-" + resolved_pcb_object.replace('/', '_')
                        if pcb_object.argument_type is None:
                            argument = ""
                        else:
                            argument = f"({TYPE_SAMPLE[pcb_object.argument_type]})"
                        evaluated_pcb_object = f"{resolved_pcb_object}{argument}"
                        test_files[pcb_object.type].extend(format_file_template(DEFTEST_TEMPLATE,
                                                                   test_name=test_name,
                                                                   evaluated_pcb_object=evaluated_pcb_object))
                        print(f"> Found {pcb_object.type.value} {evaluated_pcb_object}")

    write_stanza_dot_proj(package_infos)
    write_output_file(TEST_ENTRYPOINT_FILE_NAME, generate_test_entrypoint_file())
    for top_level, test_file in test_files.items():
        write_output_file(test_file_name(top_level), test_file)
