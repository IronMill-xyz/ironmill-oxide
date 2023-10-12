# Oxide, IronMill's zero-knowledge circuit package-manager

Oxide is a package-manager that makes integrating verifiable and zero-knowledge computation into your projects a breeze.

To learn more and use the tool, register for the open-alpha:

https://oxide.is/

## Installation
Oxide is best installed globally with pip or your choice of python package-manager:
``` console
$ sudo -H python3 -m pip install ironmill-oxide
```

## About
Oxide has the following design-decisions made as opposed to other package-managers:
1. Version specifier is version (Not branch or revision)
2. No lock-file present (Shallow dependency trees)
3. Not synced (Expected large file sizes)
4. PDM (Project dependency manager)
5. "Asymmetric" - Bundled circuits we download and projects we are used in are different: Circuit manifests and project manifests look different