import os.path
from ironmill_oxide.error import OxideError
import ironmill_oxide.settings as settings

def main():
    if os.path.exists(settings.MANIFEST):
        raise OxideError(f'{settings.MANIFEST} already exists')
    
    f = open(settings.MANIFEST, 'x')
    print(f'Create new {settings.MANIFEST} manifest')
