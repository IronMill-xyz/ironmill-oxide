import argparse
import os.path
from typing import List
import re
import ironmill_oxide.settings as settings
from ironmill_oxide.error import OxideError 

# Check that the given path is a valid circom file, raise a parser error if it isn't
def is_valid_circom(parser: argparse.ArgumentParser, path: str):
    if not os.path.exists(path):
        parser.error(f'The file {path} does not exist')
    elif not path.endswith('.circom'):
        parser.error(f"The file {path} isn't a circom file")
    else:
        return open(path, 'rb')


# Error if the manifest doesn't exist
def error_if_no_manifest():
    if not os.path.exists(settings.MANIFEST):
        raise OxideError(f'Could not find {settings.MANIFEST} in {os.getcwd()} or any parent directory.\nRun oxide init to generate a manifest file.')

# Return a list of all dependencies specified by the given lines
def get_dependencies(lines: List[str]) -> List[str]:
    dependencies = []
    in_dependency_section = False
    for line in lines:
        if line.startswith(settings.DEPENDENCIES):
            in_dependency_section = True
        elif line.startswith('['):
            in_dependency_section = False
        elif in_dependency_section:
            # TODO Use version, etc and not just circuit name
            pattern = r'(\w|_|-)+'
            dependencies.append(next(re.finditer(pattern, line)).group())
    
    return dependencies
