import json
import os
from typing import List
import datetime
import semver
from zipfile import ZipFile
import io
import requests
from ironmill_oxide import hash_verifier
from ironmill_oxide.error import OxideError
import ironmill_oxide.settings as settings
import shutil

# Size in characters of the different columns
NAME_WIDTH = 20
AUTHOR_WIDTH = 10
DATE_WIDTH = 10
VERSION_WIDTH = 8

class Row:
    def __init__(self,
                 name: str,
                 description: str,
                 author: str,
                 date: str,
                 version: str,
                 ) -> None:
        self.name = name
        self.description = description
        self.author = author
        self.date = date
        self.version = version

    def __str__(self) -> str:
        result = ''
        for field, width in [
            (self.name, NAME_WIDTH),
            (self.description, Row.get_description_width()),
            (self.author, AUTHOR_WIDTH),
            # TODO Fix the formatting on date
            (self.date, DATE_WIDTH),
            (self.version, VERSION_WIDTH)
            ]:

            alignment = '{0: <' + str(width) + '}'
            
            field_s = str(field)
            if len(field_s) > width:
                field_s = field_s[0:width - 3] + '...'
            
            result += alignment.format(field_s)
            result += ' | '

        return result.rstrip(' | ')

    @staticmethod
    def get_header() -> str:
        result = ''

        for field, width in [
            ('name', NAME_WIDTH),
            ('description', Row.get_description_width()),
            ('author', AUTHOR_WIDTH),
            ('date', DATE_WIDTH),
            ('version', VERSION_WIDTH)
            ]:

            alignment = '{0: <' + str(width) + '}'

            result += alignment.format(field).upper()
            result += ' | '
        
        return result.rstrip(' | ')

    @staticmethod
    def get_description_width() -> int:
        return os.get_terminal_size().columns - NAME_WIDTH - AUTHOR_WIDTH - DATE_WIDTH - VERSION_WIDTH - 3 * 4

def search(search_term: str) -> List[Row]:
    # Send a request to the registry to search the given name
    params = {'search_term': search_term}
    url = f'{settings.REGISTRY_URL}/search'
    response = requests.get(url, params=params)
    try:
        content = json.loads(response.content)
    except json.JSONDecodeError:
        raise OxideError("Search response was invalid json")

    return list(map(lambda row: 
        Row(
            name=row.get('repo_name'),
            description=row.get('description'),
            author=row.get('author'),
            date=row.get('updated'),
            version=row.get('version'),
        )
    , content.get('results')))

# Check whether the circuit with given name exists in the registry
def exists(name: str) -> bool:
    return __get_data(name) is not None

# Get the hash for the circuit with given name
def get_hash(name: str) -> str:
    # TODO Rename to bundle_hash
    return __get_data(name).get('circuit_hash')

# Get the version for the circuit with given name
def get_version(name: str) -> str:
    return __get_data(name).get('version')

# Download and unzip the given bundle to the circuits dir
def get_bundle(name: str, verify: bool):
    params = {'repo_name': name}
    url = f'{settings.REGISTRY_URL}/get_bundle'
    response = requests.get(url, params=params)

    # Handle response code
    if not response.ok:
        raise OxideError(f'Circuit {name} does not exist in the registry')

    # Extract from the byte-stream (Without writing to a temporary zip file)
    bundle_path = f'{settings.DEP_DIR}/{name}'
    with ZipFile(io.BytesIO(response.content)) as zFile:
        zFile.extractall(path=bundle_path)

    # Verify that the given hash matches the directory's hash
    if verify and not hash_verifier.verify(bundle_path, name):
        shutil.rmtree(bundle_path)
        print(f"Deleted {bundle_path}")
        raise OxideError(f"Downloaded circuit {name}'s hash is different from the registry's hash")

# Get data for circuit with given name
def __get_data(name: str):
    params = {'repo_name': name}
    url = f'{settings.REGISTRY_URL}/get_data'
    response = requests.get(url, params=params)

    try:
        content = json.loads(response.content)
    except json.JSONDecodeError:
        raise OxideError("Search response was invalid json")
    
    return content.get('results')
