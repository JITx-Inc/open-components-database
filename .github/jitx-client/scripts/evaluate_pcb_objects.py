import enum
import os
import random
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
# Put all definitions private in those files?
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
    arguments: Optional[List[str]]

@dataclass
class PackageInfo:
    package_name: str
    file_name: str

class TestAnnotationError(Exception):
    """Exception raised when a test annotation is invalid

    Attributes:
        line_number -- line number where the annotation was detected
    """

    def __init__(self, line_number):
        self.line_number = line_number
        self.message = f"<test> annotation is invalid: file {{filename}}, line {self.line_number}"
        super().__init__()

class SkipTestError(Exception):
    pass

def or_regex(strings: Iterable[str]) -> str:
    return "(?:" + "|".join([s.replace("|", "\|") for s in strings]) + ")"

PACKAGE_REGEX = "[\w!?/-]+"
VARIABLE_REGEX = "[\w!?-]+"
VALUE_REGEX = "[-+.!?\"'\w\d]+"
TYPE_SAMPLE = {
    "Char": '"c"',
    "String": '"hello world"',
    "Byte": '1Y',
    "Int": '1',
    "Long": '1L',
    "Float": '1.0F',
    "Double": '1.0',
    "True|False": 'true'
}
TYPE_REGEX = or_regex(TYPE_SAMPLE.keys())

OBJECT_REGEX = or_regex([o.value for o in TopLevel])
# We only test public objects
PCB_OBJECT_REGEX = f"^public +pcb-({OBJECT_REGEX}) +({VARIABLE_REGEX}) *(?:\( *({VARIABLE_REGEX}) *: *({TYPE_REGEX}) *\))? *:"
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

# returns:
#   None: pcb object takes no argument
#   List[str]: pcb object takes 1 argument and this is the different values to input into the multiple generated tests
# raises:
#   TestAnnotationError: invalid annotation, can't determine arguments
#   SkipTestError: this test should be skipped
def choose_pcb_object_arguments(arg_name: str, arg_type: str, file: File, line_number: int) -> Optional[List[str]]:
    if file[line_number - 1].startswith(";<test>skip<test>"):
        # skip when no argument
        raise SkipTestError()
    if arg_name is None:
        return None
    elif file[line_number - 1].startswith("<test>"):
        cursor = line_number - 2
        while cursor >= 0 and not file[cursor].startswith(";<test>"):
            cursor -= 1
        if cursor == -1:
            raise TestAnnotationError(line_number - 1)
        if "skip" in file[cursor][7:]:
            # skip when 1 argument
            raise SkipTestError()
        for number in range(cursor + 1, line_number - 1):
            if (m := re.match(f"^({VARIABLE_REGEX}):(.*);?", file[number]))\
                    and m.group(1) == arg_name\
                    and (n := re.findall(VALUE_REGEX, m.group(2))):
                if set(n) == {"even", "positive"}:
                    return [2 * random.randint(1, 50)]
                else:
                    return n
            else:
                raise TestAnnotationError(number)
    else:
        cursor = line_number + 1
        # Detect function body
        while cursor < len(file) and file[cursor][0] in ("\n", " ", ";") :
            cursor += 1

        function_code = [l := remove_comment(line) for line in file[line_number + 1:cursor] if not re.match(" *\n", l)]
        for line_idx, line in enumerate(function_code[:-1]) :
            #if re.match("[^;]*switch\({arg_name}\)\n".format(arg_name=arg_name), file[cursor]):
            if f"switch({arg_name})" in line :
                if (m := re.match(f" *({VALUE_REGEX}) *:", function_code[line_idx + 1])):
                    print(f"Switch parsing failure: can't retrieve example value in\n```\n{line + function_code[line_idx + 1]}\n```")
                    return [m.group(1)]

        return [TYPE_SAMPLE[arg_type]]

def remove_comment(line: str) -> str :
    idx = line.find(';')
    if idx >= 0:
        return line[:idx] + "\n"
    else:
        return line

def parse_pcb_objects(file: File, file_path: str) -> List[PcbObject]:
    objects = []
    for line_number, line in enumerate(file):
        if (m := re.match(PCB_OBJECT_REGEX, line)):
            try:
                objects.append(PcbObject(TopLevel(m.group(1)),
                                         m.group(2),
                                         choose_pcb_object_arguments(m.group(3), m.group(4), file, line_number)))
            except SkipTestError:
                print(f"> Skipped {file_path}")
            except TestAnnotationError as e:
                print(e.message.format(filename=file_path))
                exit(1)
    return objects

def parse_package_name(file: File):
    for line in file:
        if m := re.match(DEFPACKAGE_REGEX, line):
            return m.group(1)

    raise Exception("No defpackage statement")

def write_stanza_dot_proj():
    file = ['include "../open-components-database/stanza.proj"',
            PACKAGE_TEMPLATE.format(package_name=TEST_ENTRYPOINT_PACKAGE_NAME,
                                    file_name=TEST_ENTRYPOINT_FILE_NAME)]
    for top_level in TopLevel:
        file.append(PACKAGE_TEMPLATE.format(package_name=test_package_name(top_level),
                                            file_name=test_file_name(top_level)))
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
        # FIXME: we exclude modules because some of them need the part database
        if not top_level == TopLevel.Module:
            file.append(f"  import {test_package_name(top_level)}\n")

    return file

def generate_deftest(argument: Optional[str], test_suffix: str):
    resolved_pcb_object = f"{package_name}/{pcb_object.name}"
    test_name = "test-" + resolved_pcb_object.replace('/', '_') + test_suffix
    if argument is None:
        formatted_argument = ""
    else:
        formatted_argument = f"({argument})"
    evaluated_pcb_object = f"{resolved_pcb_object}{formatted_argument}"
    test_files[pcb_object.type].extend(format_file_template(DEFTEST_TEMPLATE,
                                                            test_name=test_name,
                                                            evaluated_pcb_object=evaluated_pcb_object))
    print(f"> Found {pcb_object.type.value} {evaluated_pcb_object}")

if __name__ == "__main__":
    os.makedirs(OUTPUT_DIRECTORY, exist_ok=True)
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
                pcb_objects = parse_pcb_objects(file, file_path)
                if pcb_objects:
                    package_name = parse_package_name(file)
                    for pcb_object in pcb_objects:
                        if pcb_object.arguments is None:
                            generate_deftest(None, "")
                        else:
                            for idx, argument in enumerate(pcb_object.arguments):
                                if len(pcb_object.arguments) == 1:
                                    test_suffix = ""
                                else:
                                    test_suffix = str(idx)
                                generate_deftest(argument, test_suffix)

    write_stanza_dot_proj()
    write_output_file(TEST_ENTRYPOINT_FILE_NAME, generate_test_entrypoint_file())
    for top_level, test_file in test_files.items():
        write_output_file(test_file_name(top_level), test_file)
