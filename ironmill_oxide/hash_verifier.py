import hashlib
import os.path
from ironmill_oxide import registry

# The size for each block read from the file
BLOCK_SIZE = 65536

def verify(root_dir, name):
    # Create the hash object
    hash = hashlib.sha256()
    
    # Look at each of the paths expected in the circuit's dir
    for subpath in [
        'index.js',
        f'{name}.zkey',
        f'{name}_js/{name}.wasm',
        f'{name}_js/Prover.js',
        f'{name}_js/Verifier.js',
    ]:
        path = f'{root_dir}/{subpath}'

        __update_hash(hash, path)

    return hash.hexdigest() == registry.get_hash(name)

# Update the given hash to include a hash of the contents specified by path
def __update_hash(hash, path):
    if os.path.exists(path):
        with open(path, 'rb') as f: # Open the file to read its bytes
            fb = f.read(BLOCK_SIZE) # Read from the file. Take in the amount declared above
            while len(fb) > 0: # While there is still data being read from the file
                hash.update(fb) # Update the hash
                fb = f.read(BLOCK_SIZE) # Read the next block from the file
