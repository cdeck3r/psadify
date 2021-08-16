import os
import shutil

import pytest
from src.psadify import command_line

''' Unit tests for testing logs avail at startup

Usually, these logfiles are in /var/log/psad
    - /var/log/psad/top_attackers 
    - /var/log/psad/top_sigs
    - /var/log/psad/top_ports
'''


# called before each test
@pytest.fixture(autouse=True)
def setup(request, psad_log_dir, psad_log_files):
    os.makedirs(psad_log_dir, mode=0o700)

    # create files
    for f in psad_log_files:
        with open(psad_log_dir + '/' + f, 'w') as fp:
            pass

    def teardown():
        shutil.rmtree(psad_log_dir, ignore_errors=True)

    request.addfinalizer(teardown)


#
# other fixtures
#
@pytest.fixture
def psad_log_dir():
    return '/var/log/psad'


@pytest.fixture
def psad_log_files():
    return ['top_attackers', 'top_sigs', 'top_ports']


#
# unit tests start here
#
def test_complete_log_file(psad_log_dir):
    assert command_line.check_log_files(psad_log_dir)


@pytest.mark.parametrize("log_file", ['top_attackers', 'top_sigs', 'top_ports'])
def test_missing_log_file(psad_log_dir, log_file):
    # delete a log_file
    os.remove(os.path.join(psad_log_dir, log_file))
    with pytest.raises(FileNotFoundError):
        command_line.check_log_files()  # must fail
