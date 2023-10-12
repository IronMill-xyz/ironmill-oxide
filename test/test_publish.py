import pytest
from unittest.mock import patch
import os
from ironmill_oxide.cli.commands import publish
from ironmill_oxide.error import OxideError
import requests

class MockPutResponse:
    def __init__(self, status_code):
        self.status_code = status_code
    
    def status_code(self):
        return self.status_code

@patch('prompt_toolkit.prompt', return_value='user_input')
@patch('requests.put', return_value=MockPutResponse(400))
def test_publish_throws_if_server_response_not_ok(tmp_path, mocker):
    with open(f'{tmp_path}foo.circom', 'w+') as circom_file:
        circom_file.write('pragma circom 2.0.0;')

        with pytest.raises(OxideError):
            publish.main(circom_file)

@patch('prompt_toolkit.prompt', return_value='user_input')
@patch('requests.put', return_value=MockPutResponse(201))
def test_publish_doesnt_throw_if_server_response_ok(tmp_path, mocker):
    with open(f'{tmp_path}foo.circom', 'w+') as circom_file:
        circom_file.write('pragma circom 2.0.0;')

        publish.main(circom_file)
