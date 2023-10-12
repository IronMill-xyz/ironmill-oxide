import io
import json
import requests
import ironmill_oxide.settings as settings
from ironmill_oxide.error import OxideError

# Send the given metadata + file to the bundler to handle
def bundle(metadata: dict, circom_file: io.TextIOWrapper):
    try:
        response = requests.put(
            f'{settings.BUNDLER_URL}/add_circuit',
            files={'file': circom_file},
            params=metadata,
            # TODO auth
            )
        
        # Handle response code
        if response.status_code == 201: # Succesfuly created
            print(f'Circuit {metadata["repo_name"]} published to the registry')
        elif response.status_code == 200: # Already existed
            raise OxideError(f'A circuit named {metadata["repo_name"]} already exists on the registry')
        else:
            # TODO Error handle
            raise OxideError(f'Unexpected http response: {response}')
    except Exception as e:
        raise OxideError(e)

