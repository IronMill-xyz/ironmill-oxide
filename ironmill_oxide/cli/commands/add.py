from ironmill_oxide.error import OxideError
import ironmill_oxide.settings as settings
import ironmill_oxide.registry as registry
import ironmill_oxide.util as util

def main(name: str):
    util.error_if_no_manifest()
    
    # Check that circuit with this name exists in registry
    if not registry.exists(name):
        raise OxideError(f'Circuit {name} does not exist in the registry')

    with open(settings.MANIFEST, 'r') as f:
        lines = f.readlines()

    # Ensure dependency section exists (Create it if no line is [dependency])
    if not (any(line.startswith(settings.DEPENDENCIES) for line in lines)):
        lines.append(f'{settings.DEPENDENCIES}\n')
    
    # Check if the given circuit exists already
    circuit_present = name in util.get_dependencies(lines)
    
    if circuit_present:
        raise OxideError(f'Circuit {name} already exists in {settings.DEPENDENCIES}')
    # Add the circuit
    else:
        for i in range(len(lines)):
            if (lines[i].startswith(settings.DEPENDENCIES)):
                print(f'Added circuit {name}')
                
                version = registry.get_version(name)
                lines.insert(i + 1, name + ' = { version = "' + version + '" }\n')
                
                break
    
    # Overwrite the file with new lines
    with open(settings.MANIFEST, 'w') as f:
        f.writelines(lines)
