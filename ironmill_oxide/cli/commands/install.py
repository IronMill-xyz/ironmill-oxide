import os
import shutil

from ironmill_oxide import hash_verifier
import ironmill_oxide.settings as settings
from ironmill_oxide.error import OxideError
import ironmill_oxide.util as util
import ironmill_oxide.registry as registry

def main(verify: bool):
    util.error_if_no_manifest()

    # Open the manifest to read
    with open(settings.MANIFEST, 'r') as f:
        lines = f.readlines()
    
    # Ensure circuit folder exists
    if not os.path.isdir(settings.DEP_DIR):
        os.mkdir(settings.DEP_DIR)
    
    # Get all dependency
    dependencies = util.get_dependencies(lines)

    # First ensure that each dependency is valid
    for dep in dependencies:
        if not registry.exists(dep):
            raise OxideError(f'Circuit {dep} listed in the {settings.MANIFEST} does not exist in the registry')

    # Verify existing local circuits, or download and verify any that don't exist
    amt_downloaded = 0
    for dep in dependencies:
        amt_downloaded += __verify_or_download(dep, verify)

    # Print if succesful
    print(f'Succesfully installed {amt_downloaded} packages')

def __verify_or_download(name: str, verify: bool) -> bool:
    if __is_installed(name):
        if not verify:
            return False
        else:
            # Verify that it hashes correctly
            bundle_path = f'{settings.DEP_DIR}/{name}'
            if hash_verifier.verify(bundle_path, name):
                # Don't bother to download this dependency
                print(f'Dependency is already installed: {name}')
                return False
        
        # If not, delete it and download again or error
        shutil.rmtree(bundle_path)
        print(f"Local bundle for dependency {name} doesn't match the hash listed on the registry")
        print(f"Deleted bundle {name}")
        print("Attempting to redownload...")
    
    # Download bundle from the registry
    registry.get_bundle(name, verify)
    print(f'Downloaded {name}')
    return True

# Check whether the given circuit is installed locally
def __is_installed(name: str) -> bool:
    return os.path.isdir(f'{settings.DEP_DIR}/{name}')
