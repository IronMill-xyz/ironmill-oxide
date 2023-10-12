import pytest
import os
from ironmill_oxide.cli.commands import init
from ironmill_oxide.error import OxideError

"""
NOTE
tmp_path is a special pytest name that creates a temporary directory
"""


def test_second_init_errors(tmp_path):
    os.chdir(tmp_path)
    init.main()
    with pytest.raises(OxideError):
        init.main()
