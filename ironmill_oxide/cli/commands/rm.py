import os.path
import re
from ironmill_oxide.error import OxideError
import ironmill_oxide.settings as settings
import ironmill_oxide.util as util

def main(name: str):
    util.error_if_no_manifest()
    
    with open(settings.MANIFEST, 'r') as f:
        lines = f.readlines()

    # Seek the dep section, look for circuit, remove if present
    if not __attempt_rm(lines, name):
        raise OxideError(f'Circuit {name} not listed in the dependencies')
    
    # Overwrite the file with new lines
    with open(settings.MANIFEST, 'w') as f:
        f.writelines(lines)

# Attempt to remove circuit specified by name from the lines
def __attempt_rm(lines, name: str):
    for i in range(len(lines)):
        if lines[i].startswith(settings.DEPENDENCIES):
            # Go from start of dependency section to start of next section or end of file
            for j in range(i + 1, len(lines)):
                
                r = f"^{name}" + r"\b"
                if re.search(r, lines[j]) is not None:
                    print(f'Removed circuit {name}')
                    
                    lines.pop(j)

                    return True
                
                # Stop looking once dependency section ends
                elif lines[j].startswith('['):
                    break
            break
    return False