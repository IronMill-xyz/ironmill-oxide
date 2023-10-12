import re
import prompt_toolkit
from prompt_toolkit.validation import Validator
import ironmill_oxide.bundler as bundler

MAX_DESCRIPTION_CHARS = 500
MAX_NON_DESCRIPTION_CHARS = 100

def main(file):
    print('\nThis utility will walk you through specifying the details of the circuit you are publishing.')

    # Get user input for the circuit metadata
    name = prompt_toolkit.prompt(
        "package name: ",
        validate_while_typing=True,
        validator=Validator.from_callable(
            __is_valid_name,
            error_message="Not a valid package name",
            move_cursor_to_end=True,
        ),
        )

    description = prompt_toolkit.prompt("description: ",
        validate_while_typing=True,
        validator=Validator.from_callable(
            __is_valid_description,
            error_message=f"Too many characters ({MAX_DESCRIPTION_CHARS})",
            move_cursor_to_end=True,
        ),
        )

    author = prompt_toolkit.prompt("author: ",
        validate_while_typing=True,
        validator=Validator.from_callable(
            __is_valid_name,
            error_message="Not a valid author name",
            move_cursor_to_end=True,
        ),
        )

    version = prompt_toolkit.prompt(
        "version: (1.0.0) ",
        validate_while_typing=True,
        validator=Validator.from_callable(
            __is_valid_version,
            error_message="Not a valid package version",
            move_cursor_to_end=True,
        ),
        default='1.0.0',
        )

    # Bundle metadata plus circom file
    metadata = {
        'repo_name': name,
        'description': description,
        'author': author,
        'version': version,
    }

    bundler.bundle(metadata, file)

def __is_valid_name(s: str) -> bool:
    pattern = re.compile(r"^([a-z]|[0-9]|-|_)+$")
    return pattern.match(s) is not None and len(s) <= MAX_NON_DESCRIPTION_CHARS

def __is_valid_description(s: str) -> bool:
    return len(s) <= MAX_DESCRIPTION_CHARS

def __is_valid_version(s: str) -> bool:
    pattern = re.compile(r"^([0-9]+.[0-9]+.[0-9]+)+$")
    return pattern.match(s) is not None and len(s) <= MAX_NON_DESCRIPTION_CHARS
